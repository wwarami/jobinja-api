import json
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

JOBINJA_LOGIN_URL = 'https://jobinja.ir/login/user'
COOKIES_FILE = 'config/cookies.json'


def get_cookie(email: str, password: str):
    driver = webdriver.Firefox()
    driver.get(JOBINJA_LOGIN_URL)

    # find email and password fields based on their XPATH
    email_field = driver.find_element(By.XPATH, '//*[@id="identifier"]')
    password_field = driver.find_element(By.XPATH, '//*[@id="password"]')

    # fill email and password fields
    email_field.send_keys(email)
    password_field.send_keys(password)

    # locate and submit the form
    submit = driver.find_element(By.XPATH, '/html/body/div/div/div[1]/form/div[2]/div/input[4]')
    submit.click()

    # try to get success login message and check if we are logged in correctly.
    try:
        driver.find_element(By.XPATH, '/html/body/div/header/div[2]/div')
    except NoSuchElementException:
        # handle not found element error and returning user info
        print("You're email address or password is wrong!\n \
        Recheck them please.")
        sys.exit()
    else:
        # return the cookie
        print('We got the cookies successfully!')
        return driver.get_cookies()
    finally:
        # close the driver
        driver.close()


def save_cookies(cookies, path=COOKIES_FILE):
    # save cookies in a json file
    try:
        with open(path, 'w') as file:
            json.dump(cookies, file)
    except Exception as error:
        print(f"Something went wrong while saving the cookies :(\n\
              error: {error}")
    else:
        print(f"Cookies saved successfully.\nPath: {path}")



