import requests

def query_llm(prompt, api_base, token, model="mistralai/Mixtral-8x7B-Instruct-v0.1", temperature=0.7):
    s = requests.Session()

    url = f"{api_base}/chat/completions"
    body = {
        "model": model,
        "messages": [{"role": "system", "content": "Du bist ein hilfreicher Assistent."},
                     {"role": "user", "content": prompt}],
        "temperature": temperature
    }

    with s.post(url, headers={"Authorization": f"Bearer {token}"}, json=body) as resp:
        return resp.json()["choices"][0]["message"]["content"]
