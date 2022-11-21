from selenium.webdriver import Chrome, Firefox
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from data.creds import net_id, password, COURSE_URL, COURSE_SEARCH
import logging

class Scraper:
    def __init__(self, driver: Chrome | Firefox, courses: dict[bool]):
        self.courses: dict[bool] = courses
        self.driver: Chrome | Firefox = driver
    
    def __exit__(self) -> None:
        if (self.driver != None):
            self.driver.quit()

    @property
    def courses(self) -> dict[bool]:
        return self._courses

    @courses.setter
    def courses(self, courses: dict[bool]) -> None:
        if (not courses):
            logging.warning("The courses dict is empty")
        self._courses = courses
        self._incomplete_courses = {course:False for (course, complete) in courses if not complete}

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
        d.get(COURSE_URL)
        self._wait_for_element_by(By.XPATH, '//*[@id="submit_button"]')

        d.find_element(By.XPATH, '//*[@id="username"]').send_keys(net_id)
        d.find_element(By.XPATH, '//*[@id="password"]').send_keys(password)
        d.find_element(By.XPATH, '//*[@id="submit_button"]').click()

        self._wait_for_element_by(By.XPATH, COURSE_SEARCH)

    def _wait_for_element_by(self, by: By, name: str, timeout=30):
        try:
            element_present = EC.presence_of_element_located((by, name))
            WebDriverWait(self.driver, timeout).until(element_present)
        except TimeoutException:
            print(logging.warning(f"Timeout occurred after {timeout} seconds"))
            self.driver.quit()


