import sys

if sys.version_info.major < 3 or sys.version_info.minor < 10:
    raise AssertionError(f"Python version 3.10 is required, you are running: {sys.version}")

from scraper import Scraper
from courses import Courses
from data.prefs import browser
import logging
import argparse
import utils
import getpass


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(name)s - %(message)s', level=logging.INFO)

    argparser = argparse.ArgumentParser(prog="RegistrateTUD", description="Get informed about upcoming exams!")
    argparser.add_argument("-a", "--add_courses", action="store_const", default=False,
                           help="Add courses to CSV file (default=False)", const=True)
    argparser.add_argument("-i", "--initial_setup", action="store_const", default=False,
                           help="Runs the program as if it were the first time", const=True)
    argparser.add_argument("-q", "--quit", action="store_const", default=False,
                           help="Quits the script instantly at the end, without waiting for input", const=True)
    args: dict[str] = vars(argparser.parse_args())

    if browser != "firefox" and browser != "chrome":
        raise ValueError("Browser must be firefox or chrome!")

    courses = Courses.create_courses_from_path("./courses.csv")
    if args["initial_setup"]:
        creds: dict[str] = {}
        logging.info("Running initial setup...")
        creds["net_id"]: str = input("Please input your TU Delft net id: ")
        net_pass: str = getpass.getpass("Please input the corresponding password (hidden): ")
        print("The sender email is logged into to send emails in case there are open sign ups")
        print("It is recommended you use an unimportant or dedicated script email")
        creds["sender_mail"]: str = input("Please input the sender email: ")
        print("The password has to be a google app password in the case of gmail:")
        print("https://support.google.com/accounts/answer/185833?hl=en")
        sender_pass: str = getpass.getpass("Please input the corresponding password: ")
        print("The receiver email is the email the sender sends the notifications to")
        print("This can be the same as the sender email")
        creds["receiver_mail"] = input("Please input the receiver email: ")
        creds["net_pass"] = utils.encode_string(net_pass)
        creds["mail_pass"] = utils.encode_string(sender_pass)
        utils.save_to_json(creds)
    if args["add_courses"] or args["initial_setup"]:
        logging.info("Adding courses...")
        courses.input_courses()
        courses.save()

    if not utils.read_from_json():
        raise ValueError("Credentials cannot be empty!")

    driver = utils.create_webdriver(browser)

    scraper = Scraper(driver, courses)
    scraper.scrape_for_courses()
    scraper.notify()
    if not args["quit"]:
        _ = input("Press any key to exit...")
