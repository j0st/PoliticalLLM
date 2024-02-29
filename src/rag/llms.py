import json
import os

from dotenv import load_dotenv
from tqdm import tqdm

import openai
from llama_cpp import Llama

load_dotenv(override=True)

token = os.getenv("ANYSCALE_API_KEY")
api_base = os.getenv("ANYSCALE_BASE_URL")

qwen_fpath = os.getenv("QWEN_PATH")

class LLM:
    def __init__(self, model, temperature=0.7) -> None:
        self.model = model
        self.temperature = temperature

    def query(self, prompt):
        if self.model == "Mixtral":
            template = f"""[INST] {prompt} [/INST]"""

            client = openai.OpenAI(base_url=api_base, api_key=token)
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

            qwen = Llama(model_path=qwen_fpath)
            response = qwen(
                template,
                max_tokens=200,
                temperature=self.temperature)
            
            return response["choices"][0]["text"]
        
    def pct(party=None, ideology=None, n_results=3):
        print("pct")
        ### IMPORT FROM PTC FILE
    
    def wahlomat():
        print("wahlomat")
        ### IMPORT FROM WAHLOMAT FILE
