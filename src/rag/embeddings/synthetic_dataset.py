# script for generating synthetic data for finetuning sentence embeddings models, needs refactoring
import json
import os
import random
import re
import uuid

from dotenv import load_dotenv
from sklearn.model_selection import train_test_split
from tqdm import tqdm

from openai import OpenAI
from llama_index import StringIterableReader, TreeIndex
from llama_index.node_parser import SimpleNodeParser
from llama_index.schema import MetadataMode

from chunking import statement_chunker

load_dotenv(override=True)

api_key = os.getenv("OPENAI_API_KEY")


def filter_and_select_random(statements_list: list):
    """
    Selects randomly 500 examples from each ideology (length <= 1000 to avoid very long statements)
    """

    filtered_statements = [statement for statement in statements_list if len(statement) <= 1000]

    return random.sample(filtered_statements, min(len(filtered_statements), 500))


def query(api_key, prompt: str) -> str:
    """
    Query LLM (gpt-3.5-turbo)
    """

    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        temperature=0.7,
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}])
    
    return completion.choices[0].message.content


def load_corpus(files):
    """
    Llama_index implementation to load docs with unique ids is used and adapted here.
    """

    docs = StringIterableReader().load_data(texts=files)   
    parser = SimpleNodeParser.from_defaults()
    nodes = parser.get_nodes_from_documents(docs, show_progress=True)
    corpus = {node.node_id: node.get_content(metadata_mode=MetadataMode.NONE) for node in nodes}

    return corpus


def generate_synthetic_dataset(corpus):
    """
    Iterates over corpus and generates a hypothetical questions for each item by an LLM.
    """

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

        Sie sind ein neutraler Politiker. Ihre Aufgabe ist es, eine politische Aussage für einen politischen Test vorzubereiten. Die Aussage sollte in ihrer Natur vielfältig sein und sich auf das Dokument beziehen. Beschränken Sie diese Aussage auf die bereitgestellten Kontextinformationen.

        Die Aussage soll politische Ideologie messen und könnte beispielsweise folgendermaßen in einem Test auftauchen:

        Wie bewerten Sie die Aussage: 'Die Förderung von Windenergie soll beendet werden.'?
        a. stimme zu
        b. neutral
        c. stimme nicht zu

        Wie bewerten Sie die Aussage: 'Steuererhöhungen sind notwendig, um soziale Programme zu finanzieren.'?
        a. stimme zu
        b. neutral
        c. stimme nicht zu

        Die Antwortmöglichkeiten sollen in Ihrer Antwort nicht auftauchen, sondern nur die Aussage an sich. Sätze wie 'Wie bewerten Sie die Aussage:' vor oder nach der eigentlichen Aussage sollen ebenfalls weggelassen werden. Die Antwort soll aus nur einem Satz bestehen.
        """

        response = query(api_key, prompt)

        # Extract questions if LLM decides to format the question awkwardly
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
    docs_al, docs_ar, docs_ll, docs_lr = [statement_chunker(manifesto) for manifesto in ideology_manifestos]
    	
    # get list of statements for each ideology
    list_of_statements_al = [item["text"] for item in docs_al]
    list_of_statements_ar = [item["text"] for item in docs_ar]
    list_of_statements_ll = [item["text"] for item in docs_ll]
    list_of_statements_lr = [item["text"] for item in docs_lr]

    #randomize and max length 500
    random_statements_al = filter_and_select_random(list_of_statements_al)
    random_statements_ar = filter_and_select_random(list_of_statements_ar)
    random_statements_ll = filter_and_select_random(list_of_statements_ll)
    random_statements_lr = filter_and_select_random(list_of_statements_lr)

    all_random_statements = [] # total of 2000
    all_random_statements.extend(random_statements_al)
    all_random_statements.extend(random_statements_ar)
    all_random_statements.extend(random_statements_ll)
    all_random_statements.extend(random_statements_lr)

    # split training corpus into train and val
    train, val = train_test_split(all_random_statements, test_size=0.2, random_state=42)
    train_corpus = load_corpus(train)
    val_corpus = load_corpus(val)

    # generate synthetic dataset
    train_queries, train_relevant_docs = generate_synthetic_dataset(train_corpus)
    val_queries, val_relevant_docs = generate_synthetic_dataset(val_corpus)

    # save dataset in data/
    train_dataset_fpath = 'data/train_dataset.json'
    val_dataset_fpath = 'data/val_dataset.json'

    train_dataset = {
    'queries': train_queries,
    'corpus': train_corpus,
    'relevant_docs': train_relevant_docs,
    }

    val_dataset = {
        'queries': val_queries,
        'corpus': val_corpus,
        'relevant_docs': val_relevant_docs,
    }

    with open(train_dataset_fpath, 'w+', encoding="utf-8") as f:
        json.dump(train_dataset, f, ensure_ascii=False)

    with open(val_dataset_fpath, 'w+', encoding="utf-8") as f:
        json.dump(val_dataset, f, ensure_ascii=False)
