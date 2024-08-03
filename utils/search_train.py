import os
import time
from datetime import datetime, timedelta

import pytz
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By


def search_train(driver):
    SRC = os.getenv('SOURCE_STATION')
    DEST = os.getenv('DESTINATION_STATION')
    IS_TATKAL = os.getenv('IS_TATKAL')
    TRAVEL_DATE = os.getenv('TRAVEL_DATE')

    if IS_TATKAL:
        india_timezone = pytz.timezone('Asia/Kolkata')
        current_time_in_india = datetime.now(india_timezone)
        tomorrow_date_in_india = current_time_in_india + timedelta(days=1)

        TRAVEL_DATE = tomorrow_date_in_india.date().strftime("%d/%m/%Y")

    print("start searching train", SRC, "->", DEST,
          {'IS_TATKAL': IS_TATKAL, 'TRAVEL_DATE': TRAVEL_DATE})

    # MAIN CODE GOES HERE
    input_source = driver.find_element(
        By.CSS_SELECTOR, '#origin > span > input')
    input_source.send_keys(SRC)
    time.sleep(1)
    input_source.send_keys(Keys.ENTER)

    input_dest = driver.find_element(
        By.CSS_SELECTOR, '#destination > span > input')
    input_dest.send_keys(DEST)
    time.sleep(1)
    input_dest.send_keys(Keys.ENTER)

    input_tatkal = driver.find_element(
        By.CSS_SELECTOR, '#journeyQuota')
    input_tatkal.click()
    ActionChains(driver).send_keys("T").send_keys(Keys.ENTER).perform()

    input_doj = driver.find_element(
        By.CSS_SELECTOR, '#jDate > span > input')
    input_doj.send_keys(Keys.CONTROL + "a")
    input_doj.send_keys(Keys.DELETE)
    input_doj.send_keys(TRAVEL_DATE)

    # SUBMIT ENTIRE FORM
    input_doj.send_keys(Keys.ENTER)

    print("end searching train")
