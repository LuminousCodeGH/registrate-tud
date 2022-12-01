from selenium.webdriver import Chrome, Firefox
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from constants import COURSE_BTN, SIGN_UP_URL, HOME_URL
from utils import read_from_json, decode_string
from courses import Courses
from mailer import Mailer
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
        """
        creds: dict[str] = read_from_json()
        d: Chrome | Firefox = self.driver
        d.get("https://my.tudelft.nl/#/inschrijven/toets/:id")
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
            self._wait_until_in_page("Geen zoekresultaten", course.code, timeout=10)
            if self._search_in_page("Geen zoekresultaten"):
                logging.info(f"'{course}' was not found, there is no sign up")
                d.refresh()
                continue
            d.find_element(By.CSS_SELECTOR, ".osi-ion-item").click()
            
            i: int = 0
            while True or i < 6:
                i += 1
                if self._search_in_page("Helaas"):
                    logging.info(f"You are not able to sign up for '{course}'")
                    break
                elif self._search_in_page("Selecteer een toetsgelegenheid"):
                    logging.info(f"'{course}' is open for sign up!")
                    self.__available_courses.add(course)
                    break
                elif self._search_in_page("geen deel uit van het vaste deel van je examenprogramma"):
                    logging.warning(f"'{course}' is not part of your default course program!")
                    break
                time.sleep(0.5)
            d.refresh()
        logging.info("Completed scrape!")
        d.close()

    def notify(self, method="mail"):
        """
        Attempts to send a notification to the user with the courses for which exams are open for sign up. So
        far, only notifying by mail has been implemented.
            'mail': Creates a Mailer object to send an email with to a user specified one.
            'telegram': Not implemented.
        TODO: Integrate the Telegram API to work as a notification method.

        Args:
            method (str, optional): User specified method of notification. Defaults to "mail" since this is the
                only method implemented so far.
        """
        if method == "mail":
            logging.info("Sending email!")
            creds: dict[str] = read_from_json()
            notifier = Mailer(creds["receiver_mail"], creds["sender_mail"], decode_string(creds["mail_pass"]))
            notifier.send_mail(self.__available_courses)

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

    def _refresh_course_page(self) -> None:
        """
        Shortcut to refresh the course page. In the case of the course page driver.refresh doesn't work because
        the page URL doesn't change after selecting a course.
        """
        self.driver.get(HOME_URL)
        self._wait_for_element_by(By.XPATH, COURSE_BTN)
        self.driver.get(SIGN_UP_URL)


