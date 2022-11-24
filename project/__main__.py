from utils import create_webdriver
from scraper import Scraper
from courses import Courses
from data.prefs import browser
import logging
import argparse

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(name)s - %(message)s', level=logging.INFO)

    argparser = argparse.ArgumentParser(prog="RegistrateTUD", description="Get informed about upcoming exams!")
    argparser.add_argument("-a", "--add_courses", action="store_const", default=False,
                           help="Add courses to CSV file (default=False)", const=True)
    args: dict[str] = vars(argparser.parse_args())

    courses = Courses.create_courses_from_path("./courses.csv")
    if (args["add_courses"]):
        courses.add_courses()
        courses.save()

    driver = create_webdriver("firefox")

    scraper = Scraper(driver, courses)
    scraper.scrape_for_courses()
    scraper.notify()
    _ = input("Press any key to exit...")