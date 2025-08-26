from typing import List, Tuple, TypedDict, Annotated
from uuid import UUID

from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from pydantic import SecretStr

from app.service.interface.base_agent_service import BaseAgentService
from app.service.interface.base_message_service import BaseMessageService


class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    number_of_steps: int


class AgentService(BaseAgentService):
    _self = None

    @tool
    async def job_posting_agent(self, arg_schema=...):
        pass


    def __new__(cls,
                message_service: BaseMessageService,
                model_name: str,
                ollama_base_url: str):
        if cls._self is None:
            cls._self = super().__new__(cls)
            cls._self.message_service = message_service
            cls._self.llm = ChatOpenAI(model=model_name,
                                       base_url=f"{ollama_base_url}/v1",
                                       api_key=SecretStr('ollama'))
            cls._self.job_posting_agent = ChatOpenAI(model=model_name,
                                                     base_url=f"{ollama_base_url}/v1",
                                                     api_key=SecretStr('ollama'))
            cls._self.tools = [cls.job_posting_agent]

            builder = StateGraph(AgentState)
            builder.add_node("llm", cls.call_model_node)
            builder.add_node("call_tools", cls.call_tools_node)

            builder.add_edge(START, "llm")
            builder.add_conditional_edges("llm",
                                          cls.should_continue,
                                          {
                                              "call_tools": "call_tools_node",
                                              "end": END
                                           })
            

            cls._self.graph = builder.compile()
        return cls._self


    # --- Define nodes ---
    async def call_model_node(self, agent_state: AgentState) -> AgentState:
        prompt = ChatPromptTemplate.from_messages(agent_state["messages"])

        return {"messages": [], "number_of_steps": agent_state["number_of_steps"] + 1}


    async def call_tools_node(self, agent_state: AgentState) -> AgentState:
        pass


    async def should_continue(self, agent_state: AgentState) -> str:
        if not agent_state["messages"][-1].tool_calls:
            return "call_job_posting_agent"
        return "end"


    # --- Service methods ---
    async def execute(self, text: str, chat_id: UUID, history_size: int):
        history = await self.message_service.get_history(chat_id=chat_id, size=history_size)
        messages = [(message.role, message.text) for message in history]
        self.graph.invoke({"messages": messages, "number_of_steps": 0})