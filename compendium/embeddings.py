import os
import pickle
from pathlib import Path
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from compendium.types.medication import Medication
from time import sleep

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
filename = "output/medication_embeddings.pkl"

embeddings = OpenAIEmbeddings(model="text-embedding-3-large", openai_api_key=OPENAI_API_KEY)

def create_store_embeddings(medications: list[Medication], batch_size: int = 10):
    documents = [
        Document(
            page_content=(
                f"{med.composition} {med.dosage_form} {med.indications} {med.dosage} "
                f"{med.contraindications} {med.warnings_and_precautions} {med.interactions} "
                f"{med.pregnancy_lactation_period} {med.effects_on_the_ability_to_drive_and_operate_machinery} "
                f"{med.undesirable_effects} {med.overdose} {med.properties_effects} "
                f"{med.pharmacokinetics} {med.preclinical_data} {med.other_information}"),
            metadata={"id": idx}
        )
        for idx, med in enumerate(medications)
    ]

    # Process in batches
    vector_store = None
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i + batch_size]
        batch_store = FAISS.from_documents(batch, embeddings)
        # Combine or save each batch as needed
        if vector_store is None:
            vector_store = batch_store
        else:
            vector_store.merge_from(batch_store)
        print(f"Processed {i + len(batch)} of {len(documents)} documents")
        print(f"Waiting for 5 seconds...")
        sleep(5)

    with open(filename, "wb") as f:
        pickle.dump((vector_store, documents), f)



def load_embeddings(medications: list[Medication]):
    if not Path(filename).exists():
        create_store_embeddings(medications)
    with open(filename, "rb") as f:
        vector_store, documents = pickle.load(f)
    return vector_store, documents
