from telegram.ext import Updater
from telegram.constants import ParseMode
from project.utils import read_from_json
from project.courses import Courses
from project.course import Course
import logging


class TelegramBot:
    """
    This class handles the notification sending after scraping has been completed.
    """
    def __init__(self, token, chat_id) -> None:
        """
        The initialiser method for the TelegramBot class.

        Args:
            token (_type_): This is the token provided by the user corresponding to a specific telegram bot. This can
                be sensitive.
            chat_id (_type_): The chat ID set during the initialisation for the telegram notification method. This
                is the chat the notification gets sent to.
        """
        self.token: str = token
        self.chat_id: str = chat_id
        self.updater: Updater = Updater(token=self.token, use_context=True)

    @property
    def token(self) -> str:
        return self.__token

    @token.setter
    def token(self, value) -> None:
        if value:
            self.__token = value
            return
        
        logging.warning("Telegram token provided is empty!")
        value = read_from_json().get("telegram_token", None)
        if value is None:
            raise ValueError("Token cannot be None! Make sure to set it or choose a different notification method")
        self.token = value

    @property
    def chat_id(self) -> str:
        return self._chat_id

    @chat_id.setter
    def chat_id(self, value):
        if value is None:
            raise ValueError("Chat ID cannot be None!")
        self._chat_id = value

    def send_notification(self, open_courses: Courses) -> None:
        """
        This method generates a notification based on the open_courses from the Scraper
        and sends it in a Markdown format to the provided chat (according to the chat_id).
        NOTE: Parentheses and other markdown symnols in the course name may result in the 
        markdown not parsing correctly and failing to send. Therefor it is recommended that
        you use both email and telegram.

        Args:
            open_courses (Courses): The open courses according to the results of the scrape. Provided
                in the Scraper class.
        """
        parse_mode: ParseMode = ParseMode.MARKDOWN_V2
        if open_courses.courses:
            body: str = f"The following courses are available for sign up:\n\n{open_courses}\n\n"+\
                         "Press [here](https://my.tudelft.nl/#/inschrijven/cursus/:id) to go"+\
                         " to the sign up page\n\n\-\-RegistrateTUD"
        else:
            body: str = "No open sign ups were found, you don't have to do anything."
        body = body.replace("(False)", "\(False\)")
        self.updater.bot.send_message(chat_id=self.chat_id, text=body, parse_mode=parse_mode)
