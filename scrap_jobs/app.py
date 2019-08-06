"""
This module import modules across the app and group them together to form a
specific function, e.g. run scraper
"""

from collections import OrderedDict
from time import sleep
from typing import Dict, List, NewType

import pandas as pd

from scrap_jobs.analysis.save import save_to_csv, save_to_excel
from scrap_jobs.scraper.jobstreet import JobStreetScraper

# type for scrapped job info's OrderedDict
JobDict = NewType('JobDict', Dict[str, List[str]])


class App:
    """Main app entry class. To be instantiate and used in __main__.py
    """

    @staticmethod
    def run_jobstreet_scraper(key: str, location: str = '') -> JobDict:
        """Run JobStreetScraper and obtain scrapped job info in Dictionary form

        Args:
            key (str): Search key
            location (str): Location of the job. Default to search for all
            locations if empty string is provided

        Returns:
            OrderedDict object containing organized information about the
            scrapped job data
        """
        scraper = JobStreetScraper(key, location)
        titles: List[str] = []
        company_names: List[str] = []
        locations: List[str] = []
        descriptions: List[str] = []
        details_page_links: List[str] = []
        next_page_link = ''

        # iterate over all pages
        while True:
            if next_page_link != '':
                scraper.url = next_page_link

            print(f'Scraping data from {scraper.url}...')
            html = scraper.request_site()
            soup = scraper.get_soup(html)
            panels = scraper.get_job_panels(soup)

            if not panels:
                raise Exception(
                    'Sorry, your search did not match any jobs.'
                    'Please try again with different keywords.')

            # add scrapped info to existing lists accordingly
            titles.extend(scraper.get_job_titles(panels))
            company_names.extend(scraper.get_job_company_names(panels))
            locations.extend(scraper.get_job_locations(panels))
            descriptions.extend(scraper.get_job_descriptions(panels))
            details_page_links.extend(
                scraper.get_job_details_page_links(panels)
            )

            # get next page anchor tag
            next_page_tag = soup.find(id="page_next")

            # break the loop if there is no more page can be found
            if next_page_tag is None:
                break

            next_page_link = next_page_tag.get('href')
            sleep(2.5)

        print('Done scraping...')

        # save scrapped results to OrderedDict
        jobs: Dict[str, List[str]] = OrderedDict()
        jobs['title'] = titles
        jobs['company_name'] = company_names
        jobs['location'] = locations
        jobs['description'] = descriptions
        jobs['details_page_link'] = details_page_links

        return JobDict(jobs)

    @staticmethod
    def convert_and_save_to_csv(jobs: JobDict) -> None:
        """Convert scrapped information in Dictionary form into DataFrame, then
        save it locally into csv file

        Args:
            jobs (Dict): Dictionary containing all the information scrapped
        """
        df = pd.DataFrame(columns=list(jobs.keys()))

        for key, value in jobs.items():
            df[key] = value

        save_to_csv(df, 'jobstreet.csv')

    @staticmethod
    def convert_and_save_to_excel(jobs: JobDict) -> None:
        """Convert scrapped information in Dictionary form into DataFrame, then
        save it locally into excel file

        Args:
            jobs (Dict): Dictionary containing all the information scrapped
        """
        df = pd.DataFrame(columns=list(jobs.keys()))

        for key, value in jobs.items():
            df[key] = value

        save_to_excel(df, 'jobstreet.xlsx')
