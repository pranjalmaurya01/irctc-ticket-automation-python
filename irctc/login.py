
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .captcha import extract_solve_captcha

# from api.config import logger


RETRIES = 3


def login(driver: WebDriver, USER_NAME: str, USER_PASSWORD: str):
    print("attempting login with %s", USER_NAME)

    try:
        login_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '.search_btn.loginText.ng-star-inserted'))
        )
    except Exception as e:
        print("LOGIN %s", e)
        raise SystemError("TIMEOUT: Login Button") from e

    login_btn.click()

    try:
        input_user_id = driver.find_element(
            By.CSS_SELECTOR, 'input[formcontrolname="userid"]')
        input_user_pass = driver.find_element(
            By.CSS_SELECTOR, 'input[formcontrolname="password"]')
        submit_btn = driver.find_element(
            By.CSS_SELECTOR, 'div.modal-body > form > span > button')
    except Exception as e:
        print("LOGIN %s", e)
        raise SystemError("NOT-FOUND: username & password") from e

    input_user_id.send_keys(USER_NAME)
    input_user_pass.send_keys(USER_PASSWORD)

    for i in range(RETRIES):
        extract_solve_captcha(driver)
        submit_btn.click()

        try:
            WebDriverWait(driver, 10).until(
                EC.invisibility_of_element_located(
                    (By.CSS_SELECTOR, '#preloaderP'))
            )
        except Exception as e:
            raise SystemError("TIMEOUT: LOGIN REQUEST") from e

        try:
            login_err = driver.find_element(
                By.CSS_SELECTOR, '.loginError')
        except Exception:
            print("login success for %s", USER_NAME)
            break

        print("login error text", login_err.text)
        if len(login_err.text):
            print("LOGIN ERROR MSG: %s, %s", USER_NAME, login_err.text)
            if login_err.text != 'Invalid Captcha....':
                raise SystemError(login_err.text)
            if i+1 == RETRIES:
                raise SystemError(f"RETRIES EXHAUSTED FOR {USER_NAME}")
        else:
            print("login success for %s", USER_NAME)
            break

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'a[href="/nget/logout"]'))
        )
    except Exception as e:
        raise SystemError("TIMEOUT: LOGOUT BUTTON") from e
