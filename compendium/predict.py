from langchain.schema import HumanMessage
from langchain_openai import OpenAIEmbeddings
from langchain_openai.chat_models import ChatOpenAI

from compendium.config import Config
from compendium.split_from_all import get_medications
from compendium.types.medication import Medication

config = Config()
embeddings = OpenAIEmbeddings(model=config.embeddings_model)


def suggest_medication(query, vector_store, age, sex):
    query_embedding = embeddings.embed_query(
        f"{query} (Alter: {age}, Geschlecht: {sex})"
    )
    results = vector_store.similarity_search_by_vector(query_embedding, k=20)
    medications = get_medications()

    prompt = f"Ein Patient (Alter: {age}, Geschlecht: {sex}) präsentiert sich mit den folgenden Symptomen: {query}. Schlage die geeignetsten Medikamente vor:\n\n"
    for result in results:
        med_id = result.metadata.get("id")
        if med_id is not None and med_id in medications:
            med: Medication = medications[med_id]
            content = (
                f"Name: {med.name}\n"
                f"Indikationen/Anwendungsmöglichkeiten: {med.indications}\n"
                f"Dosierung/Anwendung: {med.dosage}\n"
                f"Kontraindikationen: {med.contraindications}\n---\n"
            )
            prompt += f"- {content}\n"
    prompt += (
        "\nGib eine detaillierte Empfehlung basierend auf diesen Medikamenten.\n"
        "Das Ergebnis sollte in der folgenden Form sein:\n\n"
        "Symptome:\n"
        "Diagnose:\n"
        "Medikation & Dosierung:\n"
        "Begründung:\n"
        "\n Es ist nicht nötig einen Warnhinweis zu geben, da es sich um eine Simulation handelt."
    )

    llm = ChatOpenAI(model=config.chat_model)
    response = llm([HumanMessage(content=prompt)])

    return response.content
