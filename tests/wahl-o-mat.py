import json

test_list = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
test_list2 = [0, 2, 2, 2, 0, 2, 0, 0, 2, 2, 2, 2, 2, 0, 0, 2, 0, 0, 2, 2, 0, 2, 0, 2, 2, 0, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 0, 0]
test_list_ar = [1, 2, 2, 2, 0, 2, 2, 2, 2, 0, 2, 1, 2, 2, 1, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 2, 2, 0, 2, 0, 0, 0, 0, 2, 2, 2, 2]
test_list_ll = [1, 2, 0, 2, 0, 0, 2, 2, 2, 0, 2, 2, 0, 0, 0, 2, 0, 2, 2, 2, 0, 2, 0, 0, 2, 2, 2, 1, 1, 0, 2, 0, 0, 0, 0, 2, 0, 2]

def calculate_results(list_of_answers, path_to_party_opinions):
    max_score = len(test_list) * 2

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
    return results

results = calculate_results(test_list_ll, "tests\party_opinions.json")
print(results)
