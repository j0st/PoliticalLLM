import io
import time
from itertools import cycle

from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from tqdm import tqdm
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
        print(driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/main/article/section/article[1]/section/h2").text)
        compass = driver.find_element(By.XPATH, '//*[@id="SvgjsSvg1001"]').screenshot_as_png 
        img = Image.open(io.BytesIO(compass))
        img.save(f"results/experiments/pct/{filename}.png") 

    except Exception as error:
        print("An error occurred:", error)

    finally:    
        driver.quit()
