"""
This module contains JobStreetScraper class to scrap jobstreet.com
"""

import sys
from typing import Dict, List, Optional

import requests
from bs4 import BeautifulSoup, ResultSet
from bs4.element import Tag
from requests import HTTPError, RequestException

from scrap_jobs.web.make_headers import make_headers


def is_beautiful_soup(value) -> None:
    """Check whether value is an instance of bs4 BeautifulSoup. Raise TypeError if not
    """
    if not isinstance(value, BeautifulSoup):
        raise TypeError(
            'Argument 1 provided must be an instance of bs4 BeautifulSoup')


def is_result_set(value) -> None:
    """Check whether value is an instance of bs4 ResultSet. Raise TypeError if not
    """
    if not isinstance(value, ResultSet):
        raise TypeError(
            'Argument 1 provided must be an instance of bs4 ResultSet')


class JobStreetScraper:
    """Web scraper to scrap available jobs via key supplied from jobstreet.com
    with BeautifulSoup

    Note:
    The scrap is aimed done politely without spamming too much requests per
    second which will probably violate the jobstreet.com policy
    """
    _default_locations = {
        'selangor': '51200',
        'penang': '50700',
        'kl': '50300',
        'melaka': '50500',
        'putrajaya': '51600'
    }
    _key: str
    _location: str
    _headers: Dict[str, str]
    _url: str

    @property
    def key(self) -> str:
        """Job search key
        """
        return self._key

    @key.setter
    def key(self, value: str):
        if not isinstance(value, str):
            raise TypeError('Key needs to be str')

        self._key = value

    @property
    def location(self) -> str:
        """Location of job
        """
        return self._location

    @location.setter
    def location(self, value: str):
        if not isinstance(value, str):
            raise TypeError('Location must be of type str')

        # raise error if location provided is not found in _default_locations
        if value != '' and \
           value not in self._default_locations.values():
            raise Exception('Location not supported')

        self._location = value

    @property
    def url(self) -> str:
        """Url to scrap
        """
        return self._url

    @url.setter
    def url(self, value: str):
        if not isinstance(value, str):
            raise TypeError('Url must be str')

        self._url = value

    @property
    def headers(self):
        """Headers to be sent together with GET request
        """
        return self._headers

    @headers.setter
    def headers(self, value):
        self._headers = value

    def __init__(self, key: str, location: str = '') -> None:
        """constructor

        Args:
            key (str): Key term to be searched by job street

            location (str): Location of job. If not provided, it defaults
            to get from all locations. Currently supported options:
                1) 51200: Selangor
                2) 50700: Penang
                3) 50300: Kuala Lumpur
                4) 50500: Melaka
                5) 51600: Putrajaya
        """
        self.key = key
        self.location = location
        self.headers = make_headers()

        self.url = 'https://www.jobstreet.com.my/en/job-search/job-vacancy.php?key=' + \
            self.key + \
            '&location=' + \
            self.location + \
            '&specialization=&area=&salary='

    def request_site(self) -> str:
        """Get HTML text response from the url provided in constructor

        Returns:
            HTML text response if request is success, else raise errors
        """
        res = requests.get(self.url, headers=self.headers)

        # catch error and exit if there is any error
        try:
            res.raise_for_status()
        except HTTPError:
            print('Encountered HTTP error when requesting to site. Please retry')
            sys.exit(1)
        except RequestException:
            print('Unexpected error from requests. Exiting...')
            sys.exit(1)

        # proceed to return obtained HTML page if no error encountered
        return res.text

    @staticmethod
    def get_soup(html_doc: str) -> BeautifulSoup:
        """Get BeautifulSoup instance with the HTML document's string

        Args:
            html_doc (str): HTML document text string

        Returns:
            BeautifulSoup instance created with the HTML string provided and lxml as parser
        """
        if not isinstance(html_doc, str):
            raise TypeError('Argument 1 provided must be a str')

        soup = BeautifulSoup(html_doc, 'lxml')
        return soup

    @staticmethod
    def get_job_panels(soup: BeautifulSoup) -> ResultSet:
        """Get job panels of jobstreet.com

        Args:
            soup: BeautifulSoup instance

        Returns:
            bs4's ResultSet containing job panels
        """
        is_beautiful_soup(soup)

        job_panels = soup.find_all('div', {
            'class': ['panel ', 'panel standout']
        })

        return job_panels

    @staticmethod
    def get_job_titles(result_set: ResultSet) -> List[str]:
        """Extract job title from the given result_set

        Returns:
            List containing job title strings
        """
        is_result_set(result_set)

        job_titles: List[str] = []

        for tag in result_set:
            link_tag: Tag = tag.find('a', class_='position-title-link')

            job_titles.append(link_tag.text if link_tag is not None else '')

        return job_titles

    @staticmethod
    def get_job_company_names(result_set: ResultSet) -> List[str]:
        """Extract job company name from the given result_set

        Returns:
            List containing job company name strings
        """
        is_result_set(result_set)

        company_names: List[str] = []

        for tag in result_set:
            link_tag: Tag = tag.find('a', class_='company-name')

            company_names.append(link_tag.text if link_tag is not None else '')

        return company_names

    @staticmethod
    def get_job_locations(result_set: ResultSet) -> List[str]:
        """Extract job location

        Returns:
            List containing job location strings
        """
        is_result_set(result_set)

        job_locations: List[str] = []

        for tag in result_set:
            li_tag: Tag = tag.find('li', class_="job-location")

            job_locations.append(li_tag.text if li_tag is not None else '')

        return job_locations

    @staticmethod
    def get_job_descriptions(result_set: ResultSet) -> List[str]:
        """Extract job description

        Returns:
            List containing job description strings
        """
        is_result_set(result_set)

        job_descriptions: List[str] = []

        for tag in result_set:
            ul_tag: Tag = tag.select_one('ul[id*="job_desc_detail"]')

            job_descriptions.append(ul_tag.text if ul_tag is not None else '')

        return job_descriptions

    @staticmethod
    def get_job_details_page_links(result_set: ResultSet) -> List[str]:
        """Extract job details page link from the job title anchor tag

        Returns:
            List containing job details page link
        """
        is_result_set(result_set)

        job_details_page_links: List[str] = []

        for tag in result_set:
            link_tag: Tag = tag.find('a', class_='position-title-link')

            job_details_page_links.append(
                link_tag.get('href')
                if link_tag is not None
                else ''
            )

        return job_details_page_links

    @staticmethod
    def get_next_page_link(soup: BeautifulSoup) -> Optional[str]:
        """Extract next page link from navigation panel

        Returns:
            Next page link if found, else None is returned
        """
        is_beautiful_soup(soup)

        a_tag: Tag = soup.find(id='page_next')

        return a_tag.get('href') if a_tag is not None else None
