
import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class EasyApplyBot:
    def __init__(self, username, password, position, location):
        self.username = username
        self.password = password
        self.position = position
        self.location = location

        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
        self.wait = WebDriverWait(self.driver, 10)

    def login(self):
        self.driver.get("https://www.linkedin.com/login")
        self.wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(self.username)
        self.driver.find_element(By.ID, "password").send_keys(self.password)
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

    def search_jobs(self):
        self.driver.get("https://www.linkedin.com/jobs/")
        search_position = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Search jobs']")))
        search_position.clear()
        search_position.send_keys(self.position)
        location_field = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder='Search location']")
        location_field.clear()
        location_field.send_keys(self.location)
        location_field.send_keys(Keys.RETURN)

    def close_easy_apply_modal(self):
        try:
            close_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Dismiss']")
            if close_button.is_displayed():
                close_button.click()
                time.sleep(1)
                logging.info("Closed Easy Apply modal.")
        except Exception as e:
            logging.warning(f"Easy Apply modal not found or could not be closed: {e}")

    def apply_to_job(self):
        try:
            submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Submit application']")
            submit_button.click()
            logging.info("Submitted application.")
        except NoSuchElementException as e:
            logging.warning(f"Application process failed: {e}")
        finally:
            self.close_easy_apply_modal()

    def process_job_cards(self):
        job_cards = self.driver.find_elements(By.CSS_SELECTOR, "div.job-card-container")
        for card in job_cards:
            try:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", card)
                card.click()
                time.sleep(2)
                easy_apply_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'jobs-apply-button')]")))
                easy_apply_btn.click()
                time.sleep(2)
                self.apply_to_job()
            except ElementClickInterceptedException:
                logging.warning("Modal might be blocking job card click. Skipping.")
                self.close_easy_apply_modal()
            except Exception as e:
                logging.warning(f"Error processing job card: {e}")
                self.close_easy_apply_modal()

    def run(self):
        self.login()
        time.sleep(2)
        self.search_jobs()
        time.sleep(5)
        self.process_job_cards()


if __name__ == "__main__":
    bot = EasyApplyBot(
        username="simon.pearce@se.com",
        password="iFORGOTIT4LINKEDIN",
        position="Business Development",
        location="London"
    )
    bot.run()
