
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from api.irctc.captcha import review_journey_extract_solve_captcha

RETRIES = 3


def review_journey(driver: WebDriver):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".col-xs-push-5.progress-text"))
        )
        submit_btn = driver.find_element(
            By.CSS_SELECTOR, '.btnDefault.train_Search')
    except Exception as e:
        raise SystemError("NOT-FOUND: Review Journey") from e

    for _ in range(RETRIES):
        review_journey_extract_solve_captcha(driver)
        submit_btn.click()

        try:
            WebDriverWait(driver, 10).until(
                EC.invisibility_of_element_located(
                    (By.CSS_SELECTOR, '#preloaderP'))
            )
        except Exception as e:
            raise SystemError("TIMEOUT: REVIEW CAPTCHA REQUEST") from e

        try:
            driver.find_element(By.CSS_SELECTOR, '#captcha')
        except:
            break

    else:
        raise SystemError("REVIEW CAPTCHA RETRIES EXHAUSTED")

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.payment_opt'))
    )
    print("REVIEW JOURNEY COMPLETE")
