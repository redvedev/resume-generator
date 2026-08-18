from abc import ABC, abstractmethod

from selenium.webdriver.remote.webdriver import WebDriver

from searching_offers.domains.offer import Offer


class JobServiceConnector(ABC):
    def __init__(self, driver: WebDriver):
        self.driver = driver

    @abstractmethod
    def get_offers(self) -> list[Offer]:
        pass

    @abstractmethod
    def login(self) -> None:
        pass
