from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from loguru import logger  # <-- The new import
from src.core.settings import settings
import os

class DocumentProcessor:
    """
    Handles loading and chunking of raw documents.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._validate_file()

    def _validate_file(self):
        if not os.path.exists(self.file_path):
            # Log the error before crashing the app
            logger.error(f"File validation failed. Path does not exist: {self.file_path}")
            raise FileNotFoundError(f"File not found at: {self.file_path}")
        logger.debug(f"✅ File validated at: {self.file_path}")

    def load_and_chunk(self):
        """
        Loads PDF and returns a list of Document objects.
        """
        logger.info(f"Loading PDF from: {self.file_path}")
        
        try:
            loader = PyPDFLoader(self.file_path)
            raw_docs = loader.load()
            logger.debug(f"   - Loaded {len(raw_docs)} raw pages.")

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=500,
                chunk_overlap=50,
                separators=["\n\n", "\n", ".", " "]
            )
            
            chunks = text_splitter.split_documents(raw_docs)
            logger.success(f"Successfully split document into {len(chunks)} chunks.")
            return chunks

        except Exception as e:
            logger.exception(f"Critical error during processing: {e}")
            raise e