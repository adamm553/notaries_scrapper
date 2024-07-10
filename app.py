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
    # Open the specified link
    driver.get(link)

    # Accept cookies (assuming the button is in a popup or overlay)
    accept_cookies_button = driver.find_element(By.XPATH, '//*[@id="sliding-popup"]/div/div[2]/div/div/button')
    ActionChains(driver).move_to_element(accept_cookies_button).click().perform()
    print("Clicked on accept cookies button")

    # Initialize an empty list to store all notary names
    all_notary_names = []

    # Loop through each page to scrape data
    for page in range(num_pages_to_scrape):
        print(f"Scraping data from page {page + 1}")

        # Wait for the search results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'notary-name'))
        )

        # Retrieve all elements with class 'notary-name' on the current page
        notary_elements = driver.find_elements(By.CLASS_NAME, 'notary-name')

        # Extract and store notary names from the current page
        for notary in notary_elements:
            all_notary_names.append(notary.text)

        # Print notary names from the current page (optional)
        print(f"Notary names on page {page + 1}:")
        for notary_name in all_notary_names:
            print(notary_name)

        # Write data to CSV
        with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for name in all_notary_names:
                writer.writerow([name])

        # Find the Next button and click on it
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.pager__item--arrow--right a[rel="next"]'))
        )
        next_button.click()
        print(f"Clicked on Next button for page {page + 1}")

        time.sleep(5)

        # Clear the list to prepare for the next page's data
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
    # Allow some time to observe the results
    time.sleep(5)

    # Quit the driver
    driver.quit()
