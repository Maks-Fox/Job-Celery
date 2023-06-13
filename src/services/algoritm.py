import logging
from typing import List

from src.dto import EstimateServiceResponse
from src.services.estimation import EstimateService
from src.services.generation import KeyWordGenerationService
from src.services.parser import LinkParseService

py_logger = logging.getLogger(__name__)
py_logger.setLevel(logging.INFO)
py_handler = logging.FileHandler(f"logger.log", mode='w')
py_formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

py_handler.setFormatter(py_formatter)
py_logger.addHandler(py_handler)


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
        py_logger.info(f"Generated jobs: {job_names}")
        job_links = self.link_parse_service.execute(links, job_names)
        py_logger.info(f"Parsed links: {job_links}")
        if not job_links:
            return []
        out = self.estimate_service.execute(job_links, user_job_description)
        return out
