from utils import create_webdriver
from scrape_data import Scraper
from data.prefs import browser

if __name__ == "__main__":
    driver = create_webdriver(browser)

    scraper = Scraper(driver, {})
    scraper.scrape_for_courses()