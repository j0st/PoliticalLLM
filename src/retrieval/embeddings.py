import chunking as chunking_function
from chromadb.utils import embedding_functions
import chromadb

data = "data\manifestos.json"
docs = chunking_function.slide_chunker(data)
ids = [f"id{i}" for i in range(len(docs))]

multilingual_embeddings = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="intfloat/multilingual-e5-base")

client = chromadb.PersistentClient(path="C://Users//Jost//Desktop//db") # save vector database locally
hf_collection = client.get_or_create_collection(name="m-e5-base", embedding_function=multilingual_embeddings)

hf_collection.add(documents=docs[:40000], ids=ids[:40000])

results = hf_collection.query(
    query_texts=["Schulen sollten keine Anwesenheitspflicht haben."],
    n_results=1
)

print(results)

results = hf_collection.query(
    query_texts=["Auf allen Autobahnen soll ein generelles Tempolimit gelten."],
    n_results=1
)

print(results)
