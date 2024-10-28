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
                f"Name: {med.name}\n"
                f"Zusammensetzung: {med.composition}\n"
                f"Wirkstoffmenge pro Einheit: {med.dosage_form}\n"
                f"Indikationen/Anwendungsmöglichkeiten: {med.indications}\n"
                f"Dosierung/Anwendung: {med.dosage}\n"
                f"Kontraindikationen: {med.contraindications}\n"
                f"Warnhinweise und Vorsichtsmassnahmen: {med.warnings_and_precautions}\n"
                f"Interaktionen: {med.interactions}\n"
                f"Schwangerschaft/Stillzeit: {med.pregnancy_lactation_period}\n"
                f"Wirkung auf die Fahrtüchtigkeit und auf das Bedienen von Maschinen: {med.effects_on_the_ability_to_drive_and_operate_machinery}\n"
                f"Unerwünschte Wirkungen: {med.undesirable_effects}\n"
                f"Überdosierung: {med.overdose}\n"
                f"Eigenschaften/Wirkungen: {med.properties_effects}\n"
                f"Pharmakokinetik: {med.pharmacokinetics}\n"
                f"Präklinische Daten: {med.preclinical_data}\n"
                f"Sonstige Hinweise: {med.other_information}"
            ),
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
