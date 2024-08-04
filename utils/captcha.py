import base64
import os
import subprocess
import sys
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

CAPTCHA_FILE_NAME = 'tmp-captcha.png'


def extract_solve_captcha(driver):
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


def solve_captcha(captcha_src_base64: str, method='GOCR') -> str:
    base64_img = captcha_src_base64.split(',')[1]
    img_data = base64.b64decode(base64_img)
    with open(CAPTCHA_FILE_NAME, 'wb') as f:
        f.write(img_data)

    try:
        result = subprocess.run(['gocr', CAPTCHA_FILE_NAME],
                                capture_output=True, text=True, check=True)
        captcha_txt = result.stdout.strip()
        os.remove(CAPTCHA_FILE_NAME)
        return captcha_txt
    except Exception as e:
        print("GOCR not found on system please install to continue", e)
        sys.exit()