import random
import os

from chromadb.utils import embedding_functions
import chromadb

def retrieve(query, ideology, n_results=3, mode="similarity") -> list:
    """
    Retrieves n most similar results from vector database (or randomly if set).
    Takes a query text and ideology metadata as input.
    Returns list of results.
    """

    multilingual_embeddings = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="intfloat/multilingual-e5-base")
    db_path = os.getenv("VECTOR_DATABASE")
    client = chromadb.PersistentClient(path=db_path)
    manifesto_collection = client.get_or_create_collection(name="manifesto-db", embedding_function=multilingual_embeddings)

    if mode == "similarity":
        retrieved_context = manifesto_collection.query(query_texts=[query], n_results=n_results, where={"ideology": ideology})
        contexts = [context for context in retrieved_context['documents']]
        contexts = contexts[0]
    
    elif mode == "random":
        retrieved_context = manifesto_collection.get(ids=["id_ar_240", "id_ar_1970", "id_ar_1980"], where={"ideology": ideology})
        contexts = [context for context in retrieved_context['documents']]

    else:
        raise ValueError(f"Unsupported mode: {mode}")

    return contexts
