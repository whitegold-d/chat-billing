from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypedDict, Annotated, Sequence, Dict, Tuple
from uuid import UUID

from langchain_core.messages import BaseMessage, ToolMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from pydantic import SecretStr, Field

from app.infrastructure.db.model.response.message_response import MessageResponseORM
from app.interface.http.model.response.llm_response_dto import AnswerDTO
from app.prompt.prompts import select_skills_prompt
from app.service.interface.base_agent_service import BaseAgentService
from app.service.interface.base_message_service import BaseMessageService

# -----------------------------------------------------
# Config
# -----------------------------------------------------
@dataclass
class AgentConfig:
    model_name: str
    ollama_base_url: str = ""
    api_key: str = "ollama"


# -----------------------------------------------------
# LangGraph state
# -----------------------------------------------------
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    number_of_steps: int


# -----------------------------------------------------
# Data provider
# -----------------------------------------------------
class VacancyProvider(ABC):
    @abstractmethod
    def get_vacancies(self, link: str) -> str:
        raise NotImplementedError()


class MockVacancyProvider(VacancyProvider):
    def __init__(self, csv_path = "app/mock/vacancy_texts.csv"):
        self.csv_path = csv_path

    def get_vacancies(self, link: str) -> str:
        import pandas as pd

        df = pd.read_csv(self.csv_path)
        if "description" not in list(df):
            raise ValueError(".csv must contain 'description' column")
        return str(df.loc[0, "description"])

# -----------------------------------------------------
# Tools
# -----------------------------------------------------
class SkillExtractionTool:
    def __init__(self, llm: ChatOpenAI, vacancy_provider: VacancyProvider):
        self._llm = llm
        self._vacancy_provider = vacancy_provider
        self._prompt = ChatPromptTemplate.from_messages([
            ("system", select_skills_prompt),
            ("user", "Here is the posting: {vacancy}")
        ])
        self._chain = self._prompt | self._llm

    @tool
    async def job_posting_tool(self, link: str = Field(description="Link to hh.ru vacancy")) -> str:
        """Get skills from the vacancy link"""
        print(f"Execute job_posting_tool with {link}")
        result = await self._chain.ainvoke({"vacancy": self._vacancy_provider.get_vacancies(link)})
        return result.content


class ToolRegistry:
    def __init__(self, tools: Sequence[object]):
        self._tools = tools
        self._tools_by_name = dict()
        for t in self._tools:
            name = getattr(t, "__name__", None) or getattr(t, "name", None)
            self._tools_by_name[name] = t

    def get_tools_by_name(self):
        return self._tools_by_name

    def get_tools(self):
        return list(self._tools_by_name.values())


# -----------------------------------------------------
# LangGraph agent
# -----------------------------------------------------
class AgentGraph:
    def __init__(self, llm: ChatOpenAI, tool_registry: ToolRegistry):
        self._llm = llm
        self._llm_with_tools = self._llm.bind_tools(tool_registry.get_tools())
        self._tools = tool_registry.get_tools_by_name()

        self._builder = StateGraph(AgentState)
        self._builder.add_node("llm", self.call_model_node)
        self._builder.add_node("call_tools", self.call_tools_node)

        self._builder.add_edge(START, "llm")
        self._builder.add_conditional_edges("llm", self.should_continue,
                                      {
                                          "call_tools": "call_tools",
                                          "end": END
                                      })
        self._builder.add_edge("call_tools", "llm")
        self._graph = self._builder.compile()

    # --- Nodes ---
    async def call_model_node(self, agent_state: AgentState) -> AgentState:
        result = await self._llm_with_tools.ainvoke(agent_state["messages"])
        return {"messages": [result], "number_of_steps": agent_state["number_of_steps"] + 1}

    async def call_tools_node(self, agent_state: AgentState) -> AgentState:
        output = []

        for tool_call in agent_state["messages"][-1].tool_calls:
            result = self._tools[tool_call["name"]].invoke(tool_call["args"])
            output.append(ToolMessage(
                content=result,
                id=tool_call["id"],
                name=tool_call["name"]
            ))
        return {"messages": output, "number_of_steps": agent_state["number_of_steps"] + 1}

    @staticmethod
    async def should_continue(agent_state: AgentState) -> str:
        if agent_state["messages"][-1].tool_calls:
            return "call_tools"
        return "end"

    async def ainvoke(self, state: AgentState):
        result = await self._graph.ainvoke(state)
        number_of_messages = state["number_of_steps"]
        return result["messages"][-number_of_messages:]


# -----------------------------------------------------
# Service
# -----------------------------------------------------
class AgentService(BaseAgentService):
    _self = None
    _initialized = False

    def __new__(cls,
                llm: AgentConfig,
                llm_vacancy: AgentConfig):
        if cls._self is None:
            cls._self = super().__new__(cls)
            cls._self._llm_config = llm
            cls._self._llm_vacancy_config = llm_vacancy
        return cls._self

    def _lazy_init(self):
        if self._initialized:
            return

        self.llm = ChatOpenAI(
            model=self._llm_config.model_name,
            base_url=f"{self._llm_config.ollama_base_url}/v1",
            api_key=SecretStr(self._llm_config.api_key),
        )
        # self.vacancy_llm = ChatOpenAI(
        #     model=self._llm_vacancy_config.model_name,
        #     base_url=f"{self._llm_vacancy_config.ollama_base_url}/v1",
        #     api_key=SecretStr(self._llm_vacancy_config.api_key),
        # )

        self.vacancy_provider = MockVacancyProvider()
        self.skill_tool = SkillExtractionTool(self.llm, self.vacancy_provider)
        self.tool_registry = ToolRegistry([self.skill_tool.job_posting_tool])

        print(f"LOG: type of self.skill_tool.job_posting_tool: {type(self.skill_tool.job_posting_tool)}")

        self.agent_graph = AgentGraph(self.llm, self.tool_registry)

        self._initialized = True

    async def execute(self, text: str, history: Sequence[MessageResponseORM]):
        self._lazy_init()

        messages = []
        for m in history:
            if m.role == "human":
                messages.append(HumanMessage(content=m.text))
            elif m.role == "assistant":
                messages.append(AIMessage(content=m.text))
            elif m.role == "system":
                messages.append(SystemMessage(content=m.text))
            elif m.role == "tool":
                messages.append(ToolMessage(content=m.text))
            else:
                raise ValueError(f"Unknown role {m.role}")
        messages.append(HumanMessage(content=text))

        new_messages = await self.agent_graph.ainvoke({"messages": messages, "number_of_steps": 0})
        final_message = new_messages[-1].content
        print(new_messages)
        return AnswerDTO(text=final_message, used_tokens=len(final_message))