from anyscale_generation import query_llm
from chunking import slide_chunker
import os
import time
import re
import requests
from tqdm import tqdm
import uuid
import json

from llama_index import StringIterableReader, TreeIndex
from llama_index.node_parser import SimpleNodeParser
from llama_index.schema import MetadataMode
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv

load_dotenv()

token = os.getenv("ANYSCALE_API_KEY")
api_base = os.getenv("ANYSCALE_BASE_URL")

def load_corpus(files, verbose=False):
    if verbose:
        print(f"Loading files...")

    docs = StringIterableReader().load_data(texts=files)
    if verbose:
        print(f'Loaded {len(docs)} docs')
    
    parser = SimpleNodeParser.from_defaults()
    nodes = parser.get_nodes_from_documents(docs, show_progress=verbose)

    if verbose:
        print(f'Parsed {len(nodes)} nodes')

    corpus = {node.node_id: node.get_content(metadata_mode=MetadataMode.NONE) for node in nodes}
    return corpus

def generate_synthetic_dataset(corpus, num_questions_per_chunk=2):
    queries = {}
    relevant_docs = {}
    for node_id, text in tqdm(corpus.items()):
        context_str = text
        prompt = f"""
        Kontextinformationen sind unten aufgeführt.

        ---------------------
        {context_str}
        ---------------------

        Basierend auf den gegebenen Kontextinformationen und ohne Vorwissen.

        Sie sind ein neutraler Politiker. Ihre Aufgabe ist es, {num_questions_per_chunk} politische Aussagen für einen politischen Test vorzubereiten. Die Aussagen sollten in ihrer Natur vielfältig sein und sich auf das Dokument beziehen. Beschränken Sie die Aussagen auf die bereitgestellten Kontextinformationen.

        Die Aussagen sollen politische Ideologie messen und könnten beispielsweise folgendermaßen aussehen:

        Wie bewerten Sie die Aussage: 'Die Förderung von Windenergie soll beendet werden.'?
        a. stimme zu
        b. neutral
        c. stimme nicht zu

        Wie bewerten Sie die Aussage: 'Steuererhöhungen sind notwendig, um soziale Programme zu finanzieren.'?
        a. stimme zu
        b. neutral
        c. stimme nicht zu

        Ihre Fragen sollten auf politische Aussagen wie diese abzielen. Die Antwortmöglichkeiten sollen in Ihrer Antwort nicht auftauchen, sondern nur die Aussage an sich. Sätze wie 'Wie bewerten Sie die Aussage:' vor oder nach der eigentlichen Aussage sollen ebenfalls weggelassen werden.
        """
        response = query_llm(prompt, api_base, token)
        time.sleep(5)
        result = str(response).strip().split("\n")
        questions = [re.sub(r"^\d+[\).\s]", "", question).strip() for question in result]
            
        for question in questions:
            question_id = str(uuid.uuid4())
            queries[question_id] = question
            relevant_docs[question_id] = [node_id]
        
    return queries, relevant_docs

if __name__ == "__main__":
    data = "data\manifestos.json"
    docs = slide_chunker(data)
    train, val = train_test_split(docs, test_size=0.2, random_state=42)
    train_corpus = load_corpus(train[:100], True)
    val_corpus = load_corpus(val[:20], True)
    train_queries_small, train_relevant_docs_small = generate_synthetic_dataset(train_corpus)
    val_queries_small, val_relevant_docs_small = generate_synthetic_dataset(val_corpus)
    path = "C://Users//Jost//Desktop//finetuning"
    with open(path + "//train_queries.json", 'w+') as f:
        json.dump(train_queries_small, f)

    with open(path + "//train_docs.json", 'w+') as f:
        json.dump(train_relevant_docs_small, f)

    with open(path + "//val_queries.json", 'w+') as f:
        json.dump(val_queries_small, f)

    with open(path + "//val_docs.json", 'w+') as f:
        json.dump(val_relevant_docs_small, f)

    TRAIN_DATASET_FPATH = 'C://Users//Jost//Desktop//finetuning//train_dataset.json'
    VAL_DATASET_FPATH = 'C://Users//Jost//Desktop//finetuning//val_dataset.json'

    train_dataset = {
    'queries': train_queries_small,
    'corpus': train_corpus,
    'relevant_docs': train_relevant_docs_small,
    }

    val_dataset = {
        'queries': val_queries_small,
        'corpus': val_corpus,
        'relevant_docs': val_relevant_docs_small,
    }

    with open(TRAIN_DATASET_FPATH, 'w+') as f:
        json.dump(train_dataset, f)

    with open(VAL_DATASET_FPATH, 'w+') as f:
        json.dump(val_dataset, f)
