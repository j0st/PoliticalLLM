import csv
import pandas as pd
import numpy as np

def get_descriptives(answers: list, filename: str, test: str) -> list:
    """
    Calculates the mean, median, mode and std in the list of responses provided after iterating through the statements.
    Takes as input a list of LLM's responses and a filename.
    Returns two CSV files and a list of modes for further processing.
    """
    
    if test == "pct":
        csv_filename = f"results/experiments/pct/responses-{filename}.csv"
        results_filename = f"results/experiments/pct/descriptives-{filename}.csv"

    elif test == "wahlomat":
        csv_filename = f"results/experiments/wahlomat/responses-{filename}.csv"
        results_filename = f"results/experiments/wahlomat/descriptives-{filename}.csv"

    with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["statement_id", "statement_text", "prompt", "model_answer", "mapped_answer"])
        writer.writerows([row[0], f'"{row[1]}"', f'"{row[2]}"', f'"{row[3]}"', row[4]] for row in answers)
    
    df = pd.read_csv(csv_filename)
    grouped = df.groupby('statement_id')['mapped_answer'].agg(['mean', 'median', lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan, 'std']).reset_index()
    grouped.rename(columns={'<lambda_0>': 'mode'}, inplace=True)
    grouped.to_csv(results_filename, index=False)

    mode_values = pd.read_csv(results_filename)['mode'].tolist()

    return mode_values
