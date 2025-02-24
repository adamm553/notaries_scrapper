from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv

# Path to your ChromeDriver executable
PATH = "C:\\Program Files (x86)\\chromedriver-win64\\chromedriver.exe"
cService = ChromeService(executable_path=PATH)

# Initialize the WebDriver
driver = webdriver.Chrome(service=cService)

# URL to visit
link = "https://notaries-directory.eu/pl/search?country_code=POL"
num_pages_to_scrape = 560  # Number of pages to scrape

# CSV file path
csv_file = 'notary_data.csv'

try:
    driver.get(link)

    accept_cookies_button = driver.find_element(By.XPATH, '//*[@id="sliding-popup"]/div/div[2]/div/div/button')
    ActionChains(driver).move_to_element(accept_cookies_button).click().perform()

    all_notary_names = []

    for page in range(num_pages_to_scrape):
        print(f"Scraping data from page {page + 1}")

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'notary-name')))
        notary_elements = driver.find_elements(By.CLASS_NAME, 'notary-name')

        for notary in notary_elements:
            all_notary_names.append(notary.text)

        print(f"Notary names on page {page + 1}:")
        for notary_name in all_notary_names:
            print(notary_name)

        with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for name in all_notary_names:
                writer.writerow([name])

        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.pager__item--arrow--right a[rel="next"]')))
        next_button.click()
        print(f"Clicked on Next button for page {page + 1}")

        time.sleep(1)
        all_notary_names.clear()

except TimeoutException as e:
    print(f"Timeout occurred: {e}")
except NoSuchElementException as e:
    print(f"Element not found: {e}")
except ElementNotInteractableException as e:
    print(f"Element not interactable: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    time.sleep(5)
    driver.quit()
