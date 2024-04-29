import json
import random

from chromadb.utils import embedding_functions
import chromadb

def retrieve(query, ideology, n_results=3, mode="similarity") -> list:
    """
    Retrieves n most similar results from vector database (or randomly if set).
    Takes a query text and ideology metadata as input.
    Returns list of results.
    """

    # Load fine-tuned embedding model from Hugging Face
    multilingual_embeddings = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="jost/multilingual-e5-base-politics-de")

    client = chromadb.PersistentClient(path="\manifesto-db")
    manifesto_collection = client.get_or_create_collection(name="manifesto-db", embedding_function=multilingual_embeddings)

    if mode == "similarity":
        retrieved_context = manifesto_collection.query(query_texts=[query], n_results=n_results, where={"ideology": ideology})
        contexts = [context for context in retrieved_context['documents']]
        contexts = contexts[0]
    
    elif mode == "random":
        with open(f"data/ids_{ideology}.json", "r") as file:
            ids = json.load(file)

        random_ids = random.sample(ids, n_results)
        retrieved_context = manifesto_collection.get(ids=random_ids, where={"ideology": ideology})
        contexts = [context for context in retrieved_context['documents']]

    else:
        raise ValueError(f"Unsupported mode: {mode}")

    return contexts
