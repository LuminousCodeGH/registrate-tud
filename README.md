# RegistrateTUD
A script that tracks which exams are open for you to register for and notifies you about them.

## Description

The aim of this project is, aside from a fun coding exercise, to be a useful tool for students at the TU Delft.
Since there is (as of november 2022) no way that I know of to get notified whether there are exams open 
or not for the courses in your curriculum, it is not uncommon for students to send an email in panic to their
professor a week before the exam asking to be registered for it, because they forgot to sign up. This script
checks exams for all of the courses a user has specified and notifies them if there are any open. 

The initial setup does require some work from the user in order to set the script up properly, but this should only
be needed once. A full guide on how to install this script can be seen in 'Installing'.

It is recommended that you put this script on a device that constantly runs in the background (such as a home server)
and schedule this script every so often with a random time delay (see 'Executing program'). That way you will passively 
get emails sent to you about which exams you should sign up to (NOTE: Use `-q` to instantly quit the script after 
its completion). However, how you use this script is up to you, it is still faster to run this script that 
to check manually which exams are available. Whether or not it is worth the effort of running the script is the question.

## Getting Started

### Dependencies

* Windows 10 (It should work on Win7 and Win11 too)
* Python 3.10+
* Libraries: see requirements.txt
* Chrome or Firefox
* A respective driver (NOTE: Driver version should not exceed the browser version)
    * Chrome:  https://chromedriver.storage.googleapis.com/index.html
    * Firefox: https://github.com/mozilla/geckodriver/releases

### Installing

#### Initial Setup

* Clone the repo `git clone https://github.com/LuminousCodeGH/RegistrateTUD.git`
* Install the respective webdriver and place it in ./project
* Configure the ./project/data/prefs.py
* Run the initial setup
    * On Windows: type `python.exe -m project.__main__.py -i` in the terminal or run init.cmd
    * On MacOS / Linux: type `python -m project.__main__.py -i` in the terminal (NOTE: MacOS / Linux not supported yet)

#### Telegram Setup

* Visit BotFather to create a new bot: https://telegram.me/BotFather
* Start the conversation using `/start` if you haven't talked to BotFather before
* Create a new bot using `/newbot` and by following the steps provided
* Copy the token (starting with the number sequence, ending after the string past the colon)
* Paste the token in ./project/data/prefs.py
* Do not forget to set the notification preference in ./project/data/prefs.py too!

### Executing program

#### Windows Standard

* Run run.cmd or type `python.exe -m project.__main__.py` in the terminal
    * In case you want to add courses after intial setup, use the `-a` or `--add_courses` argument

#### Windows Schedule

* Open 'Task Scheduler'
* Under 'Actions' press 'Create Basic Task'
* Configure the task to your liking, but consider the following:
    * Under trigger, it is recommended you add a random delay
    * Under actions, select 'Start a program' and point to schedule.cmd

## Help

* To get a list of arguments type `python.exe -m project.__main__.py -h` in the terminal
* In case of a `TimeoutException` while scraping, it is possible the credentials are incorrect. To fix this you can:
    * Rerun the init.cmd
    * Manually adjust the credentials in ./project/data/creds.json (NOTE: Passwords are base64 encoded)
* In case of a exception while sending the email, most likely the credentials are incorrect again. See bullet above
    * NOTE: Only sending from a Google mail has been tested, change `smtp_host` and `port` at your own risk
* In case of an error parsing Markdown in the `TelegramBot`, this is likely because one of the open courses contains characters that have functionality in Markdown. Remove them or select a different notification method.
    * A better fix might be implemented later.

## Future Implementations

* Integrate Telegram API for notifications as an alternative to sending an email
* Add support for Linux and MacOS and instructions on how to set the script up on the respective platform
* Implement marking courses as complete after the last exam has been passed

## Authors

This project is solely developed and maintained by Jacob Reaves

## License

Licensed under the GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007 - see the LICENSE file for details