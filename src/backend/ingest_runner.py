import argparse
from loguru import logger
from src.backend.core.settings import settings
from src.backend.ingestion.loader import DocumentProcessor
from src.backend.database.vector_store import VectorDBManager

def run_ingestion():
    processor = DocumentProcessor(file_path=settings.DATA_PATH)
    chunks = processor.load_and_chunk()
    db_manager = VectorDBManager()
    db_manager.ingest_documents(chunks)

def run_query(query_text: str):
    db_manager = VectorDBManager()
    results = db_manager.search(query_text)
    
    logger.info("\n--- Results ---")
    for doc in results:
        logger.info(f"{doc.page_content[:200]}...\n")

if __name__ == "__main__":
    # Simple CLI argument parser
    parser = argparse.ArgumentParser(description=settings.APP_NAME)
    parser.add_argument("--ingest", action="store_true", help="Run the ingestion pipeline")
    parser.add_argument("--query", type=str, help="Query the database")
    
    args = parser.parse_args()

    if args.ingest:
        run_ingestion()
    elif args.query:
        run_query(args.query)
    else:
        print("Please provide --ingest or --query 'Your Text'")