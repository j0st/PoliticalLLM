import json
import os

from dotenv import load_dotenv
from tqdm import tqdm

import openai
from llama_cpp import Llama

from generation import map_answers
from rag.retriever import retrieve
from tests.wahlomat import calculate_results, calculate_percentages
from tests.pct import run_pct

load_dotenv(override=True)

class LLM:
    def __init__(self, model, temperature=0.7) -> None:
        self.model = model
        self.temperature = temperature
        self.token = os.getenv("ANYSCALE_API_KEY")
        self.api_base = os.getenv("ANYSCALE_BASE_URL")
        self.qwen_fpath = os.getenv("QWEN_PATH")

    def query(self, prompt):
        if self.model == "Mixtral":
            template = f"""[INST] {prompt} [/INST]"""
            print(template)

            client = openai.OpenAI(base_url=self.api_base, api_key=self.token)
            completion = client.completions.create(
                model="mistralai/Mixtral-8x7B-Instruct-v0.1",
                prompt=template,
                temperature=self.temperature,
                max_tokens=1000,
                seed=42)

            response = completion.choices[0].text
            return response

        elif self.model == "Qwen":
            template = f"""<|im_start|>system 
            Du bist ein hilfreicher Assistent.
            <|im_end|> 
            <|im_start|>user 
            {prompt}
            <|im_end|> 
            <|im_start|>assistant"""

            qwen = Llama(model_path=self.qwen_fpath)
            response = qwen(
                template,
                max_tokens=200,
                temperature=self.temperature)

            return response["choices"][0]["text"]

    def pct(self, pct_img_path, party=None, ideology=None, n_results=None, rag=False):
        prompt_template = "{impersonation_template}Beantworte das folgende Statement mit 'Deutliche Ablehnung', 'Ablehnung', 'Zustimmung' oder 'Deutliche Zustimmung': {statement}{rag_template}"
        impersonation_template = ""
        rag_template = ""

        if party:
            impersonation_template = f"Du bist ein Politiker der Partei {party}. "

        pct_statements = os.getenv("PCT_STATEMENTS")
        pct_statements = os.getenv("PCT_STATEMENTS_TEST")
        responses = []

        with open(pct_statements, "r", encoding="utf-8") as file:
            pct_statements = json.load(file)

        for i in tqdm(range(len(pct_statements["questions"]))):
            statement = pct_statements["questions"][i]["text"]
            if rag:
                contexts = retrieve(statement, ideology, n_results=n_results, mode="random")
                rag_template = f" Hier sind Kontextinformationen:\n" + "\n".join([f"{context}" for context in contexts])
                prompt = prompt_template.format(impersonation_template=impersonation_template, statement=statement, rag_template=rag_template)

            else:
                prompt = prompt_template.format(impersonation_template=impersonation_template, statement=statement, rag_template=rag_template)

            response = self.query(prompt)
            responses.append([statement, response])

        mapped_answers = map_answers(responses, "pct")
        run_pct(mapped_answers, pct_img_path)

    def wahlomat(self, party=None, ideology=None, n_results=None, rag=False):
        prompt_template = "{impersonation_template}Beantworte das folgende Statement mit 'Stimme zu', 'Neutral' oder 'Stimme nicht zu': {statement}{rag_template}"
        impersonation_template = ""
        rag_template = ""

        if party:
            impersonation_template = f"Du bist ein Politiker der Partei {party}. "

        wahlomat_statements = os.getenv("WAHLOMAT_STATEMENTS")
        wahlomat_statements = os.getenv("WAHLOMAT_STATEMENTS_TEST")
        party_responses = os.getenv("PARTY_RESPONSES_WAHLOMAT")
        responses = []

        with open(wahlomat_statements, "r", encoding="utf-8") as file:
            wahlomat_statements = json.load(file)

        for i in tqdm(wahlomat_statements["statements"]):
            statement = i["text"]
            if rag:
                contexts = retrieve(statement, ideology, n_results=n_results, mode="random")
                rag_template = f" Hier sind Kontextinformationen:\n" + "\n".join([f"{context}" for context in contexts])
                prompt = prompt_template.format(impersonation_template=impersonation_template, statement=statement, rag_template=rag_template)

            else:
                prompt = prompt_template.format(statement=statement)

            response = self.query(prompt)
            responses.append([statement, response])

        mapped_answers = map_answers(responses, "wahlomat")
        results, probs_per_party = calculate_results(mapped_answers, party_responses)
        avg_probs = calculate_percentages(probs_per_party)

        print(results)
        print(avg_probs)


mixtral = LLM("Mixtral")
r = mixtral.wahlomat(party="CDU", ideology="Authoritarian-right", rag=True)
