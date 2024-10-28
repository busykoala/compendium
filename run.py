from compendium.split_from_all import get_medications
from compendium.embeddings import load_embeddings
from compendium.embeddings import get_documents
from compendium.predict import suggest_medication

medications = get_medications()
vectorstore = load_embeddings(medications)
documents = get_documents(medications)
suggest_medication(
    "kopfschmerzen, gliederschmerzen",
    vectorstore,
    documents)
