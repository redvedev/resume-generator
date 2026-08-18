from abc import ABC, abstractmethod

from searching_offers.domains.offer import Offer


class JobServiceConnector(ABC):
    def __init__(self, driver):
        self.driver = driver

    @abstractmethod
    def get_offers(self) -> list[Offer]:
        pass
