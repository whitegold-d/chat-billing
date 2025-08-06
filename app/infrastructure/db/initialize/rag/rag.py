import uuid
from typing import Literal, List

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

from app.infrastructure.db.postgresql_connection_manager import PostgreSQLConnectionManager

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


class RAG:
    _self = None

    def __new__(cls, *args, **kwargs):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self


    def __init__(self,
                 db_type: Literal['pgvector'],
                 embedding_name: str = "Alibaba-NLP/gte-multilingual-base",
                 ):
        self.type = db_type

        if self.type == 'pgvector':
            ...

        self._embedding_model = HuggingFaceEmbeddings(model_name=embedding_name)


    async def get_vector(self, query: str):
        if not query:
            return []

        return await self._embedding_model.aembed_query(query)


    async def vector_search(self, user_query: str, limit: int = 5):
        query_vector = self.get_vector(user_query)

        search_sql = """
        SELECT id, embedding <=> $1 as distance 
        FROM documents
        ORDER BY distance
        LIMIT $2        
        """

        with PostgreSQLConnectionManager.get_connection() as connection:
            record = await connection.fetch(search_sql, query_vector, limit)

        return record


    async def upload_documents(self, document_url: str):
        insert_document_sql = """
        INSERT INTO documents (id, text, embedding) VALUES ($1, $2, $3)(
        """

        loader = PyPDFLoader(document_url)
        splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=300)
        documents = loader.load_and_split(splitter)

        vectors = await self._embedding_model.aembed_documents([document.page_content for document in documents])
        sql_queries = [(uuid.uuid4(), vector, document) for vector, document in zip(vectors, documents)]

        with PostgreSQLConnectionManager.get_connection() as connection:
            await connection.excecutemany(
                insert_document_sql,
                sql_queries
            )
            records = await connection.fetch("""SELECT * FROM documents""")
        print(records)
