import chunking as chunking_function
from chromadb.utils import embedding_functions
import chromadb

data = "data\manifestos.json"
data_ideology = ["data\manifestos_al.json", "data\manifestos_ar.json", "data\manifestos_ll.json", "data\manifestos_lr.json"]

#docs = chunking_function.slide_chunker(data)
docs_al, docs_ar, docs_ll, docs_lr = [chunking_function.sentence_chunker(data) for data in data_ideology]

ids_al = [f"id_al_{i}" for i in range(len(docs_al))]
ids_ar = [f"id_ar_{i}" for i in range(len(docs_ar))]
ids_ll = [f"id_ll_{i}" for i in range(len(docs_ll))]
ids_lr = [f"id_lr_{i}" for i in range(len(docs_lr))]

metadatas_al = [{"ideology": "Authoritarian-left"} for _ in range(len(ids_al))]
metadatas_ar = [{"ideology": "Authoritarian-right"} for _ in range(len(ids_ar))]
metadatas_ll = [{"ideology": "Libertarian-left"} for _ in range(len(ids_ll))]
metadatas_lr = [{"ideology": "Libertarian-right"} for _ in range(len(ids_lr))]

multilingual_embeddings = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="jost/multilingual-e5-base-politics-de")

client = chromadb.PersistentClient(path="C://Users//Jost//Desktop//db_ideologies") # save vector database locally
manifesto_collection = client.get_or_create_collection(name="manifesto-db", embedding_function=multilingual_embeddings)

# manifesto_collection.add(documents=docs_al, ids=ids_al, metadatas=metadatas_al)
# manifesto_collection.add(documents=docs_ar, ids=ids_ar, metadatas=metadatas_ar)
# manifesto_collection.add(documents=docs_ll, ids=ids_ll, metadatas=metadatas_ll)
# manifesto_collection.add(documents=docs_lr, ids=ids_lr, metadatas=metadatas_lr)

# results = manifesto_collection.query(
#     query_texts=["Auf allen Autobahnen soll ein generelles Tempolimit gelten."],
#     n_results=3,
#     where={"ideology": "Authoritarian-left"}
# )


# print(results)

# results = manifesto_collection.query(
#     query_texts=["Auf allen Autobahnen soll ein generelles Tempolimit gelten."],
#     n_results=3,
#     where={"ideology": "Authoritarian-right"}
# )

# print(results)

# results = manifesto_collection.query(
#     query_texts=["Auf allen Autobahnen soll ein generelles Tempolimit gelten."],
#     n_results=3,
#     where={"ideology": "Libertarian-left"}
# )


# print(results)

# results = manifesto_collection.query(
#     query_texts=["Auf allen Autobahnen soll ein generelles Tempolimit gelten."],
#     n_results=3,
#     where={"ideology": "Libertarian-right"}
# )


# print(results)

print(manifesto_collection.count())
