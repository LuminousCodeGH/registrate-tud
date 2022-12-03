from telegram.ext import Updater
from telegram import ParseMode
from project.utils import read_from_json
from project.courses import Courses
from project.course import Course
import logging


class TelegramBot:
    def __init__(self, token, chat_id) -> None:
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
        parse_mode: ParseMode = ParseMode.MARKDOWN_V2
        if open_courses.courses:
            body: str = f"The following courses are available for sign up:\n\n{open_courses}\n\n"+\
                         "Press [here](https://my.tudelft.nl/#/inschrijven/cursus/:id) to go"+\
                         " to the sign up page\n\n\-\-RegistrateTUD"
        else:
            body: str = "No open sign ups were found, you don't have to do anything."
        body = body.replace("(False)", "\(False\)")
        self.updater.bot.send_message(chat_id=self.chat_id, text=body, parse_mode=parse_mode)
