"""
Main entry for scrap_jobs module. To be run from console
"""

from scrap_jobs.app import App
from scrap_jobs.scraper.jobstreet import JobStreetScraper

if __name__ == '__main__':
    key = input('Please input your search key: ')
    location = input(
        'Please enter your preferred location. Default to all if leave empty: '
    )
    scraper = JobStreetScraper(key, location)
    scrapped_job_info = App.run_jobstreet_scraper(key, location)
    App.convert_and_save_to_csv(scrapped_job_info)
    App.convert_and_save_to_excel(scrapped_job_info)
