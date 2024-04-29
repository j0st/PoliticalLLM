import json

from chromadb.utils import embedding_functions
import chromadb

import chunking as chunking_function

ideology_manifestos = ["data\Authoritarian-left-manifestos.json",
                       "data\Authoritarian-right-manifestos.json",
                       "data\Libertarian-left-manifestos.json",
                       "data\Libertarian-right-manifestos.json"]

def embedd_manifestos(manifesto_data):
    """
    This function chunks the manifesto data and embedds the chunks into a chroma database.
    Metadata, such as ideology and ids, to run the indirect steering experiments are also provided.
    """

    # chunking
    docs_al, docs_ar, docs_ll, docs_lr = [chunking_function.statement_chunker(manifesto) for manifesto in manifesto_data]

    # metadata
    ids_al = [f"id_al_{i}" for i in range(len(docs_al))]
    ids_ar = [f"id_ar_{i}" for i in range(len(docs_ar))]
    ids_ll = [f"id_ll_{i}" for i in range(len(docs_ll))]
    ids_lr = [f"id_lr_{i}" for i in range(len(docs_lr))]

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
    metadata_al = [item[1] for item in docs_al]
    metadata_ar = [item[1] for item in docs_al]
    metadata_ll = [item[1] for item in docs_al]
    metadata_lr = [item[1] for item in docs_al]

    # get list of statement for embeddings
    list_of_statements_al = [item[0] for item in docs_al]
    list_of_statements_ar = [item[0] for item in docs_al]
    list_of_statements_ll = [item[0] for item in docs_al]
    list_of_statements_lr = [item[0] for item in docs_al]

    # create embeddings
    multilingual_embeddings = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="jost/multilingual-e5-base-politics-de")

    client = chromadb.PersistentClient(path="manifesto-database") # save vector database locally
    manifesto_collection = client.get_or_create_collection(name="manifesto-database", embedding_function=multilingual_embeddings)

    manifesto_collection.add(documents=list_of_statements_al, ids=ids_al, metadatas=metadata_al)
    manifesto_collection.add(documents=list_of_statements_ar, ids=ids_ar, metadatas=metadata_ar)
    manifesto_collection.add(documents=list_of_statements_ll, ids=ids_ll, metadatas=metadata_ll)
    manifesto_collection.add(documents=list_of_statements_lr, ids=ids_lr, metadatas=metadata_lr)

# only done once:
# embedd_manifestos(ideology_manifestos)
