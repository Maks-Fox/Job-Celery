import random
import re
import time
from typing import List, Optional
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from selenium.webdriver import Remote
from selenium.webdriver.common.by import By

from src.dto import LinkParseResponse, JobData
from src.services.clients import Logger


class LinkParseService:

    def __init__(self, driver: Remote, logger: Logger):
        self._driver = driver
        self._logger = logger

    @staticmethod
    def _extract_domain_name_(url: str) -> str:
        res = urlparse(url)
        domain_url = f'{res.scheme}://{res.netloc}'
        return domain_url

    def _build_bs_from_link(self, link: str) -> BeautifulSoup | None:
        try:
            self._driver.get(link)
            time.sleep(5)
            page_content = self._driver.page_source
            try:
                cookie_btn = self._driver.find_element(By.LINK_TEXT, 'Accept')
                if cookie_btn:
                    cookie_btn.click()
            except:
                pass
            time.sleep(5)
            soup = BeautifulSoup(page_content, 'html.parser')
            self._logger.log_info(f'LinkParseService get page content from: {link}')
            print('parsed link: ', {link})
            return soup
        except Exception as e:
            print('ERROR: parsed link: ', {link})
            self._logger.log_error(f'Driver get link: {link}: {str(e)}')

    @staticmethod
    def _extract_data_from_job_url_(domain_url: str, html: BeautifulSoup, job_name: str) -> Optional[JobData]:
        try:
            tag_list = html.find_all(string=re.compile(job_name))
            print('tag_list: ', tag_list)
            for tag in tag_list:
                tag_parents = tag.parents
                for parent in tag_parents:
                    a_tag = parent.find('a')
                    print('a_tag: ', a_tag)
                    if not a_tag:
                        continue
                    print('a_tag: ', a_tag)
                    search_result = re.search(job_name.lower(), a_tag.text.lower())
                    if not search_result:
                        continue
                    job_href = a_tag.get('href')
                    if not job_href:
                        continue
                    job_url = domain_url + job_href
                    return JobData(url=job_url, name=tag)
        except Exception as e:
            return None

    def _parse_src_link_(self, src_link: str, key_word_list: List[str]) -> List[LinkParseResponse]:
        html = self._build_bs_from_link(src_link)
        if not html:
            return []
        domain_url = self._extract_domain_name_(src_link)
        print(domain_url)
        out_data = []
        for key_word in key_word_list:
            job_data = self._extract_data_from_job_url_(domain_url, html, key_word)
            print('job_data: ', job_data, key_word)
            if not job_data:
                continue
            out_data.append(
                LinkParseResponse(
                    url=src_link,
                    job_name=job_data.name,
                    job_url=job_data.url
                )
            )
        return out_data

    def execute(self, src_link_list: List[str], key_word_list: List[str]) -> List[LinkParseResponse]:
        outputs = []
        for src_link in src_link_list:
            print('src_link: ', src_link)
            tmp_data = self._parse_src_link_(src_link, key_word_list)
            outputs += tmp_data
            time.sleep(random.uniform(1, 3))

        return outputs
