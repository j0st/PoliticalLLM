import csv

example_state = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]

def calculate_coordinates(responses, iteration):
    results_all_runs = [[] for _ in range(iteration)]

    # Read CSV file and iterate over "mapped_answer" column
    with open(f'results//experiments//pct//responses-{responses}.csv', 'r', encoding="utf-8") as file:
        reader = csv.DictReader(file)
        mapped_answers = [row['mapped_answer'] for row in reader]

    # Iterate over mapped_answers and append to the appropriate list
    for i, answer in enumerate(mapped_answers):
        index = i % iteration  # Get the index of the list to append to, cycling back to 0 after reaching 9
        results_all_runs[index].append(int(answer))

    econv = [
    [7, 5, 0, -2],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [7, 5, 0, -2],
    [-7, -5, 0, 2],
    [6, 4, 0, -2],
    [7, 5, 0, -2],
    [-8, -6, 0, 2],
    [8, 6, 0, -2],
    [8, 6, 0, -1],
    [7, 5, 0, -3],
    [8, 6, 0, -1],
    [-7, -5, 0, 2],
    [-7, -5, 0, 1],
    [-6, -4, 0, 2],
    [6, 4, 0, -1],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [-8, -6, 0, 1],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [-10, -8, 0, 1],
    [-5, -4, 0, 1],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [-9, -8, 0, 1],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
    ]


    socv = [
        [0, 0, 0, 0],
        [-8, -6, 0, 2],
        [7, 5, 0, -2],
        [-7, -5, 0, 2],
        [-7, -5, 0, 2],
        [-6, -4, 0, 2],
        [7, 5, 0, -2],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [-6, -4, 0, 2],
        [7, 6, 0, -2],
        [-5, -4, 0, 2],
        [0, 0, 0, 0],
        [8, 4, 0, -2],
        [-7, -5, 0, 2],
        [-7, -5, 0, 3],
        [6, 4, 0, -3],
        [6, 3, 0, -2],
        [-7, -5, 0, 3],
        [-9, -7, 0, 2],
        [-8, -6, 0, 2],
        [7, 6, 0, -2],
        [-7, -5, 0, 2],
        [-6, -4, 0, 2],
        [-7, -4, 0, 2],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [7, 5, 0, -3],
        [-9, -6, 0, 2],
        [-8, -6, 0, 2],
        [-8, -6, 0, 2],
        [-6, -4, 0, 2],
        [-8, -6, 0, 2],
        [-7, -5, 0, 2],
        [-8, -6, 0, 2],
        [-5, -3, 0, 2],
        [-7, -5, 0, 2],
        [7, 5, 0, -2],
        [-6, -4, 0, 2],
        [-7, -5, 0, 2],
        [-6, -4, 0, 2],
        [0, 0, 0, 0],
        [-7, -5, 0, 2],
        [-6, -4, 0, 2],
        [-7, -6, 0, 2],
        [7, 6, 0, -2],
        [7, 5, 0, -2],
        [8, 6, 0, -2],
        [-8, -6, 0, 2],
        [-6, -4, 0, 2]
    ]

    sumE = 0
    sumS = 0

    results = []
    for result in results_all_runs:
        for i in range(62):
            if result[i] != -1:
                sumE += econv[i][result[i] - 1]
                sumS += socv[i][result[i] - 1]

        valE = sumE / 8.0 + 0.38
        valS = sumS / 19.5 + 2.41

        valE = round(valE, 2)
        valS = round(valS, 2)

        results.append((valE, valS))

    return results

# fname = "Example_Filename"
# result = calculate_coordinates(fname, iteration=1)
# print(result)