import chromadb
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from src.core.settings import settings
from loguru import logger

class VectorDBManager:
    """
    Manages interactions with the ChromaDB Vector Store.
    """
    def __init__(self , emdedding_model: str = settings.EMBEDDING_MODEL):
        self.embedding_function = HuggingFaceEmbeddings(
            model_name=emdedding_model
        )
    
        self.client = chromadb.HttpClient(
            host=settings.CHROMA_HOST, 
            port=settings.CHROMA_PORT
        )
        
        self.vector_store = Chroma(
            client=self.client,
            collection_name=settings.COLLECTION_NAME,
            embedding_function=self.embedding_function
        )

    def ingest_documents(self, documents):
        """
        Adds documents to the vector store.
        """
        logger.info(f"Ingesting {len(documents)} documents into collection: {settings.COLLECTION_NAME}...")
        self.vector_store.add_documents(documents=documents)
        logger.success("Ingestion Complete.")

    def search(self, query: str, k: int = 3):
        """
        Performs similarity search.
        """
        logger.info(f"Searching for: '{query}'")
        results = self.vector_store.similarity_search(query, k=k)
        return results