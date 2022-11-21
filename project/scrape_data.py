from selenium.webdriver import Chrome, Firefox
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from data.creds import net_id, password, COURSE_BOX, COURSE_MSG, COURSE_BTN, SIGN_UP_URL, HOME_URL
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
        self._incomplete_courses = {course:False for (course, complete) in courses.items() if not complete}
        # TODO: Registrate builds incomplete courses based off of the grades

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

        d.find_element(By.XPATH, '//*[@id="username"]').send_keys(net_id)
        d.find_element(By.XPATH, '//*[@id="password"]').send_keys(password)
        d.find_element(By.XPATH, '//*[@id="submit_button"]').click()

        for course in self._incomplete_courses:
            self._wait_for_element_by(By.CLASS_NAME, "searchbar-input")
            d.find_element(By.CLASS_NAME, "searchbar-input").send_keys(course)
            self._wait_for_element_by(By.XPATH, COURSE_BOX)
            d.find_element(By.XPATH, COURSE_BOX).click()
            
            i: int = 0
            while (True or i < 1000):
                i += 1
                if (self._search_in_page("Helaas")):
                    logging.info(f"You are not able to sign up for '{course}'")
                    break
                elif (self._search_in_page("Selecteer een toetsgelegenheid")):
                    logging.warning(f"Not implemented!")
                    break
                    # TODO: Implement if course is available
            self._refresh_course_page()
        logging.info("Completed scrape")

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


