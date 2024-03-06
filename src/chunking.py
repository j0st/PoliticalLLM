import os
import json

from dotenv import load_dotenv

load_dotenv(override=True)
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

def sentence_chunker(manifestos):
    with open(manifestos, 'r', encoding='utf-8') as file:
        data = json.load(file)

    texts = []
    sentence = ""
    for item in data['items']:
        sub_items = item.get('items', [])
        for sub_item in sub_items:
            if not sentence:
                if sub_item['text'].endswith(('.', '!', '?')):
                    texts.append(sub_item['text'])
                else:
                    sentence += sub_item['text'] + " "
            else:
                if sub_item['text'].endswith(('.', '!', '?')):
                    sentence += sub_item['text']
                    texts.append(sentence)
                    sentence = ""
                else:
                    sentence += sub_item['text'] + " "
    return texts

#texts = slide_chunker(manifestos_json)
#texts2 = sentence_chunker(manifestos_json)
