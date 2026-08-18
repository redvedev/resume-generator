from abc import ABC, abstractmethod

from selenium.webdriver.remote.webdriver import WebDriver


class JobServiceConnector(ABC):
    def __init__(self, driver: WebDriver):
        self.driver = driver

    @abstractmethod
    def get_offers(self, base_url: str) -> list[str]:
        pass

    @abstractmethod
    def login(self) -> None:
        pass
