from platform import system


browser: str = "firefox"     # Put desired browser ('chrome' or 'firefox') here

match system():              # Put browser executable files here for your system in case of errors
    case "Windows":
        browser_path: str = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
    case "Linux":
        browser_path: str = "/snap/bin/firefox"

browser_profile: str = ""

notification_method: str = "m"  # Put desired method(s) here ('m' for email, 't' for 'telegram')
