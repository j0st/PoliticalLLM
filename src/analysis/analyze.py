import csv
import pandas as pd
import numpy as np

def get_descriptives(answers: list):
    header = ["statement_id", "statement_text", "model_answer", "mapped_answer"]
    csv_filename = "1Test25_03_07.csv"
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        for row in answers:
            writer.writerow([row[0], '"{}"'.format(row[1]), '"{}"'.format(row[2]), row[3]])
    
    df = pd.read_csv('1Test25_03_07.csv')
    grouped = df.groupby('statement_id')['mapped_answer'].agg(['mean', 'median', lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan, 'std']).reset_index()
    grouped.rename(columns={'<lambda_0>': 'mode'}, inplace=True)
    grouped.to_csv('1Results_Test25_03_07.csv', index=False)

    with open('1Results_Test25_03_07.csv', mode='r') as file:
        reader = csv.DictReader(file)
        mode_values = []
        for row in reader:
            mode_values.append(row['mode'])

    return mode_values
