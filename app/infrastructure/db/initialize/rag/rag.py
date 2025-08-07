import uuid
from typing import Literal, List

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer

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
                 db_type: Literal['pgvector'] = 'pgvector',
                 embedding_name: str = "Alibaba-NLP/gte-multilingual-base",
                 ):
        self.type = db_type

        if self.type == 'pgvector':
            ...

        self._embedding_model = SentenceTransformer(model_name_or_path=embedding_name,
                                                    trust_remote_code=True)


    async def vector_search(self, user_query: str, limit: int = 5):
        query_vector = self._embedding_model.encode_query(user_query, normalize_embeddings=True)

        search_sql = """
        SELECT id, embedding <=> $1 as distance, text
        FROM documents
        ORDER BY distance
        LIMIT $2        
        """

        async with PostgreSQLConnectionManager.get_connection() as connection:
            record = await connection.fetch(search_sql, query_vector, limit)

        return record


    async def upload_documents(self, document_url: str):
        insert_document_sql = """
        INSERT INTO documents (id, text, embedding) VALUES ($1, $2, $3);
        """

        print("Document is loading ...")
        loader = PyPDFLoader(document_url)
        splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=300)
        pdf_file = await loader.aload()
        print("Loading complete. Splitting ...")
        documents = splitter.split_documents(pdf_file)
        print("Spiting done.")


        print("Vectorizing documents ...")
        vectors = self._embedding_model.encode_document([document.page_content for document in documents])
        sql_queries = [(uuid.uuid4(), document.page_content, vector) for document, vector in zip(documents, vectors)]

        print(f"Vectorizing complete. Inserting documents ...")
        async with PostgreSQLConnectionManager.get_connection() as connection:
            await connection.executemany(
                insert_document_sql,
                sql_queries
            )
            records = await connection.fetch("""SELECT * FROM documents""")
        print("Result: ", records)
