from utils import create_webdriver
from scrape_data import Scraper
from data.prefs import browser
import logging

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(name)s - %(message)s', level=logging.INFO)
    driver = create_webdriver(browser)

    scraper = Scraper(driver, {})
    scraper.scrape_for_courses()
    _ = input("Press any key to exit...")