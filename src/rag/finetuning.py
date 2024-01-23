from anyscale_generation import query_llm
import os
import time
import re
import requests
from tqdm import tqdm

from dotenv import load_dotenv

load_dotenv()

token = os.getenv("ANYSCALE_API_KEY")
api_base = os.getenv("ANYSCALE_BASE_URL")


def generate_synthetic_dataset(corpus, prompt, num_questions_per_chunk=2):    
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

        Ihre Fragen sollten auf politische Aussagen wie diese abzielen. Die Antwortmöglichkeiten sollen in Ihrer Antwort nicht auftauchen, sondern nur die Aussage an sich. Sätze wie 'Wie bewerten Sie die Aussage:' vor der eigentlichen Aussage sollen ebenfalls weggelassen werden.
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
