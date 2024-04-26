import json

def slide_chunker(manifestos, window_size=2): # not used in this work
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

def get_full_sentence(manifesto_chunks):
    """
    Concatenates political statements to full sentences.
    """

    i = 0
    while i < len(manifesto_chunks) - 1:
        if len(manifesto_chunks[i]['text'] + ' ' + manifesto_chunks[i+1]['text']) <= 2000 and not manifesto_chunks[i]['text'][-1] in '.!?':
            manifesto_chunks[i]['text'] += ' ' + manifesto_chunks[i+1]['text']
            manifesto_chunks[i]['cmp_code'] += '+' + manifesto_chunks[i+1]['cmp_code']
            del manifesto_chunks[i+1]
        else:
            i += 1

    return manifesto_chunks

def statement_chunker(manifestos):
    """
    Aims to combine quasi-sentences to political statements while keeping metadata information.
    Only quasi-sentences annotated with a policy topic are considered.
    """

    concatenated_data = []
    current_cmp_code = None
    current_text = ""

    with open(manifestos, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for manifesto in data['items']:
        texts_and_metadatas = manifesto.get('items', [])
        for quasi_sentence in texts_and_metadatas:
            cmp_code = quasi_sentence.get('cmp_code')
            if cmp_code in ['NA', 'H']:
                continue  # Ignore items with cmp_code "NA" or "H" (headlines etc.)

            if quasi_sentence['cmp_code'] != current_cmp_code: # If cmp_code has changed, add the previous concatenated text to the list
                if current_text:
                    concatenated_data.append({
                        'text': current_text.strip(),
                        'cmp_code': current_cmp_code,
                        'eu_code': quasi_sentence['eu_code'],
                        'name': quasi_sentence['name'],
                        'abbreviation': quasi_sentence['abbreviation'],
                        'date': quasi_sentence['date'],
                        'political_orientation': quasi_sentence['political_orientation']
                    })

                current_text = quasi_sentence['text']
                current_cmp_code = quasi_sentence['cmp_code']

            else:
                current_text += " " + quasi_sentence['text'] # Concatenate text if cmp_code remains the same

        # Append last quasi-sentence
        if current_text:
            concatenated_data.append({
                'text': current_text.strip(),
                'cmp_code': current_cmp_code,
                'eu_code': texts_and_metadatas[-1]['eu_code'],
                'name': texts_and_metadatas[-1]['name'],
                'abbreviation': texts_and_metadatas[-1]['abbreviation'],
                'date': texts_and_metadatas[-1]['date'],
                'political_orientation': texts_and_metadatas[-1]['political_orientation']
            })
    
    results = get_full_sentence(concatenated_data)
