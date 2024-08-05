import os
import sys

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .captcha import extract_solve_captcha

RETRIES = 3


def login(driver: WebDriver, USER_NAME: str, USER_PASSWORD: str):
    print("attempting login")

    try:
        login_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '.search_btn.loginText.ng-star-inserted'))
        )

    except Exception as e:
        print("Error getting login btn timeout", e)
        sys.exit()

    login_btn.click()

    input_user_id = driver.find_element(
        By.CSS_SELECTOR, 'input[formcontrolname="userid"]')
    input_user_id.click()
    input_user_id.send_keys(USER_NAME)

    input_user_pass = driver.find_element(
        By.CSS_SELECTOR, 'input[formcontrolname="password"]')
    input_user_pass.click()
    input_user_pass.send_keys(USER_PASSWORD)

    for i in range(RETRIES):
        extract_solve_captcha(driver)

        try:
            login_err = driver.find_element(
                By.CSS_SELECTOR, '.loginError')
            if len(login_err.text):
                print(login_err.text)
                if login_err.text != 'Invalid Captcha....':
                    driver.quit()
            else:
                break
        except Exception:
            if i+1 == RETRIES:
                print("UNABLE TO SOLVE CAPTCHA")
                driver.quit()

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'a[href="/nget/logout"]'))
        )
    except:
        pass
    print("login success")
