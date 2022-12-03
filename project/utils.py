from selenium.webdriver import Chrome, ChromeOptions, Firefox, FirefoxOptions
from project.data.prefs import browser_path
import logging
import base64
import json
import os


def create_webdriver(browser: str, is_headless=False) -> Chrome | Firefox | None:
    """
    Create a webdriver for use in the Scraper class. NOTE: In order for this to work you will have to download
    a version of the chrome or firefox webdriver. Check the README.md for steps on how to download and set it up.

    Args:
        browser (str, 'firefox' | 'chrome'): Select which browser the driver should use. NOTE: Chrome gives
            seemingly random warnings when using that driver, so Firefox is recommended. Though, so far there have not
            been any performance issues with Chrome despite the warnings.
        is_headless (bool, optional): Whether or not to hide the browser window when the driver
            is being run. Defaults to False.

    Returns:
        Chrome | Firefox | None: The driver which will be used for scraping. In case there is an error, returns None.
    """
    logging.info(f"Creating {browser} webdriver...")
    if browser != "chrome" and browser != "firefox":
        if browser == "":
            logging.error(f"Browser type 'browser' seems to be unset. Set it in ./data/prefs.py")
            return
        logging.error(f"Browser type '{browser}' not recognized. Did you set it correctly in data/prefs.py?")
        return
    try:
        if browser == "chrome":
            driver_options = ChromeOptions()
            driver_options.headless = is_headless
            driver = Chrome(executable_path="./project/chromedriver.exe", options=driver_options)
        elif browser == "firefox":
            driver_options = FirefoxOptions()
            driver_options.headless = is_headless
            driver_options.binary_location = browser_path
            driver = Firefox(executable_path="./project/geckodriver.exe", options=driver_options)
        return driver
    except Exception as e:
        # Catching WebDriverException is not allowed, which is what is called in this case. Hence 'Exception'...
        logging.error(e)
        return None


def encode_string(value: str) -> str:
    """
    Encodes a string to Base64 and returns it. Used to make passwords unreadable to a user.
    NOTE: While this adds a minimal layer of protection, this is not as secure as encryption at all, so do not rely
    on this to keep your passwords secure. It is merely intended to prevent people from looking at your screen and
    instantly knowing your passwords.

    Args:
        value (str): The string to encode.

    Returns:
        str: The Base64 encoded string.
    """
    value_bytes: bytes = value.encode('ascii')
    value_bytes = base64.b64encode(value_bytes)
    value_b64: str = value_bytes.decode('ascii')
    return value_b64


def decode_string(value_b64: str) -> str:
    """
    Decodes the Base64 encoded string and returns it.

    Args:
        value_b64 (str): The Base64 encoded string to decode.

    Returns:
        str: The decoded string.
    """
    value_b64_bytes: bytes = value_b64.encode('ascii')
    value_bytes: bytes = base64.b64decode(value_b64_bytes)
    value: str = value_bytes.decode('ascii')
    return value


def save_to_json(creds: dict[str], jpath="./project/data/creds.json") -> None:
    """
    Saves credentials to the creds.json.

    Args:
        creds (dict[str]): A dictionary with the user credentials. Passwords should be encoded before saving.
        jpath (str, optional): The file path to where to save the credentials. Defaults to "./data/creds.json".
    """
    with open(jpath, 'w') as f:
        json.dump(creds, f)


def read_from_json(jpath="./project/data/creds.json") -> dict[str]:
    """
    Read the user credentials from file or create an empty file in case such file does not exist.

    Args:
        jpath (str, optional): The file path to where the credentials are saved. Defaults to "./data/creds.json".

    Returns:
        dict[str]: A dictionary with all of the data read in the saved JSON file.
    """
    if not os.path.exists(jpath):
        save_to_json({})
        logging.warning("The creds.json file was not found, so an empty one was created!")
    with open(jpath) as f:
        creds: dict[str] = json.load(f)
    return creds
