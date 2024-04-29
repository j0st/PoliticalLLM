import csv
import time
from tqdm import tqdm
from itertools import cycle

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def run_pct(answers: list, filename: str):
    """
    Goes through the Political Compass Test statements with a selenium webdriver since scoring details are not published.
    Takes a list of answers (mapped to integer values) and a filename as input.
    Returns the ideology placement on the two-dimension spectrum as a PNG file.
    """

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))

    url = 'https://www.politicalcompass.org/test/de'

    answer_cycle = cycle(answers)

    try:
        time.sleep(5)
        driver.get(url)
        driver.minimize_window()
        time.sleep(2)

        # cookies
        cookie_confirm = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div[1]/div[2]/div[2]/button[1]/p') # sometimes first div is div[4], sometimes div[3]?
        driver.execute_script("arguments[0].click();", cookie_confirm)
        time.sleep(2)

        # go through question pages
        questions_per_page = [7, 14, 18, 12, 5, 6]

        for i in tqdm(questions_per_page):
            for j in range(1, i + 1):
                current_answer = next(answer_cycle)
                element = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/main/article/form/span[{j}]/fieldset/div/div/div/label[{current_answer}]/span')
                driver.execute_script("arguments[0].click();", element)
            
            next_page = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/main/article/form/button')
            driver.execute_script("arguments[0].click();", next_page)
            time.sleep(2)

        # results
        time.sleep(2)
        coordinates = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/main/article/section/article[1]/section/h2").text

    except Exception as error:
        print("An error occurred:", error)

    finally:    
        driver.quit()

    return coordinates


def collect_coordinates(filename, iteration):
    results_all_runs = [[] for _ in range(iteration)]

    # Read CSV file and iterate over "mapped_answer" column
    with open(f'results//experiments//pct//responses-{filename}.csv', 'r', encoding="utf-8") as file:
        reader = csv.DictReader(file)
        mapped_answers = [row['mapped_answer'] for row in reader]

    # Iterate over mapped_answers and append to the appropriate list
    for i, answer in enumerate(mapped_answers):
        index = i % iteration  # Get the index of the list to append to, cycling back to 0 after reaching 9
        results_all_runs[index].append(int(answer))

    all_coordinates = []
    for run in results_all_runs:
        while True:  # Keep trying until successful
            try:
                coordinate = run_pct(run, "test")
                all_coordinates.append(coordinate)
                break  # Exit the retry loop if successful
            except Exception as e:
                print(f"An exception occurred: {e}. Retrying...")

    return all_coordinates
