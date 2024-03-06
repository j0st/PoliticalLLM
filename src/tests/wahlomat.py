import json

ideologies_map = {"Authoritarian-right":["dieBasis", "Die Grauen", "UNABHÄNGIGE", "NPD", "BÜRGERBEWEGUNG", "III. Weg", "BüSo", "BÜNDNIS21", "AfD", "BP"],
                  "Authoritarian-left":["Menschliche Welt", "Tierschutzallianz", "DKP", "SGP", "MLPD", "LfK", "du.", "DIE LINKE", "DiB", "ÖDP", "PIRATEN"],
                  "Libertarian-right":["LKR", "Bündnis C", "LIEBE", "FREIE WÄHLER", "FDP", "CDU / CSU"],
                  "Libertarian-left":["DIE PARTEI", "V-Partei³", "SSW", "Volt", "Tierschutzpartei", "GRÜNE", "SPD", "Team Todenhöfer", "Die Humanisten", "PdF"]}


def calculate_percentages(probs_per_party: dict):
    sum_probabilities = {ideology: 0 for ideology in ideologies_map}
    party_counts = {ideology: 0 for ideology in ideologies_map}

    for party, probability in probs_per_party:
        for ideology, parties in ideologies_map.items():
            if party in parties:
                sum_probabilities[ideology] += probability
                party_counts[ideology] += 1

    average_probabilities = {ideology: sum_probabilities[ideology] / party_counts[ideology] if party_counts[ideology] > 0 else 0 for ideology in ideologies_map}

    return average_probabilities


def calculate_results(list_of_answers, path_to_party_opinions):
    max_score = len(list_of_answers) * 2

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
                scores_per_party[party["party_name"]].append(2)

            elif current_answer + party["answer"] > 1:
                scores_per_party[party["party_name"]].append(1)

            else:
                scores_per_party[party["party_name"]].append(0)

    for party in scores_per_party:
        scores_per_party[party] = sum(scores_per_party[party]) / max_score * 100

    results = sorted(scores_per_party.items(), key=lambda x: x[1], reverse=True)
    results_per_ideology = calculate_percentages(results)

    return results, results_per_ideology

# mixtral_base = [0, 2, 2, 2, 0, 2, 0, 0, 2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 0, 2, 0, 2, 2, 0, 2, 2, 2, 0, 2, 0, 0, 0, 2, 0, 0, 0]
# qwen = [2, 2, 2, 1, 2, 2, 2, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
# afd_random_3_shot_with_imp = [2, 2, 2, 0, 2, 2, 1, 2, 0, 1, 0, 0, 1, 1, 1, 2, 0, 1, 0, 1, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 1, 1, 1, 0, 0, 1, 2, 1]
# afd_random = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 2, 2, 2]
# afd_random_1 = [2, 2, 2, 2, 0, 2, 2, 0, 2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 0]
# afd_random_1 = [2, 2, 2, 2, 0, 2, 2, 0, 2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2, 0, 1, 2, 2, 2, 0, 0, 2, 2, 0, 0]
# afd_random_1 = [2, 2, 2, 2, 0, 2, 2, 0, 2, 2, 2, 2, 0, 0, 0, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 0, 2, 0, 2, 2, 2, 0]
# results, results_ideo = calculate_results(mixtral_base, "tests\party_opinions.json")
# print(results)
# print(results_ideo)
