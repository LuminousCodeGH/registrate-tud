from selenium.webdriver import Chrome, ChromeOptions, Firefox, FirefoxOptions
import logging


def create_webdriver(browser: str, is_headless=False) -> Chrome | Firefox | None:
    logging.info(f"Creating {browser} webdriver...")
    if browser != "chrome" and browser != "firefox":
        if (browser == ""):
            logging.error(f"Browser type 'browser' seems to be unset. Set it in ./data/prefs.py")
        logging.error(f"Browser type '{browser}' not recognized. Did you set it correctly in data/prefs.py?")
        return
    driver_options = ChromeOptions() if browser == "chrome" else FirefoxOptions()
    driver_options.headless = is_headless
    try:
        if (browser == "chrome"):
            driver = Chrome(executable_path="./chromedriver.exe", options=driver_options)
        else:
            driver = Firefox(executable_path="./geckodriver.exe", options=driver_options)
        return driver
    except Exception as e:
        # Catching WebDriverException is not allowed, which is what is called in this case. Hence 'Exception'...
        logging.error(e)
        return None