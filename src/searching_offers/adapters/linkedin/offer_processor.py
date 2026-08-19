from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from searching_offers.domains.offer import Offer
from searching_offers.ports.offer_processor import OfferProcessorPort


class LinkedinOfferProcessor(OfferProcessorPort):
    def _open_url(self, url):
        self.driver.get(url)

    def _get_description(self):
        wait = WebDriverWait(self.driver, 10)  # Maksymalny czas oczekiwania: 10 sekund

        # 1. Czekamy na pojawienie się przycisku "more" i go klikamy (jeśli istnieje)
        try:
            expand_button = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "button[data-testid='expandable-text-button']")
                )
            )
            self.driver.execute_script("arguments[0].click();", expand_button)
        except TimeoutException:
            # Przycisk nie pojawił się w ciągu 10s - opis może być krótki i nie wymagać rozwinięcia
            pass

        # 2. Czekamy na załadowanie głównego kontenera z tekstem opisu
        try:
            about_the_job_element = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "span[data-testid='expandable-text-box']")
                )
            )
            return about_the_job_element.text.strip()
        except TimeoutException:
            return ""

    def process_offer_from_url(self, url: str) -> Offer:
        self._open_url(url)
        wait = WebDriverWait(self.driver, 10)

        # 1. Czekamy na załadowanie głównego widoku oferty
        try:
            wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//a[contains(@aria-label, 'Apply') or .//span[text()='Apply']]",
                    )
                )
            )
        except TimeoutException:
            print(f"Ostrzeżenie: Przycisk Apply nie pojawił się dla URL: {url}")

        # 2. Pobieramy opis
        description = self._get_description()
        job_title = self.driver.title.split(" | ")[0]
        # 4. NAZWA FIRMY: Link prowadzący do podstrony firmy
        company_name = self.driver.find_element(
            By.XPATH, "//a[contains(@href, '/company/')]"
        ).text.strip()

        # 5. TAGI (Remote, Full-time itd.): Pobieramy wartości bezpośrednio z widoku tagów
        tags = []
        tag_elements = self.driver.find_elements(
            By.XPATH,
            "//div[contains(@class, '_120b64fe')]//span[contains(@class, 'cdca70f4')]",
        )
        tags = [tag.text.strip() for tag in tag_elements if tag.text.strip()]

        # Fallback w przypadku zmiany układu: szukamy spandów wewnątrz linków w bloku cech
        if not tags:
            tag_elements = self.driver.find_elements(
                By.XPATH,
                "//a[contains(@href, '/jobs/view/')]//span[contains(@class, 'cdca70f4')]",
            )
            tags = [
                tag.text.strip()
                for tag in tag_elements
                if tag.text.strip()
                and tag.text.strip() not in ["Apply", "See more jobs like this"]
            ]

        location_elem = self.driver.find_element(
            By.XPATH,
            "//span[contains(text(), 'Poland') or contains(text(), 'Krakow') or contains(text(), 'Warsaw')]",
        )
        location = location_elem.text.strip()

        # 7. ID OFERTY
        clean_url = url.split("?")[0].rstrip("/")
        linkedin_id = clean_url.split("/")[-1]

        return Offer(
            linkedin_url=url,
            linkedin_id=linkedin_id,
            description=description,
            location=location,
            job_title=job_title,
            tags=tags,
            company_name=company_name,
        )
