import csv
import os
import json

from dotenv import load_dotenv
import requests

load_dotenv()

api_key = os.getenv("MANIFESTO_PROJECT_API_KEY")
api_root = 'https://manifesto-project.wzb.eu/api/v1/'

csv_file = os.getenv("FILEPATH_CORE_CSV")
output_file = os.getenv("FILEPATH_OUTPUT_JSON")

def core_dataset_to_csv(filepath, version="MPDS2023a"):
    url = f'{api_root}get_core?api_key={api_key}&key={version}'
    response = requests.get(url)

    with open(filepath, 'w', newline='', encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(response.json()[0])
        csv_writer.writerows(response.json()[1:])
    
    print(f"Core dataset saved to {filepath}.")


def get_manifesto_keys(csv_file, country: str):
    manifesto_keys = []

    with open(csv_file, 'r', encoding="utf-8") as csvfile:
        csv_reader = csv.DictReader(csvfile)
        
        for row in csv_reader:
            if row['countryname'] == country:
                manifesto_keys.append(row['party'] + "_" + row['date'])
    
    return manifesto_keys
        

def get_manifestos(manifesto_keys, output_file, version="2023-1"):
    url = f'{api_root}texts_and_annotations?api_key={api_key}&{"&".join([f"keys[]={key}" for key in manifesto_keys])}&version={version}'
    response = requests.get(url)

    with open(output_file, 'w', encoding="utf-8") as file:
            json.dump(response.json(), file, ensure_ascii=False, indent=2)

    return response.json()



#core_dataset_to_csv(csv_file)
list_of_keys = get_manifesto_keys(csv_file, "Germany")
get_manifestos(list_of_keys, output_file)
