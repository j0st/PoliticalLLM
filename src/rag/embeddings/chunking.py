import os
import re
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

def sentence_chunker2(manifestos):
    with open(manifestos, 'r', encoding='utf-8') as file:
        data = json.load(file)

    texts_with_metadata = []
    current_sentences = []
    current_cmp_code = None

    for item in data['items']:
        sub_items = item.get('items', [])
        for sub_item in sub_items:
            cmp_code = sub_item.get('cmp_code')
            if cmp_code in ['NA', 'H']:
                continue  # Ignore items with cmp_code "NA" or "H"

            text = sub_item['text']
            metadata = {
                'cmp_code': cmp_code,
                'partyname': sub_item.get('name'),
                'abbreviation': sub_item.get('abbreviation'),
                'date': sub_item.get('date'),
                'ideology': sub_item.get('political_orientation')
            }

            if cmp_code == current_cmp_code:
                current_sentences.append(text)
            else:
                if current_sentences:
                    texts_with_metadata.append((" ".join(current_sentences), metadata))
                current_sentences = [text]
                current_cmp_code = cmp_code

    if current_sentences:
        texts_with_metadata.append((" ".join(current_sentences), metadata))

    return texts_with_metadata


result = sentence_chunker2(manifestos_json)

def concatenate_texts(text_list):
    concatenated_list = []
    current_text = ''
    metadata = None

    for text, meta in text_list:
        if text.endswith(('.', '!', '?')):
            if current_text:
                concatenated_list.append((current_text + ' ' + text, metadata))
                current_text = ''
            else:
                concatenated_list.append((text, meta))
        else:
            if not current_text:
                current_text = text
                metadata = meta
            else:
                current_text += ' ' + text

    if current_text:
        concatenated_list.append((current_text, metadata))

    return concatenated_list

# Concatenate texts
concatenated_list = concatenate_texts(result)
print(concatenated_list[940][0])

#texts = slide_chunker(manifestos_json)
#texts2 = sentence_chunker(manifestos_json)