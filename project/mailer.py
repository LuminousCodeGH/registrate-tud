from project.courses import Courses
import logging
import smtplib
import ssl


class Mailer:
    """
    This class handles the email sending using smtplib. The default settings are setup to work with gmail.
    """
    def __init__(self, receiver_email: str, sender_email="", pw=""):
        """
        The initialiser method for the Mailer class.

        Args:
            receiver_email (str): The email address that receives a notification.
            sender_email (str, optional): The email that sends the notification, currently setup to
                work with gmail buy default. Defaults to "".
            pw (str, optional): The password for the sender email. Should not be accessed from
                outside of the class. Defaults to "".
        """
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
        logging.warning("Your password should not be accessed!")

    @email_pass.setter
    def email_pass(self, value: str) -> None:
        if not value:
            raise ValueError("The password is empty, make sure to set it using 'python __main__.py -i'")
        self.__email_pass = value

    def send_mail(self, open_courses: Courses, port=465, smtp_host="smtp.gmail.com"):
        """
        Sends emails to the receiver_email from the sender_email using smtplib. If there are courses open
        for sign up, it will send a list with those courses. Otherwise, it will notify you you don't have to
        do anything. To set up a custom smtp_host and port, look up the respective SMTP server and port(s).

        Args:
            open_courses (Courses): A Courses object with all courses that have open signups. Generated automatically.
            port (int, optional): The SMTP port for the SMTP host. Defaults to 465.
            smtp_host (str, optional): The SMTP server that the email gets sent through. Defaults to "smtp.gmail.com".
        """
        context = ssl.create_default_context()
        subject: str = "No open sign ups found!"
        body: str = "No open sign ups were found, you don't have to do anything."

        try:
            with smtplib.SMTP_SSL(smtp_host, port, context=context) as server:
                server.login(self.sender_email, self.__email_pass)
                if open_courses.courses:
                    subject = "Open courses available!"
                    body = f"The following courses are available for sign up:\n{open_courses}\n\n\n--RegistrateTUD"
                msg: str = f"Subject: {subject}\n\n{body}"
                server.sendmail(self.sender_email, self.receiver_email, msg)
        except Exception as e:
            logging.error(f"An error occurred while sending the email:\n{e}")