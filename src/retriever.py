from chromadb.utils import embedding_functions
import chromadb

multilingual_embeddings = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="intfloat/multilingual-e5-base")
client = chromadb.PersistentClient(path="C://Users//Jost//Desktop//db_ideologies")
manifesto_collection = client.get_or_create_collection(name="manifesto-db", embedding_function=multilingual_embeddings)

def retrieve(query, ideology, n_results=3, mode="similarity"):
    contexts = []
    if mode == "similarity":
        retrieved_context = manifesto_collection.query(query_texts=[query], n_results=n_results, where={"ideology": ideology})
        context = retrieved_context['documents'][0][0]
        context_1 = retrieved_context['documents'][0][1]
        context_2 = retrieved_context['documents'][0][2]
        contexts.append(context)
        contexts.append(context_1)
        contexts.append(context_2)
    
    else:
        retrieved_context = manifesto_collection.get(ids=["id_ar_240", "id_ar_1970", "id_ar_1980"], where={"ideology": ideology})
        context = retrieved_context['documents'][0]
        context_1 = retrieved_context['documents'][1]
        context_2 = retrieved_context['documents'][2]
        contexts.append(context)
        contexts.append(context_1)
        contexts.append(context_2)

    return contexts
