# script for generating synthetic data for finetuning sentence embeddings models, needs refactoring
from chunking import concatenate_texts, sentence_chunker
import os
import time
import random
import re
from tqdm import tqdm
import uuid
import json

from llama_index import StringIterableReader, TreeIndex
from llama_index.node_parser import SimpleNodeParser
from llama_index.schema import MetadataMode
import openai
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv

load_dotenv(override=True)

token = os.getenv("ANYSCALE_API_KEY")
api_base = os.getenv("ANYSCALE_BASE_URL")

def filter_and_select_random(statements_list):
    filtered_statements = [statement for statement in statements_list if len(statement) <= 250]
    return random.sample(filtered_statements, min(len(filtered_statements), 500))

def query_llm(prompt, token, api_base, temperature=0.7):
    template = f"""[INST] {prompt} [/INST]"""
    client = openai.OpenAI(base_url=api_base, api_key=token)
    completion = client.completions.create(
         model="mistralai/Mixtral-8x7B-Instruct-v0.1",
         prompt=template,
         temperature=temperature,
         max_tokens=1000)

    response = completion.choices[0].text

    return response

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

        Ihre Fragen sollten auf politische Aussagen wie diese abzielen. Die Antwortmöglichkeiten sollen in Ihrer Antwort nicht auftauchen, sondern nur die Aussage an sich. Sätze wie 'Wie bewerten Sie die Aussage:' vor oder nach der eigentlichen Aussage sollen ebenfalls weggelassen werden. Die Antwort soll aus nur einem Satz bestehen.
        """
        response = query_llm(prompt, token, api_base)
        time.sleep(5)
        result = str(response).strip().split("\n")
        questions = [re.sub(r"^\d+[\).\s]", "", question).strip() for question in result]
        questions = [question.strip('"') for question in questions]
            
        for question in questions:
            question_id = str(uuid.uuid4())
            queries[question_id] = question
            relevant_docs[question_id] = [node_id]
        
    return queries, relevant_docs

if __name__ == "__main__":
    ideology_manifestos = ["data\Authoritarian-left-manifestos.json",
                       "data\Authoritarian-right-manifestos.json",
                       "data\Libertarian-left-manifestos.json",
                       "data\Libertarian-right-manifestos.json"]

    # chunking
    docs_al, docs_ar, docs_ll, docs_lr = [sentence_chunker(manifesto) for manifesto in ideology_manifestos]
    chunked_docs_al, chunked_docs_ar, chunked_docs_ll, chunked_docs_lr = [concatenate_texts(doc) for doc in [docs_al, docs_ar, docs_ll, docs_lr]]

    # get list of statements
    list_of_statements_al = [item[0] for item in chunked_docs_al]
    list_of_statements_ar = [item[0] for item in chunked_docs_ar]
    list_of_statements_ll = [item[0] for item in chunked_docs_ll]
    list_of_statements_lr = [item[0] for item in chunked_docs_lr]

    #randomize and max length 500
    random_statements_al = filter_and_select_random(list_of_statements_al)
    random_statements_ar = filter_and_select_random(list_of_statements_ar)
    random_statements_ll = filter_and_select_random(list_of_statements_ll)
    random_statements_lr = filter_and_select_random(list_of_statements_lr)

    all_random_statements = []
    all_random_statements.extend(random_statements_al)
    all_random_statements.extend(random_statements_ar)
    all_random_statements.extend(random_statements_ll)
    all_random_statements.extend(random_statements_lr)

    train, val = train_test_split(all_random_statements, test_size=0.2, random_state=42)
    train_corpus = load_corpus(train, True)
    val_corpus = load_corpus(val, True)
    train_queries_small, train_relevant_docs_small = generate_synthetic_dataset(train_corpus)
    val_queries_small, val_relevant_docs_small = generate_synthetic_dataset(val_corpus)

    path = "C://Users//Jost//Desktop//finetuning_data"
    with open(path + "//train_queries.json", 'w+', encoding="utf-8") as f:
        json.dump(train_queries_small, f, ensure_ascii=False)

    with open(path + "//train_docs.json", 'w+', encoding="utf-8") as f:
        json.dump(train_relevant_docs_small, f, ensure_ascii=False)

    with open(path + "//val_queries.json", 'w+', encoding="utf-8") as f:
        json.dump(val_queries_small, f, ensure_ascii=False)

    with open(path + "//val_docs.json", 'w+', encoding="utf-8") as f:
        json.dump(val_relevant_docs_small, f, ensure_ascii=False)

    TRAIN_DATASET_FPATH = 'C://Users//Jost//Desktop//finetuning_data//train_dataset.json'
    VAL_DATASET_FPATH = 'C://Users//Jost//Desktop//finetuning_data//val_dataset.json'

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

    with open(TRAIN_DATASET_FPATH, 'w+', encoding="utf-8") as f:
        json.dump(train_dataset, f, ensure_ascii=False)

    with open(VAL_DATASET_FPATH, 'w+', encoding="utf-8") as f:
        json.dump(val_dataset, f, ensure_ascii=False)
