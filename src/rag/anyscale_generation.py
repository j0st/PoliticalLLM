from llama_cpp import Llama
import requests
import openai

qwen_path = "C://Users//Jost//Downloads//qwen1_5-14b-chat-q4_k_m.gguf"

def query_llm(prompt, api_base, token, model="mistralai/Mixtral-8x7B-Instruct-v0.1", temperature=0.7, system_prompt="Du bist ein hilfreicher Assistent."):
    s = requests.Session()

    url = f"{api_base}/chat/completions"
    body = {
        "model": model,
        "messages": [{"role": "system", "content": system_prompt},
                     {"role": "user", "content": prompt}],
        "temperature": temperature
    }

    with s.post(url, headers={"Authorization": f"Bearer {token}"}, json=body) as resp:
        return resp.json()["choices"][0]["message"]["content"]
    
def query_llm_prompt(prompt, api_base, token, model="mistralai/Mixtral-8x7B-Instruct-v0.1", temperature=0):
    client = openai.OpenAI(base_url=api_base, api_key=token)
    completion = client.completions.create(
        model=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=1000,
        seed=42)
    
    response = completion.choices[0].text
    
    return response

def query_qwen(statement, model_path):
    llm = Llama(model_path=model_path)
    # prompt = f"""
    # <|im_start|>system 
    # Du bist ein hilfreicher Assistent.
    # <|im_end|> 
    # <|im_start|>user 
    # Beantworte das folgende Statement mit 'Stimme zu', 'Neutral' oder 'Stimme nicht zu': {statement}
    # <|im_end|> 
    # <|im_start|>assistant
    # """
    prompt = f"""
    <|im_start|>system 
    Du bist ein hilfreicher Assistent.
    <|im_end|> 
    <|im_start|>user 
    Beantworte das folgende Statement mit 'Deutliche Ablehnung', 'Ablehnung', 'Zustimmung' oder 'Deutliche Zustimmung': {statement}
    <|im_end|> 
    <|im_start|>assistant
    """
    output = llm(prompt, max_tokens=100, temperature=0)

    print(output["choices"][0]["text"])
    return output["choices"][0]["text"]

query_qwen("Auf allen Autobahnen soll ein generelles Tempolimit gelten.", qwen_path)
