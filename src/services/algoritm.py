from typing import List

from src.dto import EstimateServiceResponse
from src.services.estimation import EstimateService
from src.services.generation import KeyWordGenerationService
from src.services.parser import LinkParseService


class AlgorithmService:
    def __init__(self,
                 generation_service: KeyWordGenerationService,
                 link_parse_service: LinkParseService,
                 estimate_service: EstimateService):
        self.generation_service = generation_service
        self.link_parse_service = link_parse_service
        self.estimate_service = estimate_service

    def execute(self, user_job_description: str, links: List[str]) -> List[EstimateServiceResponse]:
        job_names = self.generation_service.execute(user_job_description)
        job_links = self.link_parse_service.execute(links, job_names)
        # print('---' * 20)
        # print(f'job links: {job_links}')
        # print('---' * 20)
        if not job_links:
            return []
        out = self.estimate_service.execute(job_links, user_job_description)
        # print('---' * 20)
        # print(f'estimations: {out}')
        # print('---' * 20)
        return out
