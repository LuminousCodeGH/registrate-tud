from selenium.webdriver import Chrome, Firefox
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from data.creds import net_id, password
from constants import COURSE_BOX, COURSE_BTN, SIGN_UP_URL, HOME_URL
from courses import Courses
from course import Course
import time
import logging


class Scraper:
    def __init__(self, driver: Chrome | Firefox, courses: Courses):
        self.courses: Courses = courses
        self.driver: Chrome | Firefox = driver
        self.__available_courses: list[Course] = []
    
    def __exit__(self) -> None:
        if (self.driver != None):
            self.driver.quit()

    @property
    def courses(self) -> Courses:
        return self._courses

    @courses.setter
    def courses(self, courses: Courses) -> None:
        if (not courses.courses):
            logging.warning("The 'courses' object is empty!")
        self._courses = courses
        self._incomplete_courses = courses.get_incomplete()
        # TODO: Registrate builds incomplete courses based off of the 'voortgang'

    @property
    def driver(self) -> Chrome | Firefox:
        return self.__driver

    @driver.setter
    def driver(self, driver: Chrome | Firefox) -> None:
        if (not isinstance(driver, Chrome) and not isinstance(driver, Firefox)):
            raise ValueError(f"Driver needs to be a Firefox or Chrome driver, not: '{type(driver)}'")
        self.__driver = driver

    def scrape_for_courses(self):
        d: Chrome | Firefox = self.driver
        d.get("https://my.tudelft.nl/#/inschrijven/cursus/:id")
        self._wait_for_element_by(By.XPATH, '//*[@id="submit_button"]')
        logging.info("Attempting login...")

        d.find_element(By.XPATH, '//*[@id="username"]').send_keys(net_id)
        d.find_element(By.XPATH, '//*[@id="password"]').send_keys(password)
        d.find_element(By.XPATH, '//*[@id="submit_button"]').click()

        for course in self._incomplete_courses.courses:
            logging.info(f"Searching for: {course}")
            self._wait_for_element_by(By.CLASS_NAME, "searchbar-input")
            d.find_element(By.CLASS_NAME, "searchbar-input").send_keys(course.code)
            time.sleep(0.5)  # Sometimes the filter does not have time to filter and the first course box gets clicked
            if (self._search_in_page("Geen zoekresultaten")):
                logging.info(f"'{course}' was not found, there is no sign up")
                d.refresh()
                continue
            self._wait_for_element_by(By.XPATH, COURSE_BOX)
            d.find_element(By.XPATH, COURSE_BOX).click()
            
            i: int = 0
            while (True or i < 6):
                i += 1
                if (self._search_in_page("Helaas")):
                    logging.info(f"You are not able to sign up for '{course}'")
                    break
                elif (self._search_in_page("Selecteer een toetsgelegenheid")):
                    logging.info(f"'{course}' is open for sign up!")
                    self.__available_courses.append(course)
                    break
                time.sleep(0.5)
            d.refresh()
        logging.info("Completed scrape!")
        d.close()

    def notify(self, method="mail"):
        if (method == "mail"):
            logging.info("Sending email!")
            print(self.__available_courses)

    def _wait_for_element_by(self, by: By, name: str, timeout=30) -> None:
        try:
            element_present = EC.presence_of_element_located((by, name))
            WebDriverWait(self.driver, timeout).until(element_present)
        except TimeoutException:
            logging.warning(f"Timeout occurred after {timeout} seconds. Quitting...")
            self.driver.quit()
    
    def _search_in_page(self, text) -> bool:
        return self.driver.execute_script(f'return document.body.innerHTML.includes("{text}")')

    def _refresh_course_page(self) -> None:
        self.driver.get(HOME_URL)
        self._wait_for_element_by(By.XPATH, COURSE_BTN)
        self.driver.get(SIGN_UP_URL)


