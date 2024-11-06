from compendium import logger
from compendium.embeddings import create_store_embeddings
from compendium.embeddings import get_documents
from compendium.split_from_all import get_medications

logger.info("Loading and parsing medications...")
medications = get_medications()

logger.info("Creating documents...")
documents = get_documents(medications)

logger.info("Loading/Creating embeddings...")
vectorstore = create_store_embeddings(medications)
