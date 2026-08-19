from abc import ABC, abstractmethod

from selenium.webdriver.remote.webdriver import WebDriver

from searching_offers.domains.offer import Offer


class OfferProcessorPort(ABC):
    def __init__(self, driver: WebDriver):
        self.driver = driver

    @abstractmethod
    def process_offer_from_url(self, url: str) -> Offer:
        pass
