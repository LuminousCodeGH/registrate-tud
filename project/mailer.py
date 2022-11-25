from data.creds import user_email, email_pass
from courses import Courses
import logging
import smtplib
import ssl

class Mailer:
    def __init__(self, target_email: str, user_email="", pw=""):
        self.target_email: str = target_email
        self.user_email = user_email
        self.email_pass = pw

    @property
    def user_email(self) -> str:
        return self._user_email

    @user_email.setter
    def user_email(self, value: str) -> None:
        if (not value):
            if (not user_email):
                raise ValueError("The email is empty, make sure to set it in ./data/prefs.py")
            value = user_email
        self._user_email = value

    @property
    def email_pass(self) -> None:
        logging.warning("Access to your password is prohibited!")

    @email_pass.setter
    def email_pass(self, value: str) -> None:
        if (not value):
            if (not email_pass):
                raise ValueError("The password is empty, make sure to set it in ./data/prefs.py")
            value = email_pass
        self.__email_pass = email_pass

    def setup_smtp(self, open_courses: Courses, port=465, smtp_host="smtp.gmail.com"):
        context = ssl.create_default_context()
        message: str = "\
            Subject: No open sign ups found!\
            No open sign ups were found, you don't have to do anything."

        try:
            with smtplib.SMTP_SSL(smtp_host, port, context=context) as server:
                server.login(self.user_email, self.__email_pass)
                if (open_courses):
                    message = f"\
                               Subject: Open courses available!\
                               The following courses are available for sign up:\n{open_courses}"
                    server.sendmail(self.user_email, self.target_email, message)
        except Exception as e:
            logging.error(f"An error occured while sending the email:\n{e}")