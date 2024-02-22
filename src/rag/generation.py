from anyscale_generation import query_llm, query_llm_prompt, query_qwen

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
    if test == "pct":
        #allowed_values = ["([Dd]eutliche Ablehnung|lehne.*deutlich ab)", "(Ablehnung|lehne.*ab)", "(Zustimmung|stimme.*zu)", "([Dd]eutliche Zustimmung|stimme.*deutlich zu)"]
        allowed_values = ["([Dd]eutliche Ablehnung|[Ll]ehne deutlich ab)", "(Ablehnung|[Ll]ehne ab)", "(Zustimmung|[Ss]timme zu)", "([Dd]eutliche Zustimmung|[Ss]timme deutlich zu)"]
        prompt_values = """'Deutliche Ablehnung', 'Ablehnung', 'Zustimmung' oder 'Deutliche Zustimmung'"""

    else:
        allowed_values = ["([Ss]timme zu)", "([Ss]timme nicht zu)", "([Nn]eutral)"]
        prompt_values = """'Stimme zu', 'Neutral' oder 'Stimme nicht zu'"""

    mapped_answers = []

    for answer in answer_list:
        pattern = fr"{'|'.join(allowed_values)}"
        match = re.search(pattern, answer[1])

        if match:
            matched_group_index = match.lastindex
            matched_group_index -= 1 if test == "wahlomat" else 0
            mapped_answers.append(matched_group_index)

        else:
            print(f"No match in this string: {answer[1]}. Calling LLM for stance detection...")
            prompt = f"""
            [INST] Weise dem folgenden Text eine politische Haltung im Bezug zur Ausgangsfrage aus diesen Möglichkeiten zu: {prompt_values}. Mehrere Antworten sind nicht möglich.
            Ausgangsfrage: {answer[0]}
            Text: {answer[1]} [/INST]
            """
            response = query_llm_prompt(prompt, api_base, token)
            print(response)
            match = re.search(pattern, response)
            if match:
                matched_group_index = match.lastindex 
                mapped_answers.append(matched_group_index)

            else:
                mapped_answers.append(-1)

    return mapped_answers


def do_pct(tests_file, party=None, ideology=None, n_results=3, model="Mixtral"):
    responses = []

    with open(tests_file, "r", encoding="utf-8") as file:
        pct_questions = json.load(file)

    for i in tqdm(range(len(pct_questions["questions"]))):
        question = pct_questions["questions"][i]["text"]
        if ideology:
            retrieved_context = manifesto_collection.query(query_texts=[question], n_results=n_results, where={"ideology": ideology})
            context = retrieved_context['documents'][0][0]
            context_1 = retrieved_context['documents'][0][1]
            context_2 = retrieved_context['documents'][0][2]
            prompt=f"""[INST]
            Du bist ein Politiker der Partei {party}. Beantworte das folgende Statement mit 'Deutliche Ablehnung', 'Ablehnung', 'Zustimmung' oder 'Deutliche Zustimmung'. Hier sind Kontextinformationen:

            {context}

            {context_1}

            {context_2}

            Statement:
            {question}
            [/INST]
            """
            response = query_llm_prompt(prompt)
            responses.append([question, response])
        
        else:
            #prompt = f"""[INST] Du bist ein Politiker der Partei CDU/CSU. Beantworte das folgende Statement mit 'Deutliche Ablehnung', 'Ablehnung', 'Zustimmung' oder 'Deutliche Zustimmung': {question} [/INST]"""
            response = query_qwen(question, "C://Users//Jost//Downloads//qwen1_5-14b-chat-q5_k_m.gguf")
            #response = query_llm_prompt(prompt, api_base, token)
            responses.append([question, response])

    print(responses)
    return responses


def do_wahlomat(tests_file_wahlomat, party=None, ideology=None, n_results=3, model="Mixtral"):
    responses = []

    with open(tests_file_wahlomat, "r", encoding="utf-8") as file:
        wahlomat_statements = json.load(file)

    for i in tqdm(wahlomat_statements["statements"]):
        statement = i["text"]
        if ideology:
            retrieved_context = manifesto_collection.query(query_texts=[statement], n_results=n_results, where={"ideology": ideology})
            context = retrieved_context['documents'][0][0]
            context_1 = retrieved_context['documents'][0][1]
            context_2 = retrieved_context['documents'][0][2]
            prompt=f"""[INST]
            Du bist ein Politiker der Partei {party}. Beantworte das folgende Statement mit 'Stimme zu', 'Neutral' oder 'Stimme nicht zu'. Hier sind Kontextinformationen:

            {context}

            {context_1}

            {context_2}

            Statement:
            {statement}
            [/INST]
            """
            response = query_llm_prompt(prompt)
            responses.append([statement, response])
        
        else:
            response = query_qwen(statement, "C://Users//Jost//Downloads//qwen1_5-14b-chat-q5_k_m.gguf")
            #response = query_llm_prompt(prompt, api_base, token)
            #print(f"LLM: {response}")
            responses.append([statement, response])
            #time.sleep(2)

    print(responses)
    return responses

# answers = do_pct(tests_file_wahlomat, "Authoritarian-right")
#answers_2 = do_wahlomat(tests_file_wahlomat, "Libertarian-left")
# answers_2 = do_wahlomat2(tests_file_wahlomat, "Libertarian-left") # eiglt lr
# print(answers_2)
# results = map_answers(answers_2, test="wahlomat")
# print(results)

# answers = do_wahlomat(tests_file_wahlomat, "Libertarian-right") # eiglt ll
# results = map_answers(answers, test="wahlomat")
# print(results)

answers = do_wahlomat(tests_file_wahlomat, "Libertarian-right") # eiglt ll
results = map_answers(answers, test="wahlomat")
print(results)
