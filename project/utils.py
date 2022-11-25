from selenium.webdriver import Chrome, ChromeOptions, Firefox, FirefoxOptions
from data.prefs import browser_path
import logging
import base64
import json
import os


def create_webdriver(browser: str, is_headless=False) -> Chrome | Firefox | None:
    logging.info(f"Creating {browser} webdriver...")
    if browser != "chrome" and browser != "firefox":
        if (browser == ""):
            logging.error(f"Browser type 'browser' seems to be unset. Set it in ./data/prefs.py")
            return
        logging.error(f"Browser type '{browser}' not recognized. Did you set it correctly in data/prefs.py?")
        return
    try:
        if (browser == "chrome"):
            driver_options = ChromeOptions()
            driver_options.headless = is_headless
            driver = Chrome(executable_path="./chromedriver.exe", options=driver_options)
        elif (browser == "firefox"):
            driver_options = FirefoxOptions()
            driver_options.headless = is_headless
            driver_options.binary_location = browser_path
            driver = Firefox(executable_path="./geckodriver.exe", options=driver_options, )
        return driver
    except Exception as e:
        # Catching WebDriverException is not allowed, which is what is called in this case. Hence 'Exception'...
        logging.error(e)
        return None


def encode_string(value: str) -> str:
    value_bytes: bytes = value.encode('ascii')
    value_bytes = base64.b64encode(value_bytes)
    value_b64: str = value_bytes.decode('ascii')
    return value_b64


def decode_string(value_b64: str) -> str:
    value_b64_bytes: bytes = value_b64.encode('ascii')
    value_bytes: bytes = base64.b64decode(value_b64_bytes)
    value: str = value_bytes.decode('ascii')
    return value


def save_to_json(creds: dict[str], jpath="./data/creds.json") -> None:
    with open(jpath, 'w') as f:
        json.dump(creds, f)


def read_from_json(jpath="./data/creds.json") -> dict[str]:
    if (not os.path.exists(jpath)):
        raise FileNotFoundError(f"File '{jpath.split('/')[-1]}' was not found at path!")
    with open(jpath) as f:
        creds: dict[str] = json.load(f)
    return creds