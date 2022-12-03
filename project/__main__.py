import sys

if sys.version_info.major < 3 or sys.version_info.minor < 10:
    raise AssertionError(f"Python version 3.10 is required, you are running: {sys.version}")

from project.scraper import Scraper
from project.courses import Courses
from project.data.prefs import browser, notification_method
from project.utils import read_from_json, save_to_json, encode_string, create_webdriver
import logging
import argparse
import getpass
import subprocess
import time


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
    creds: dict[str] = read_from_json()

    if browser != "firefox" and browser != "chrome":
        raise ValueError("Browser preference must be firefox or chrome!")

    if "t" not in notification_method and "m" not in notification_method:
        raise ValueError("Notification preferences must contain 't', 'm' or both!")

    courses = Courses.create_courses_from_path("./project/courses.csv")
    if args["initial_setup"]:
        creds: dict[str] = {}
        logging.info("Running initial setup...")
        creds["net_id"]: str = input("Please input your TU Delft net id: ")
        net_pass: str = getpass.getpass("Please input the corresponding password (hidden): ")
        creds["net_pass"] = encode_string(net_pass)
        save_to_json(creds)
    if args["add_courses"] or args["initial_setup"]:
        logging.info("Adding courses...")
        courses.input_courses()
        courses.save()

    if not creds:
        raise ValueError("Credentials cannot be empty!")

    if "t" in notification_method:
        if creds.get("telegram_token", None) is None:
            print("You have selected Telegram as a notification method, no credentials for that have been found")
            telegram_token: str = input("Please enter your bot token (check README.md for help): ")
            creds["telegram_token"] = telegram_token
            save_to_json(creds)
        if creds.get("telegram_id", None) is None:
            logging.warning("Telegram is selected as a notification method, but no telegram_id is set!")
            print("Starting the telegram init, please register your ID by sending '/start' to the bot")
            telegram_init = subprocess.Popen([sys.executable, "-m" ,"project.telegram_init"])
            timeout, t = 300, 0
            while t < timeout:
                if read_from_json().get("telegram_id", None) is not None:
                    telegram_init.terminate()
                    break
                time.sleep(1)

    if "m" in notification_method:
        if creds.get("sender_mail", None) is None or\
           creds.get("receiver_mail", None) is None or\
           creds.get("mail_pass", None) is None:
            print("The sender email is logged into to send emails in case there are open sign ups")
            print("It is recommended you use an unimportant or dedicated script email")
            creds["sender_mail"]: str = input("Please input the sender email: ")
            print("The password has to be a google app password in the case of gmail:")
            print("https://support.google.com/accounts/answer/185833?hl=en")
            sender_pass: str = getpass.getpass("Please input the corresponding password: ")
            creds["mail_pass"] = encode_string(sender_pass)
            print("The receiver email is the email the sender sends the notifications to")
            print("This can be the same as the sender email")
            creds["receiver_mail"] = input("Please input the receiver email: ")
            save_to_json(creds)

    driver = create_webdriver(browser)
    scraper = Scraper(driver, courses)
    scraper.scrape_for_courses()
    scraper.notify(notification_method)

    logging.info("Script executed successfully!")
    if not args["quit"]:
        _ = input("Press any key to exit...")
