from compendium.config import Config
from compendium.types.medication import Medication
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from pathlib import Path
from time import sleep

config = Config()
embeddings = OpenAIEmbeddings(model=config.embeddings_model)

def get_documents(medications: list[Medication]):
    return [
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

def create_store_embeddings(medications: list[Medication], batch_size: int = 10):
    documents = get_documents(medications)

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
        sleep(5)
        break
    vector_store.save_local(config.vectorstore_dir)


def load_embeddings(medications: list[Medication]):
    if not Path(config.vectorstore_dir).exists():
        print("No embeddings found, creating new embeddings")
        create_store_embeddings(medications)
    print("Loading embeddings")
    vector_store = FAISS.load_local(
        config.vectorstore_dir,
        OpenAIEmbeddings(),
        allow_dangerous_deserialization=True)
    return vector_store
