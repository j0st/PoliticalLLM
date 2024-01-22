import csv
import os
import json

from dotenv import load_dotenv
import requests

load_dotenv()

api_key = os.getenv("MANIFESTO_PROJECT_API_KEY")
api_root = 'https://manifesto-project.wzb.eu/api/v1/'

csv_file = os.getenv("FILEPATH_CORE_CSV")

def core_dataset_to_csv(filepath, version="MPDS2023a"):
    url = f'{api_root}get_core?api_key={api_key}&key={version}'
    response = requests.get(url)

    with open(filepath, 'w', newline='', encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(response.json()[0])
        csv_writer.writerows(response.json()[1:])
    
    print(f"Core dataset saved to {filepath}.")


def get_manifesto_ids(csv_file, country: str):
    manifesto_ids = []

    with open(csv_file, 'r', encoding="utf-8") as csvfile:
        csv_reader = csv.DictReader(csvfile)
        
        for row in csv_reader:
            if row['countryname'] == country:
                manifesto_ids.append(row['party'] + "_" + row['date'])
    
    return manifesto_ids
        

core_dataset_to_csv(csv_file)
test = get_manifesto_ids(csv_file, "Germany")
print(test)
