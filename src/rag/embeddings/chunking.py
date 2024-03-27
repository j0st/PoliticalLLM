import json
import os

from dotenv import load_dotenv

load_dotenv(override=True)
manifestos_json = os.getenv("FILEPATH_OUTPUT_JSON")

def slide_chunker(manifestos, window_size=2): # not used
    """
    Sets a sliding window to each quasi-sentence and chunks them together.
    """

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
    """
    Aims to combine political statements to full sentences while keeping metadata information.
    Only quasi-sentences annotated with a policy topic are considered.
    """

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
                continue  # Ignore items with cmp_code "NA" or "H" (headlines etc.)

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

def concatenate_texts(text_list):
    """
    Used for further processing after sentence_chunker().
    To-do: Combine both functions into one, more simpler function.
    """
    
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
