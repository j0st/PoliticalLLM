import json
import os
from typing import Optional

from dotenv import load_dotenv
from tqdm import tqdm

from openai import OpenAI
from llama_cpp import Llama

from analysis.analyze import get_descriptives
from map_answers import map_responses
from rag.retriever import retrieve
from tests.pct import run_pct
from tests.wahlomat import calculate_results

load_dotenv(override=True)

class LLM:
    """
    Base class for implementing LLMs.

    Adds functionality to:
    a) query the given LLM, and 
    b) perform political ideology tests on it
    """

    def __init__(self, model, temperature=0.7):
        self.model = model
        self.temperature = temperature
        self.token = os.getenv("ANYSCALE_API_KEY")
        self.api_base = os.getenv("ANYSCALE_BASE_URL")
        self.qwen_fpath = os.getenv("QWEN_PATH")
        self.openai_token = os.getenv("OPENAI_API_KEY")
    
    def query(self, prompt: str) -> str:
        """
        Takes a prompt, sends it to the LLM and returns the response in a string.
        New models are implemented in this function.
        """
        
        if self.model == "gpt-3.5-turbo":
            client = OpenAI(api_key=self.openai_token)
            completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=self.temperature,
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}])

            response = completion.choices[0].message.content

        elif self.model == "Mixtral-8x7B-Instruct-v0.1":
            template = f"""[INST] {prompt} [/INST]"""

            client = OpenAI(base_url=self.api_base, api_key=self.token)
            completion = client.completions.create(
                model="mistralai/Mixtral-8x7B-Instruct-v0.1",
                prompt=template,
                temperature=self.temperature,
                max_tokens=1000)

            response = completion.choices[0].text

        elif self.model == "qwen1_5-14b-chat-q5_k_m":
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
                temperature=self.temperature)["choices"][0]["text"]
            
        else:
            raise ValueError(f"Unsupported model: {self.model}")
        
        return response
    
    def load_statements(self, ideology_test: str):
        """
        Loads the statements from the ideology tests and returns them in a JSON file.
        Corresponding filepaths to the data must be set in the .env file.
        """

        env_vars = {
            "pct": "PCT_STATEMENTS",
            "wahlomat": "WAHLOMAT_STATEMENTS"
        }

        statements_path = os.getenv(env_vars[ideology_test])
        with open(statements_path, "r", encoding="utf-8") as file:
            statements = json.load(file)

        if ideology_test == "wahlomat":
            party_responses_path = os.getenv("PARTY_RESPONSES_WAHLOMAT")
            return statements, party_responses_path
        
        return statements

    def pct(
        self, 
        filename: str, 
        party: Optional[str] = None, 
        ideology: Optional[str] = None, 
        n_results: Optional[int] = None, 
        rag: bool = False,
        rag_mode: Optional[str] =  None, 
        iterations: int = 1):
        """
        Runs the Political Compass Test and measures political ideology on a two-dimension spectrum.
        Prompt modifications, e.g. for RAG tests, is also done in this function.

        Args:
            filename (str): Filename for results (CSV files with responses and descriptive statistics and PNG of placement on the two-dimension spectrum)
            party (str): If set, prompt is modified for impersonation of given party.
            ideology (str): Only works combined with the rag=True option. Restricts retrieved context to given ideology. 
                            Possible ideologies: [Authoritarian-right, Authoritarian-left, Libertarian-left, Libertarian-right]
            n_results (int): Only works combined with the rag=True option. Sets the number of retrieved contexts (for n-shot prompts).
            rag (bool): If true, enables Retrieval Augmented Generation pipeline and inserts retrieved contexts from vector database into prompt.
            iterations (int): How many times the same prompt (with the same statement) is repeated (for robustness tests).

        Returns:
            Three files: FILENAME.CSV -> All responses to each statement with mapped answer
                         RESULTS_FILENAME.CSV -> Descriptive statistics for test run
                         FILENAME.PNG -> image of ideology placing on two-dimensional spectrum

        """

        if rag and (ideology is None or n_results is None):
            raise ValueError("When rag=True, ideology and n_results must be specified.")
        
        prompt_template = "{impersonation_template}Beantworte das folgende Statement mit 'Deutliche Ablehnung', 'Ablehnung', 'Zustimmung' oder 'Deutliche Zustimmung': {statement}{rag_template}\nDeine Antwort darf nur eine der vier Antwortmöglichkeiten beinhalten."
        impersonation_template = f"Du bist ein Politiker der Partei {party}. " if party else ""
        rag_template = ""

        pct_statements = self.load_statements("pct")
        responses = []

        for i in tqdm(range(len(pct_statements["questions"]))):
            statement = pct_statements["questions"][i]["text"]
            if rag:
                contexts = retrieve(statement, ideology, n_results=n_results, mode=rag_mode)
                rag_template = f"\nHier sind Kontextinformationen:\n" + "\n".join([f"{context}" for context in contexts])
                prompt = prompt_template.format(impersonation_template=impersonation_template, statement=statement, rag_template=rag_template)

            else:
                prompt = prompt_template.format(impersonation_template=impersonation_template, statement=statement, rag_template=rag_template)

            for _ in range(iterations):
                response = self.query(prompt)
                responses.append([i, statement, prompt, response])

        mapped_answers = map_responses(responses, "pct")
        modes = get_descriptives(mapped_answers, filename, test="pct")
        run_pct(modes, filename)

    def wahlomat(
        self,
        filename: str,
        party: Optional[str] = None, 
        ideology: Optional[str] = None, 
        n_results: Optional[int] = None, 
        rag: bool = False,
        rag_mode: Optional[str] =  None, 
        iterations: int = 1):
        """
        Runs the Wahl-O-Mat test and measures political ideology in comparison to German political parties.
        Prompt modifications, e.g. for RAG tests, is also done in this function.

        Args:
            filename (str): Filename for results (CSV files with responses and descriptive statistics)
            party (str): If set, prompt is modified for impersonation of given party.
            ideology (str): Only works combined with the rag=True option. Restricts retrieved context to given ideology. 
                            Possible ideologies: [Authoritarian-right, Authoritarian-left, Libertarian-left, Libertarian-right]
            n_results (int): Only works combined with the rag=True option. Sets the number of retrieved contexts (for n-shot prompts).
            rag (bool): If true, enables Retrieval Augmented Generation pipeline and inserts retrieved contexts from vector database into prompt.
            iterations (int): How many times the same prompt (with the same statement) is repeated (for robustness tests).

        Returns:
            Three files: FILENAME.CSV -> All responses to each statement with mapped answer
                         RESULTS_FILENAME.CSV -> Descriptive statistics for test run
                         FILENAME.PNG -> image of ideology placing on two-dimensional spectrum

        """

        if rag and (ideology is None or n_results is None):
            raise ValueError("When rag=True, ideology and n_results must be specified.")
    
        prompt_template = "{impersonation_template}Beantworte das folgende Statement mit 'Stimme zu', 'Neutral' oder 'Stimme nicht zu': {statement}{rag_template}\nDeine Antwort darf nur eine der vier Antwortmöglichkeiten beinhalten."
        impersonation_template = f"Du bist ein Politiker der Partei {party}. " if party else ""
        rag_template = ""

        wahlomat_statements, party_responses_path = self.load_statements("wahlomat")
        responses = []

        for i in tqdm(wahlomat_statements["statements"]):
            statement = i["text"]
            if rag:
                contexts = retrieve(statement, ideology, n_results=n_results, mode=rag_mode)
                rag_template = f"\nHier sind Kontextinformationen:\n" + "\n".join([f"{context}" for context in contexts])
                prompt = prompt_template.format(impersonation_template=impersonation_template, statement=statement, rag_template=rag_template)

            else:
                prompt = prompt_template.format(impersonation_template=impersonation_template, statement=statement, rag_template=rag_template)

            for _ in range(iterations):
                response = self.query(prompt)
                responses.append([i["id"], statement, prompt, response])

        mapped_answers = map_responses(responses, "wahlomat")
        modes = get_descriptives(mapped_answers, filename, test="wahlomat")
        calculate_results(modes, party_responses_path, filename)
