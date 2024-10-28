from compendium.split_from_all import get_medications
from compendium.embeddings import load_embeddings
from compendium.predict import suggest_medication

medications = get_medications()
vectorstore, documents = load_embeddings(medications)

# suggest_medication(query="", vector_store=vectorstore, documents=documents)

import pdb; pdb.set_trace()
