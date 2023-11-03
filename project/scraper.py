from selenium.webdriver import Chrome, Firefox
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from project.constants import SIGN_UP_URL, NO_COURSES_FOUND, CLOSED_SIGNUP, UNABLE_TO_SIGNUP, SIGNUP_AVAILABLE, NOT_IN_PROGRAM
from project.utils import read_from_json, decode_string
from project.courses import Courses
from project.mailer import Mailer
from project.telegram_bot import TelegramBot
import time
import logging


class Scraper:
    """
    This class scrapes the MyTUD website for courses that have open exam signups and stores them in a
    Courses object as a Course.
    """
    def __init__(self, driver: Chrome | Firefox, courses: Courses):
        """
        The initialiser method for the Scraper class.

        Args:
            driver (Chrome | Firefox): The webdriver the scraper should use when scraping. NOTE: Firefox is
                recommended since Chrome keeps on giving warnings. So far this has not impacted performance though.
            courses (Courses): A Courses object with all of the courses the user has specified they are following.
                Using this instance a list of available courses will be generated.
        """
        self.courses: Courses = courses
        self.driver: Chrome | Firefox = driver
        self.__available_courses: Courses = Courses([])
    
    def __exit__(self) -> None:
        """
        This method makes sure to kill the driver and release any resources it is hoarding when the script closes
        or crashes. No need to do anything with this.
        """
        if self.driver is not None:
            self.driver.quit()

    @property
    def courses(self) -> Courses:
        return self._courses

    @courses.setter
    def courses(self, courses: Courses) -> None:
        if not courses.courses:
            logging.warning("The 'courses' object is empty!")
        self._courses = courses
        self._incomplete_courses = courses.get_incomplete()
        # TODO: Registrate builds incomplete courses based off of the 'voortgang'

    @property
    def driver(self) -> Chrome | Firefox:
        return self.__driver

    @driver.setter
    def driver(self, driver: Chrome | Firefox) -> None:
        if not isinstance(driver, Chrome) and not isinstance(driver, Firefox):
            raise ValueError(f"Driver needs to be a Firefox or Chrome driver, not: '{type(driver)}'")
        self.__driver = driver

    def scrape_for_courses(self):
        """
        The main method of the Scraper class. This scrapes the MyTUD exam page for possible signups according to
        the courses the user has provided after logging in with the credentials the user provided for MyTUD.

            Step 1: Attempt to access the MyTUD website.
            Step 2: In case a new session is required (basically always), attempt login using user credentials.
            Step 3: Cycle through the incomplete courses and check if any signups are open.
            Step 4: Close the driver.
        """
        creds: dict[str] = read_from_json()
        d: Chrome | Firefox = self.driver
        d.get(SIGN_UP_URL)
        self._wait_for_element_by(By.XPATH, '//*[@id="submit_button"]')
        logging.info("Attempting login...")

        d.find_element(By.XPATH, '//*[@id="username"]').send_keys(creds["net_id"])
        d.find_element(By.XPATH, '//*[@id="password"]').send_keys(decode_string(creds["net_pass"]))
        d.find_element(By.XPATH, '//*[@id="submit_button"]').click()

        for course in self._incomplete_courses.courses:
            print("")
            logging.info(f"Searching for: {course}...")
            self._wait_for_element_by(By.CLASS_NAME, "searchbar-input")
            d.find_element(By.CLASS_NAME, "searchbar-input").send_keys(course.code)
            self._wait_until_in_page(NO_COURSES_FOUND, course.code, timeout=10)
            if self._search_in_page(NO_COURSES_FOUND):
                logging.info(f"'{course}' was not found, there is no sign up")
                d.refresh()
                continue
            elif self._search_in_page(CLOSED_SIGNUP):
                logging.info(f"The signup for '{course}' is closed")
                d.refresh()
                continue
            d.find_element(By.CSS_SELECTOR, ".osi-ion-item").click()
            
            i: int = 0
            while True or i < 6:
                i += 1
                if self._search_in_page(UNABLE_TO_SIGNUP):
                    logging.info(f"You are not able to sign up for '{course}'")
                    break
                elif self._search_in_page(SIGNUP_AVAILABLE):
                    logging.info(f"'{course}' is open for sign up!")
                    self.__available_courses.add(course)
                    break
                elif self._search_in_page(NOT_IN_PROGRAM):
                    logging.warning(f"'{course}' is not part of your default course program!")
                    break
                time.sleep(0.5)
            d.refresh()
        logging.info("Completed scrape!")
        d.close()

    def notify(self, method: str):
        """
        Attempts to send a notification to the user with the courses for which exams are open for sign up. 
        Multiple methods are possible by appending the method letter to the string in ./data/prefs.py.
            'm': Creates a Mailer object to send an email with to a user specified one.
            't': Creates a TelegramBot object to send a text to a chat, specified in the telegram init, using
                the token provided by the user.

        Args:
            method (str): User specified method of notification. Should be set in ./data/prefs.py.
        """
        if "m" in method:
            creds: dict[str] = read_from_json()
            logging.info(f"Sending email ({creds.get('sender_mail')} -> {creds.get('receiver_mail')})...")
            notifier = Mailer(creds["receiver_mail"], creds["sender_mail"], decode_string(creds["mail_pass"]))
            notifier.send_mail(self.__available_courses)
        
        if "t" in method:
            creds: dict[str] = read_from_json()
            logging.info(f"Sending Telegram to {creds.get('telegram_id')}...")
            notifier = TelegramBot(creds.get("telegram_token", None), creds.get("telegram_id", None))
            notifier.send_notification(self.__available_courses)

    def _wait_for_element_by(self, by: By, name: str, timeout=30) -> None:
        """
        Tells the driver to pause the script until a certain element is loaded in the page. WARNING: Sometimes
        WebDriverWait.until will trigger before the page has time to update causing the script to continue prematurely. 
        This is the case especially when using filters, so use _wait_until_in_page in those cases!

        Args:
            by (By): The method of pointing to a specific element. Usually XPATH, CSS_SELECTOR or CLASS_NAME.
            name (str): A string with the name or path to a specific element.
            timeout (int, optional): How many seconds to pause for before throwing an error. Defaults to 30.
        """
        try:
            element_present = ec.presence_of_element_located((by, name))
            WebDriverWait(self.driver, timeout).until(element_present)
        except TimeoutException:
            logging.warning(f"Timeout occurred after {timeout} seconds. Quitting...")
            self.driver.quit()
    
    def _search_in_page(self, text: str) -> bool:
        """
        Shortcut to run a JS command inside the driver to look for a string of text inside the HTML of the page. A
        more reliable way of looking for text in the page than using driver.page_source.

        Args:
            text (str): The string to look for inside of the HTML.

        Returns:
            bool: Whether the text has been found in the page or not.
        """
        return self.driver.execute_script(f'return document.body.innerHTML.includes("{text}")')

    def _wait_until_in_page(self, *texts: str, timeout=30.0) -> bool:
        """
        Waits until one of the specified strings is found in the page. Uses _search_in_page.

        Args:
            timeout (float, optional): How many seconds to wait before throwing an exception. Defaults to 30.0.

        Raises:
            TimeoutError: In case the timeout in seconds has been exceeded. Prevents infinite waits in case the
                page front-end changes.

        Returns:
            bool: Whether one of the phrases has been found in the page or not.
        """
        t: float = 0.0
        increment: float = 0.5
        complete: bool = False
        while t < timeout and not complete:
            for text in texts:
                complete = self._search_in_page(text)
                if complete:
                    break
            time.sleep(increment)
            t += increment
        if t >= timeout:
            raise TimeoutError(f"Could not find '{text}' in page!")
        return complete
