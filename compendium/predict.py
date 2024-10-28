from compendium.config import Config
from langchain.schema import HumanMessage
from langchain_openai import OpenAIEmbeddings
from langchain_openai.chat_models import ChatOpenAI

config = Config()
embeddings = OpenAIEmbeddings(model=config.embeddings_model)

def suggest_medication(query, vector_store, documents):
    query_embedding = embeddings.embed_query(query)
    results = vector_store.similarity_search_by_vector(query_embedding, k=5)
    prompt = f"A patient presents with the following symptoms: {query}. Suggest the most suitable medications:\n\n"

    for result in results:
        doc_content = documents[result.metadata["id"]].page_content
        prompt += f"- {doc_content}\n"

    prompt += "\nProvide a detailed recommendation based on these medications."

    llm = ChatOpenAI(model=config.chat_model)
    response = llm([HumanMessage(content=prompt)])

    return response.content
