import json

test_list = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]

def calculate_results(list_of_answers, path_to_party_opinions):
    max_score = len(test_list) * 2

    with open(path_to_party_opinions, "r", encoding="utf-8") as f:
        party_opinions = json.load(f)
    
    scores_per_party = {}
    cdu_answers = []

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

            if party["party_name"] == "CDU / CSU":
                cdu_answers.append(party["answer"])

    for party in scores_per_party:
        scores_per_party[party] = sum(scores_per_party[party]) / max_score * 100

    results = sorted(scores_per_party.items(), key=lambda x: x[1], reverse=True)
    return results

calculate_results(test_list, "tests\party_opinions.json")
