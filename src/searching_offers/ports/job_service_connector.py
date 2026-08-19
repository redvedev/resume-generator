from abc import ABC, abstractmethod

from selenium.webdriver.remote.webdriver import WebDriver

from searching_offers.domains.search_query import SearchQuery


class JobServiceConnector(ABC):
    def __init__(self, driver: WebDriver):
        self.driver = driver

    @abstractmethod
    def get_offers(self, SearchQuery) -> list[str]:
        pass

    @abstractmethod
    def login(self) -> None:
        pass
