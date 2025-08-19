import uuid
from typing import Literal

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pgvector import Vector
from sentence_transformers import SentenceTransformer
from sqlalchemy import select, text

from app.infrastructure.db.model.ORM.document_orm import DocumentsORM
from app.infrastructure.db.postgresql_connection_manager import PostgreSQLConnectionManager


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

        # search_sql = """
        # SELECT id, embedding <=> $1 as distance, text
        # FROM documents
        # ORDER BY distance
        # LIMIT $2
        # """

        async with PostgreSQLConnectionManager.get_session() as session:
            stmt = (
                select(
                    DocumentsORM.id,
                    DocumentsORM.embedding.cosine_distance(query_vector).label("distance"),
                    DocumentsORM.text
                ).order_by(
                    text("distance")
                ).limit(
                    limit
                ))
            result = await session.execute(stmt)
            similar_entries = result.all()
        return similar_entries


    async def upload_documents(self, document_url: str):
        insert_document_sql = "INSERT INTO documents (id, text, embedding) VALUES (:id, :text, :embedding);"

        print("Document is loading ...")
        loader = PyPDFLoader(document_url)
        splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=300)
        pdf_file = await loader.aload()
        print("Loading complete. Splitting ...")
        documents = splitter.split_documents(pdf_file)
        print("Spiting done.")


        print("Vectorizing documents ...")
        vectors = self._embedding_model.encode_document([document.page_content for document in documents])
        sql_queries = [{"id": uuid.uuid4(), "text": document.page_content, "embedding": str(vector.tolist())}
                       for document, vector in zip(documents, vectors)]

        print(f"Vectorizing completed. Inserting documents ...")
        async with PostgreSQLConnectionManager.get_session() as session:
            await session.execute(
                text(insert_document_sql),
                sql_queries
            )
            await session.commit()

            stmt = select(DocumentsORM)
            results = await session.execute(stmt)
            documents = results.all()
        print("Result: ", documents)
