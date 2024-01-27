import csv
import os
import json

from dotenv import load_dotenv
import requests

load_dotenv(override=True)

ideologies = {"Authoritarian-right":["AfD"], "Authoritarian-left":["LINKE", "PDS", "L-PDS", "Pirates", ""], "Libertarian-right":["FDP", "CDU/CSU"], "Libertarian-left":["90/Greens", "SPD", "SSW"]}
api_key = os.getenv("MANIFESTO_PROJECT_API_KEY")
api_root = 'https://manifesto-project.wzb.eu/api/v1/'

csv_file = os.getenv("FILEPATH_CORE_CSV")
output_file = os.getenv("FILEPATH_OUTPUT_JSON")

def find_ideology(ideologies_d, party):
    for ideology, parties in ideologies_d.items():
        if party in parties:
            return ideology
        

def core_dataset_to_csv(filepath, version="MPDS2023a"):
    url = f'{api_root}get_core?api_key={api_key}&key={version}'
    response = requests.get(url)

    with open(filepath, 'w', newline='', encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(response.json()[0])
        csv_writer.writerows(response.json()[1:])
    
    print(f"Core dataset saved to {filepath}.")


def get_manifesto_keys(csv_file, country: str, timeframe: str):
    start_year, end_year = map(int, timeframe.split('-'))
    manifesto_keys_d = {}

    with open(csv_file, 'r', encoding="utf-8") as csvfile:
        csv_reader = csv.DictReader(csvfile)
        
        for row in csv_reader:
            if row['countryname'] == country:
                key_date = row['date']
                key_year = int(key_date[:4])
                if start_year <= key_year <= end_year:
                    ideology = find_ideology(ideologies, row['partyabbrev'])
                    metadata = []
                    metadata.extend((row["partyname"], row["partyabbrev"], row["edate"], ideology))
                    manifesto_keys_d[row['party'] + "_" + key_date] = metadata
    
    return manifesto_keys_d
        

def get_manifestos(manifesto_keys_d, output_file, ideology: str, version="2023-1"):
    manifesto_keys = []
    for key, value in manifesto_keys_d.items():
        if ideology in value:
            manifesto_keys.append(key)

    url = f'{api_root}texts_and_annotations?api_key={api_key}&{"&".join([f"keys[]={key}" for key in manifesto_keys])}&version={version}'
    response = requests.get(url)

    with open(output_file, 'w', encoding="utf-8") as file:
            json.dump(response.json(), file, ensure_ascii=False, indent=2)

    return response.json()


if __name__ == "__main__":
    #core_dataset_to_csv(csv_file)
    d_of_keys = get_manifesto_keys(csv_file, "Germany", "1998-2021")
    get_manifestos(d_of_keys, output_file, "Authoritarian-right")
