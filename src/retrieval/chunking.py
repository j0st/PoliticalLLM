import os
import json

from dotenv import load_dotenv

load_dotenv()
manifestos_json = os.getenv("FILEPATH_OUTPUT_JSON")

def slide_chunker(manifestos, window_size=2):   
    with open(manifestos, 'r', encoding='utf-8') as file:
        data = json.load(file)

    texts = []

    for item in data['items']:
        sub_items = item.get('items', [])
        
        for i in range(len(sub_items) - window_size + 1):
            window = [sub_item['text'] for sub_item in sub_items[i:i+window_size]]
            concatenated_text = ' '.join(window)
            texts.append(concatenated_text)

    return texts

#texts = slide_chunker(manifestos_json)
