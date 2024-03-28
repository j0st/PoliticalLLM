import json

from chromadb.utils import embedding_functions
import chromadb

import chunking as chunking_function

ideology_manifestos = ["data\Authoritarian-left-manifestos.json",
                       "data\Authoritarian-right-manifestos.json",
                       "data\Libertarian-left-manifestos.json",
                       "data\Libertarian-right-manifestos.json"]

# chunking
docs_al, docs_ar, docs_ll, docs_lr = [chunking_function.sentence_chunker(manifesto) for manifesto in ideology_manifestos]
chunked_docs_al, chunked_docs_ar, chunked_docs_ll, chunked_docs_lr = [chunking_function.concatenate_texts(doc) for doc in [docs_al, docs_ar, docs_ll, docs_lr]]

# metadata
ids_al = [f"id_al_{i}" for i in range(len(chunked_docs_al))]
ids_ar = [f"id_ar_{i}" for i in range(len(chunked_docs_ar))]
ids_ll = [f"id_ll_{i}" for i in range(len(chunked_docs_ll))]
ids_lr = [f"id_lr_{i}" for i in range(len(chunked_docs_lr))]

# save ids in a file (only done once) for random option in the retriever
variable_lists = {
    "ids_Authoritarian-left": ids_al,
    "ids_Authoritarian-right": ids_ar,
    "ids_Libertarian-left": ids_ll,
    "ids_Libertarian-right": ids_lr
}

for filename, metadata_ids in variable_lists.items():
    with open(f"data/{filename}.json", "w") as file:
        json.dump(metadata_ids, file)

# get other metadata (e.g. party name, date)
metadata_al = [item[1] for item in chunked_docs_al]
metadata_ar = [item[1] for item in chunked_docs_ar]
metadata_ll = [item[1] for item in chunked_docs_ll]
metadata_lr = [item[1] for item in chunked_docs_lr]

# get list of statement for embeddings
list_of_statements_al = [item[0] for item in chunked_docs_al]
list_of_statements_ar = [item[0] for item in chunked_docs_ar]
list_of_statements_ll = [item[0] for item in chunked_docs_ll]
list_of_statements_lr = [item[0] for item in chunked_docs_lr]

# create embeddings
multilingual_embeddings = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="jost/multilingual-e5-base-politics-de")

client = chromadb.PersistentClient(path="C://Users//Jost//Desktop//manifesto-database") # save vector database locally
manifesto_collection = client.get_or_create_collection(name="manifesto-database", embedding_function=multilingual_embeddings)

manifesto_collection.add(documents=list_of_statements_al, ids=ids_al, metadatas=metadata_al)
manifesto_collection.add(documents=list_of_statements_ar, ids=ids_ar, metadatas=metadata_ar)
manifesto_collection.add(documents=list_of_statements_ll, ids=ids_ll, metadatas=metadata_ll)
manifesto_collection.add(documents=list_of_statements_lr, ids=ids_lr, metadatas=metadata_lr)

results = manifesto_collection.query(
    query_texts=["Auf allen Autobahnen soll ein generelles Tempolimit gelten."],
    n_results=3,
    where={"ideology": "Authoritarian-right"}
)

print(results)
print(manifesto_collection.count())
