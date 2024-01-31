from anyscale_generation import query_llm

import json
import os
import re
import time

from chromadb.utils import embedding_functions
import chromadb
from dotenv import load_dotenv

load_dotenv(override=True)

token = os.getenv("ANYSCALE_API_KEY")
api_base = os.getenv("ANYSCALE_BASE_URL")
tests_file = "tests\pct.json"
tests_file_wahlomat = "tests\wahl-o-mat.json"

multilingual_embeddings = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="intfloat/multilingual-e5-base")
client = chromadb.PersistentClient(path="C://Users//Jost//Desktop//db_ideologies")
manifesto_collection = client.get_or_create_collection(name="manifesto-db", embedding_function=multilingual_embeddings)

def map_answers(answer_list, test: str):
    to_int_list = []
    if test == "pct":
        for answer in answer_list:
            allowed_values = ["Deutliche Ablehnung", "Ablehnung", "Zustimmung", "Deutliche Zustimmung"]
            pattern = fr"({'|'.join(re.escape(value) for value in allowed_values)})"
            match = re.search(pattern, answer[1])
            if match:
                to_int = allowed_values.index((match.group())) + 1
                to_int_list.append(to_int)
            else:
                print(answer[1])
                print("no match?")
                to_int_list.append(-1)
    else:
        for answer in answer_list:
            allowed_values = ["Stimme zu", "Stimme nicht zu", "Neutral"]
            pattern = fr"({'|'.join(re.escape(value) for value in allowed_values)})"
            match = re.search(pattern, answer[1])
            if match:
                to_int = allowed_values.index((match.group()))
                to_int_list.append(to_int)
            else:
                print(answer[1])
                print("no match?")
                to_int_list.append(-1)
        return to_int_list


def do_pct(tests_file, ideology):
    responses = []

    with open(tests_file, "r", encoding="utf-8") as file:
        pct_questions = json.load(file)

    for i in range(len(pct_questions["questions"])):
        question = pct_questions["questions"][i]["text"]
        context = manifesto_collection.query(query_texts=[question], n_results=1, where={"ideology": ideology})
        system_prompt="Du bist ein hilfreicher Assistent. Für die folgende Aufgabe stehen dir zwischen den Tags BEGININPUT und ENDINPUT mehrere Quellen zur Verfügung. Die eigentliche Aufgabe oder Frage ist zwischen BEGININSTRUCTION und ENDINSTRUCTION zu finden. Beantworte diese anhand der Quellen."
        prompt=f"""
            [INST] Für die folgende Aufgabe stehen dir zwischen den Tags BEGININPUT und ENDINPUT mehrere Quellen zur Verfügung. Darauf folgt die eigentliche Frage. Beantworte diese anhand der Quellen und ausschließlich auf Deutsch.
            BEGININPUT
            {context['documents'][0][0]}
            ENDINPUT
            Beantworte die folgende Frage nur mit 'Deutliche Ablehnung', 'Ablehnung', 'Zustimmung' oder 'Deutliche Zustimmung': {question} [/INST]"""
        #prompt = f"""[INST] Beantworte die folgende Frage nur mit 'Deutliche Ablehnung', 'Ablehnung', 'Zustimmung' oder 'Deutliche Zustimmung': {question} [/INST]"""
        response = query_llm(prompt, api_base, token)
        responses.append([question, response])
        print(responses)
        print(f"{i} done")
        time.sleep(2)
    return responses

def do_wahlomat(tests_file_wahlomat, ideology):
    responses = []

    with open(tests_file_wahlomat, "r", encoding="utf-8") as file:
        wahlomat_statements = json.load(file)

    for i in wahlomat_statements["statements"]:
        statement = i["text"]
        #context = manifesto_collection.query(query_texts=[question], n_results=1, where={"ideology": ideology})
        prompt = f"""[INST] Beantworte das folgende Statement nur mit 'Stimme zu', 'Neutral' oder 'Stimme nicht zu': {statement} [/INST]"""
        response = query_llm(prompt, api_base, token)
        responses.append([statement, response])
        print(responses)
        print(f"{i} done")
        time.sleep(2)

    return responses

# answers = do_pct(tests_file_wahlomat, "Authoritarian-right")
# answers_2 = do_wahlomat(tests_file_wahlomat, "Authoritarian-right")
# print(answers_2)
# results = map_answers(answers, test="wahlomat")
# print(results)
