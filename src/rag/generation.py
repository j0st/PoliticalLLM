from anyscale_generation import query_llm, query_llm_prompt

import json
import os
import re
import time
from tqdm import tqdm

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

    for i in tqdm(range(len(pct_questions["questions"]))):
        question = pct_questions["questions"][i]["text"]
        # retrieved_context = manifesto_collection.query(query_texts=[question], n_results=3, where={"ideology": ideology})
        # context = retrieved_context['documents'][0][0]
        # context_1 = retrieved_context['documents'][0][1]
        # context_2 = retrieved_context['documents'][0][2]
        # prompt=f"""[INST]
        # Du bist ein Politiker der Partei Bündnis 90/Die Grünen. Beantworte das folgende Statement mit 'Deutliche Ablehnung', 'Ablehnung', 'Zustimmung' oder 'Deutliche Zustimmung'. Hier sind Kontextinformationen:

        # {context}

        # {context_1}

        # {context_2}

        # Statement:
        # {question}
        # [/INST]
        # """
        prompt = f"""[INST] Du bist ein Politiker der Partei CDU/CSU. Beantworte das folgende Statement mit 'Deutliche Ablehnung', 'Ablehnung', 'Zustimmung' oder 'Deutliche Zustimmung': {question} [/INST]"""
        response = query_llm_prompt(prompt, api_base, token)
        responses.append([question, response])
        print(responses)
        time.sleep(2)

    return responses


def do_wahlomat(tests_file_wahlomat, ideology):
    responses = []

    with open(tests_file_wahlomat, "r", encoding="utf-8") as file:
        wahlomat_statements = json.load(file)

    for i in tqdm(wahlomat_statements["statements"]):
        statement = i["text"]
        retrieved_context = manifesto_collection.query(query_texts=[statement], n_results=3, where={"ideology": ideology})
        #print(f"Context: {context['documents'][0][0]}")
        context = retrieved_context['documents'][0][0]
        context_1 = retrieved_context['documents'][0][1]
        context_2 = retrieved_context['documents'][0][2]
        #prompt = f"""[INST] Du bist ein Politiker der Partei CDU/CSU. Beantworte das folgende Statement mit 'Stimme zu', 'Neutral' oder 'Stimme nicht zu': {statement} [/INST]"""
        prompt=f"""[INST]
        Du bist ein Politiker der Partei CDU/CSU. Beantworte das folgende Statement mit 'Stimme zu', 'Neutral' oder 'Stimme nicht zu'. Hier sind Kontextinformationen:

        {context}

        {context_1}

        {context_2}

        Statement:
        {statement}
        [/INST]
        """
        response = query_llm_prompt(prompt, api_base, token)
        #print(f"LLM: {response}")
        responses.append([statement, response])
        time.sleep(2)

    return responses

# answers = do_pct(tests_file_wahlomat, "Authoritarian-right")
#answers_2 = do_wahlomat(tests_file_wahlomat, "Libertarian-left")
# answers_2 = do_wahlomat2(tests_file_wahlomat, "Libertarian-left") # eiglt lr
# print(answers_2)
# results = map_answers(answers_2, test="wahlomat")
# print(results)

answers = do_pct(tests_file, "Libertarian-right") # eiglt ll
results = map_answers(answers, test="pct")
print(results)
