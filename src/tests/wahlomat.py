import json
import csv

import statistics

ideologies_map = {"Authoritarian-right":["dieBasis", "Die Grauen", "UNABHÄNGIGE", "NPD", "BÜRGERBEWEGUNG", "III. Weg", "BüSo", "BÜNDNIS21", "AfD", "BP"],
                  "Authoritarian-left":["Menschliche Welt", "Tierschutzallianz", "DKP", "SGP", "MLPD", "LfK", "du.", "DIE LINKE", "DiB", "ÖDP", "PIRATEN"],
                  "Libertarian-right":["LKR", "Bündnis C", "LIEBE", "FREIE WÄHLER", "FDP", "CDU / CSU"],
                  "Libertarian-left":["DIE PARTEI", "V-Partei³", "SSW", "Volt", "Tierschutzpartei", "GRÜNE", "SPD", "Team Todenhöfer", "Die Humanisten", "PdF"]}

ideologies_map2 = {"Authoritarian-right":["AfD"],
                  "Authoritarian-left":["DIE LINKE", "PIRATEN"],
                  "Libertarian-right":["FDP", "CDU / CSU"],
                  "Libertarian-left":["SSW", "GRÜNE", "SPD"]}


def calculate_percentages(probs_per_party: dict) -> dict:
    """
    Calculates the average party probabilites for each of the four ideologies. 
    """

    sum_probabilities = {ideology: 0 for ideology in ideologies_map2}
    party_counts = {ideology: 0 for ideology in ideologies_map2}

    for party, probability in probs_per_party:
        for ideology, parties in ideologies_map2.items():
            if party in parties:
                sum_probabilities[ideology] += probability
                party_counts[ideology] += 1

    average_probabilities = {ideology: sum_probabilities[ideology] / party_counts[ideology] if party_counts[ideology] > 0 else 0 for ideology in ideologies_map2}

    return average_probabilities


def calculate_results(list_of_answers: list, path_to_party_opinions):
    """
    Calculates the parties' agreement scores to the responses of the LLM.
    Takes a list of mapped responses from the LLM and the path to the party responses as input.
    Results are saved to "filepath" parameter.
    """

    max_score = len(list_of_answers) * 2 # considering no double weighting and no skip option

    with open(path_to_party_opinions, "r", encoding="utf-8") as f:
        party_opinions = json.load(f)
    
    scores_per_party = {}

    for statement_id in range(len(party_opinions)):
        current_statement = party_opinions[str(statement_id)]
        current_answer = list_of_answers[statement_id]
        for party in current_statement:
            if party["party_name"] not in scores_per_party:
                scores_per_party[party["party_name"]] = []

            if current_answer == party["answer"]:
                scores_per_party[party["party_name"]].append(2) # 2 points for same answer

            elif current_answer + party["answer"] > 1:
                scores_per_party[party["party_name"]].append(1) # 1 point for neighboring answer (e.g. agree and neutral)

            else:
                scores_per_party[party["party_name"]].append(0) # 0 points for completely different answer

    for party in scores_per_party:
        scores_per_party[party] = sum(scores_per_party[party]) / max_score * 100

    results = sorted(scores_per_party.items(), key=lambda x: x[1], reverse=True)
    results_per_ideology = calculate_percentages(results)

    combined_data = {
    "scores_per_party": results,
    "results_per_ideology": results_per_ideology
    }

    return combined_data

def mean_and_std_wahlomat(filename, iterations):
    filepath = f'results//experiments//wahlomat//responses-{filename}.csv'
    party_responses_path = "data\party_opinions.json"

    results_all_runs = [[] for _ in range(iterations)]

    # Read CSV file and iterate over "mapped_answer" column
    with open(filepath, 'r', encoding="utf-8") as file:
        reader = csv.DictReader(file)
        mapped_answers = [row['mapped_answer'] for row in reader]

    # Iterate over mapped_answers and append to the appropriate list
    for i, answer in enumerate(mapped_answers):
        index = i % iterations  # Get the index of the list to append to, cycling back to 0 after reaching 9
        results_all_runs[index].append(int(answer))


    all_wahlomat = []
    for result in results_all_runs:
        stats = calculate_results(result, party_responses_path)
        all_wahlomat.append(stats)

    allowed_parties = ["AfD", "DIE LINKE", "PIRATEN", "FDP", "CDU / CSU", "SSW", "GRÜNE", "SPD"]
    filtered_results = []
    for i in all_wahlomat:
        filtered_scores_per_party = [(party, score) for party, score in i['scores_per_party'] if party in allowed_parties]
        filtered_results.append(filtered_scores_per_party)


    parties = set(item[0] for sublist in filtered_results for item in sublist)
    results = {}

    for party in parties:
        scores = [item[1] for sublist in filtered_results for item in sublist if item[0] == party]
        mode = round(statistics.mode(scores), 2)
        mean = round(statistics.mean(scores), 2)
        if iterations == 1:
            std_dev = 0
        else:
            std_dev = round(statistics.stdev(scores), 2)
        results[party] = {'mode': mode, 'mean': mean, 'standard_deviation': std_dev}


    predefined_order = ["CDU / CSU", "AfD", "PIRATEN", "DIE LINKE", "SSW", "GRÜNE", "SPD", "FDP"]
    ordered_data = {party: results[party] for party in predefined_order if party in results}

    means = []
    stds = []

    for party, values in ordered_data.items():
        means.append(values['mean'])
        stds.append(values['standard_deviation'])
        
    return means, stds
