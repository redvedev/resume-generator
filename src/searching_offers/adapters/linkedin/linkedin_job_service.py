import logging
import os
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from searching_offers.domains.offer import Offer
from searching_offers.domains.search_query import LinkedinSearchQuery, SearchQuery
from searching_offers.ports.job_service_connector import JobServiceConnector

logger = logging.getLogger(__name__)


class LinkedinJobService(JobServiceConnector):
    def login(self):
        linkedin_email = os.environ["LINKEDIN_EMAIL"]
        linkedin_password = os.environ["LINKEDIN_PASSWORD"]
        linkedin_login_url = "https://www.linkedin.com/login/"
        self.driver.get(linkedin_login_url)

        email_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='email']")
        visible_email = [inp for inp in email_inputs if inp.is_displayed()][0]
        visible_email.send_keys(linkedin_email)

        password_inputs = self.driver.find_elements(
            By.CSS_SELECTOR, "input[type='password']"
        )
        visible_password = [inp for inp in password_inputs if inp.is_displayed()][0]
        visible_password.send_keys(linkedin_password)

        wait = WebDriverWait(self.driver, 300)
        jobs_link = wait.until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/jobs/')]"))
        )
        logger.info("Logging successful")

    def get_page_offers(self) -> list[str]:
        """
        This returns links to jobs on this linkedin page
        """
        job_offers = self.driver.execute_script("""
            const cards = document.querySelectorAll('div[role="button"][componentkey^="job-card-component-ref-"]');

            return Array.from(cards).map(card => {
                const componentKey = card.getAttribute('componentkey') || '';
                const jobId = componentKey.replace('job-card-component-ref-', '');
                const link = jobId ? `https://www.linkedin.com/jobs/view/${jobId}/` : '';
                return link;
            });
        """)
        return job_offers

    def prepare_job_search_query(self, search_query: LinkedinSearchQuery):
        url_base = "https://www.linkedin.com/jobs/search-results/"
        post_arguments = {
            "keywords": " or ".join(search_query.keywords).replace(" ", "+"),
            "geoId": search_query.geo_id,
            "distance": round(
                search_query.distance / 1.60934, 6
            ),  # Distance in kilometers converted to miles because Linkedin requires it
        }

        post_arguments_url = "&".join([f"{k}={v}" for k, v in post_arguments.items()])

        url = f"{url_base}?{post_arguments_url}"
        return url

    def get_offers(self, search_query: SearchQuery) -> list[str]:
        self.driver.get(self.prepare_job_search_query(search_query))
        all_job_urls = list()  # Używamy set(), aby uniknąć duetów
        page_number = 1

        # Inicjalizujemy wait, by poczekać na nową stronę
        wait = WebDriverWait(self.driver, 15)

        while True:
            print(f"Pobieranie ofert ze strony {page_number}...")
            page_number += 1

            # --- NAPRAWA SCROLLOWANIA DO LAZY-LOAD ---
            # Przewijamy stronę do ostatniej karty w pętli, aż przestaną się doładowywać nowe.
            last_count = 0
            while True:
                cards = self.driver.find_elements(
                    By.CSS_SELECTOR,
                    'div[role="button"][componentkey^="job-card-component-ref-"]',
                )
                if not cards:
                    break

                # Zjedź do ostatniej znalezionej karty na liście
                self.driver.execute_script("arguments[0].scrollIntoView();", cards[-1])
                time.sleep(1.5)  # Dajemy chwilę na dociągnięcie przez LinkedIn

                # Sprawdzamy, czy doszły nowe karty
                new_count = len(
                    self.driver.find_elements(
                        By.CSS_SELECTOR,
                        'div[role="button"][componentkey^="job-card-component-ref-"]',
                    )
                )
                if new_count == last_count:
                    break  # Jeśli liczba się nie zmieniła, zjechaliśmy na sam dół tej strony
                last_count = new_count
            # ------------------------------------------

            job_elements = self.get_page_offers()
            all_job_urls.extend(job_elements)

            STOP_TEXT = "We found more results related to your search that may not be exact matches"
            if STOP_TEXT in self.driver.page_source:
                logger.info("All related offers found")
                break

            try:
                next_button = self.driver.find_element(
                    By.CSS_SELECTOR,
                    "button[data-testid='pagination-controls-next-button-visible']",
                )

                # Zanim klikniemy, zachowujemy ten "stary" przycisk
                self.driver.execute_script("arguments[0].click();", next_button)

                # --- CZEKANIE NA ZAŁADOWANIE NOWYCH OFERT ---
                # Czekamy, aż ten konkretny, stary przycisk zostanie podmieniony (strona się odświeży)
                wait.until(EC.staleness_of(next_button))

                # Dla pewności czekamy, aż pojawią się już nowe karty po odświeżeniu
                wait.until(
                    EC.presence_of_element_located(
                        (
                            By.CSS_SELECTOR,
                            'div[role="button"][componentkey^="job-card-component-ref-"]',
                        )
                    )
                )
                # --------------------------------------------

            except NoSuchElementException:
                logger.info('The "Next" button not found. Probably the end of offers')
                break
            except Exception as e:
                break

        return list(set(all_job_urls))
