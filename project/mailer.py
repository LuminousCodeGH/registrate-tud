from courses import Courses
import logging
import smtplib
import ssl


class Mailer:
    def __init__(self, receiver_email: str, sender_email="", pw=""):
        self.receiver_email: str = receiver_email
        self.sender_email: str = sender_email
        self.email_pass: str = pw

    @property
    def sender_email(self) -> str:
        return self._user_email

    @sender_email.setter
    def sender_email(self, value: str) -> None:
        if not value:
            raise ValueError("The email is empty, make sure to set it using 'python __main__.py -i'")
        self._user_email = value

    @property
    def email_pass(self) -> None:
        logging.warning("Access to your password is prohibited!")

    @email_pass.setter
    def email_pass(self, value: str) -> None:
        if not value:
            raise ValueError("The password is empty, make sure to set it using 'python __main__.py -i'")
        self.__email_pass = value

    def send_mail(self, open_courses: Courses, port=465, smtp_host="smtp.gmail.com"):
        context = ssl.create_default_context()
        subject: str = "No open sign ups found!"
        body: str = "No open sign ups were found, you don't have to do anything."

        try:
            with smtplib.SMTP_SSL(smtp_host, port, context=context) as server:
                server.login(self.sender_email, self.__email_pass)
                if open_courses:
                    subject = "Open courses available!"
                    body = f"The following courses are available for sign up:\n{open_courses}\n\n\n--RegistrateTUD"
                msg: str = f"Subject: {subject}\n\n{body}"
                server.sendmail(self.sender_email, self.receiver_email, msg)
        except Exception as e:
            logging.error(f"An error occurred while sending the email:\n{e}")