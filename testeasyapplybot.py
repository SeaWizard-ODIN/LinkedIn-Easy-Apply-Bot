import json
import csv
import logging
import os
import random
import re
import time
import urllib.parse
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import yaml
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

def setup_logger():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    return logging.getLogger(__name__)

log = setup_logger()

class EasyApplyBot:
    MAX_SEARCH_TIME = 60 * 60  # 1 hour

    def __init__(self, username, password, positions, locations, 
                 phone_number, uploads={}, filename='output.csv', experience_level=[]):
        self.username = username
        self.password = password
        self.positions = positions
        self.locations = locations
        self.phone_number = phone_number
        self.uploads = uploads
        self.filename = filename
        self.experience_level = experience_level

        self.browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.wait = WebDriverWait(self.browser, 30)
        self.answers = {}

        self.login_linkedin()

    def login_linkedin(self):
        log.info("Logging into LinkedIn...")
        self.browser.get("https://www.linkedin.com/login")
        try:
            user_field = self.browser.find_element(By.ID, "username")
            pw_field = self.browser.find_element(By.ID, "password")
            user_field.send_keys(self.username)
            pw_field.send_keys(self.password)
            pw_field.send_keys(Keys.RETURN)
            time.sleep(5)
        except TimeoutException:
            log.error("Login elements not found.")

    def search_jobs(self, position, location):
        log.info(f"Searching for jobs: {position} in {location}")
        search_url = f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(position)}&location={urllib.parse.quote(location)}"
        self.browser.get(search_url)
        time.sleep(5)

    def apply_jobs(self):
        for position in self.positions:
            for location in self.locations:
                self.search_jobs(position, location)
                self.process_job_cards()

    def process_job_cards(self):
        job_cards = self.browser.find_elements(By.CLASS_NAME, "job-card-container")
        for card in job_cards:
            try:
                card.click()
                time.sleep(2)
                if self.is_easy_apply():
                    self.apply_to_job()
            except Exception as e:
                log.warning(f"Error processing job card: {e}")

    def is_easy_apply(self):
        try:
            self.browser.find_element(By.CLASS_NAME, "jobs-apply-button").click()
            return True
        except:
            return False

    def apply_to_job(self):
        try:
            time.sleep(2)
            next_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Continue to next step']")))
            next_button.click()
            time.sleep(2)

            submit_button = self.browser.find_element(By.CSS_SELECTOR, "button[aria-label='Submit application']")
            if submit_button:
                submit_button.click()
                log.info("Application submitted.")
                self.save_application(True)
            else:
                log.info("Submit button not found.")
                self.save_application(False)
        except Exception as e:
            log.warning(f"Application process failed: {e}")
            self.save_application(False)

    def save_application(self, success):
        with open(self.filename, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now(), success])

    def close_browser(self):
        self.browser.quit()

if __name__ == "__main__":
    with open("config.yaml", 'r') as file:
        config = yaml.safe_load(file)

    bot = EasyApplyBot(
        username=config['username'],
        password=config['password'],
        positions=config['positions'],
        locations=config['locations'],
        phone_number=config['phone_number'],
        uploads=config.get('uploads', {}),
        filename=config.get('output_filename', 'output.csv'),
        experience_level=config.get('experience_level', [])
    )

    bot.apply_jobs()
    bot.close_browser()
