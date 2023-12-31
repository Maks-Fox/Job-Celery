import re
from typing import List

from src.services.clients import ChatGptClient, Logger


class KeyWordGenerationService:
    def __init__(self, chat_gpt_client: ChatGptClient, logger: Logger):
        self._chat_gpt = chat_gpt_client
        self._logger = logger

    @staticmethod
    def _build_text_request_(description: str) -> str:
        text = f'''
            Generate 50 common job titles in one or two words by description: 
            {description}
        '''
        return text

    @staticmethod
    def _preproc_string_(string: str) -> List[str]:
        data = string.split('\n')
        data = [el.strip() for el in data]
        data = [re.sub(pattern='\d+. ', repl='', string=el) for el in data if el]
        return data

    def execute(self, job_description: str) -> List[str]:
        try:
            msg = self._build_text_request_(job_description)
            response = self._chat_gpt.send_request(msg)
            results = self._preproc_string_(response)
            return results
        except Exception as e:
            self._logger.log_error(f'Error Generate Jobs: {str(e)}')
            return []
