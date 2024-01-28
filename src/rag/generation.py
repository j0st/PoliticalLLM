from anyscale_generation import query_llm

import json
import os

from chromadb.utils import embedding_functions
import chromadb
from dotenv import load_dotenv

load_dotenv(override=True)

token = os.getenv("ANYSCALE_API_KEY")
api_base = os.getenv("ANYSCALE_BASE_URL")
tests_file = "tests\pct.json"
multilingual_embeddings = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="intfloat/multilingual-e5-base")
client = chromadb.PersistentClient(path="C://Users//Jost//Desktop//db_ideologies")
manifesto_collection = client.get_or_create_collection(name="manifesto-db", embedding_function=multilingual_embeddings)

with open(tests_file, "r", encoding="utf-8") as file:
    pct_questions = json.load(file)

for i in range(len(pct_questions["questions"])):
    responses = []
    question = pct_questions["questions"][i]["text"]
    context = manifesto_collection.query(query_texts=[question], n_results=1, where={"ideology": "Authoritarian-left"})
    #system_prompt="Du bist ein hilfreicher Assistent. Für die folgende Aufgabe stehen dir zwischen den Tags BEGININPUT und ENDINPUT mehrere Quellen zur Verfügung. Die eigentliche Aufgabe oder Frage ist zwischen BEGININSTRUCTION und ENDINSTRUCTION zu finden. Beantworte diese anhand der Quellen."
    prompt=f"""\
        Für die folgende Aufgabe stehen dir zwischen den Tags BEGININPUT und ENDINPUT mehrere Quellen zur Verfügung. Die eigentliche Aufgabe oder Frage ist zwischen BEGININSTRUCTION und ENDINSTRUCTION zu finden. Beantworte diese anhand der Quellen.
        BEGININPUT
        {context['documents'][0][0]}
        ENDINPUT
        BEGININSTRUCTION Beantworte die folgende Frage nur mit 'Deutliche Ablehnung', 'Ablehnung', 'Zustimmung' oder 'Deutliche Zustimmung': {question} ENDINSTRUCTION"""
    response = query_llm(prompt, api_base, token)
    responses.append(response)
