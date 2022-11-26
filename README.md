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
get emails sent to you about which exams you should sign up to. NOTE: Use -q to instantly quit the script after 
its completion. However, how you use this script is up to you, it is still faster to run this script that 
to check manually which exams are available. Whether or not it is worth the effort of running the script is the question.

## Getting Started

### Dependencies

* Windows 10 (It should work on Win7 and Win11 too)
* Python 3.10+
* Libraries: see requirements.txt
* Chrome or Firefox
* A respective driver (NOTE: Driver version should match the browser version)
    * Chrome:  https://chromedriver.storage.googleapis.com/index.html
    * Firefox: https://github.com/mozilla/geckodriver/releases