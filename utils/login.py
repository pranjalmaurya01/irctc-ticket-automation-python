import os
import sys
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .captcha import solve_captcha


def login(driver):
    print("attempting login")

    USER_NAME = os.getenv('USER_NAME')
    USER_PASSWORD = os.getenv('USER_PASSWORD')

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

    captcha_img = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'div.captcha_div > span.ng-star-inserted > img'))
    )

    captcha_src_base64 = captcha_img.get_attribute("src")

    captcha_txt = solve_captcha(captcha_src_base64)

    input_captcha = driver.find_element(
        By.CSS_SELECTOR, 'input[formcontrolname="captcha"]')
    input_captcha.click()
    input_captcha.send_keys(captcha_txt)

    time.sleep(1)
    submit_btn = driver.find_element(
        By.CSS_SELECTOR, 'div.modal-body > form > span > button')
    submit_btn.click()

    try:
        login_err = driver.find_element(
            By.CSS_SELECTOR, '.loginError')
        if len(login_err.text):
            print(login_err.text)

            if login_err.text == 'Invalid Captcha....':
                print("try captcha again")
            # elif login_err.text == 'Bad credentials':
            sys.exit()
    except Exception:
        pass

    print("login success")
