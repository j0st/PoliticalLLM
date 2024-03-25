import csv
import os
import json

from dotenv import load_dotenv
import requests

load_dotenv(override=True)

ideologies = {"Authoritarian-right":["AfD"],
              "Authoritarian-left":["LINKE", "PDS", "L-PDS", "Pirates", ""],
              "Libertarian-right":["FDP", "CDU/CSU"],
              "Libertarian-left":["90/Greens", "SPD", "SSW"]}

api_key = os.getenv("MANIFESTO_PROJECT_API_KEY")
api_root = 'https://manifesto-project.wzb.eu/api/v1/'

def find_ideology(ideologies_d, party):
    for ideology, parties in ideologies_d.items():
        if party in parties:
            return ideology
        

def core_dataset_to_csv(version="MPDS2023a"):
    url = f'{api_root}get_core?api_key={api_key}&key={version}'
    response = requests.get(url)
    fpath = f"data/core_dataset_{version}.csv"

    with open(fpath, 'w', newline='', encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(response.json()[0])
        csv_writer.writerows(response.json()[1:])

    return fpath


def get_manifesto_keys(country: str, timeframe: str):
    csv_file = core_dataset_to_csv()
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
        

def get_manifestos(ideology: str, country: str, timeframe: str, version="2023-1"):
    manifesto_keys_d = get_manifesto_keys(country, timeframe)
    manifesto_keys = []
    for key, value in manifesto_keys_d.items():
        if ideology in value:
            manifesto_keys.append(key)

    url = f'{api_root}texts_and_annotations?api_key={api_key}&{"&".join([f"keys[]={key}" for key in manifesto_keys])}&version={version}'
    response = requests.get(url)

    with open(f"data/{ideology}_manifestos.json", 'w', encoding="utf-8") as file:
            json.dump(response.json(), file, ensure_ascii=False, indent=2)

    json_data = response.json()
    for item in json_data["items"]:
        key = item["key"]
        for item in item["items"]:
            if key in manifesto_keys_d:
                values = manifesto_keys_d[key]
                item["name"] = values[0]
                item["abbreviation"] = values[1]
                item["date"] = values[2]
                item["political_orientation"] = values[3]
    
    with open(f"data/{ideology}_TEST.json", 'w', encoding="utf-8") as file:
            json.dump(json_data, file, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    [get_manifestos(ideology, "Germany", "1998-2021") for ideology in ideologies]
