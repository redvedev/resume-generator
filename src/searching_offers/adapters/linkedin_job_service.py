from searching_offers.domains.offer import Offer
from searching_offers.ports.job_service_connector import JobServiceConnector


class LinkedinJobService(JobServiceConnector):
    def login(self):
        pass

    def get_offers(self) -> list[Offer]:
        return []
