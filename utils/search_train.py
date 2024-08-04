import os
import re
import sys
import time
from datetime import datetime, timedelta

import pytz
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def search_train(driver: WebDriver):
    SRC = os.getenv('SOURCE_STATION')
    DEST = os.getenv('DESTINATION_STATION')
    IS_TATKAL = os.getenv('IS_TATKAL') == 1
    TRAVEL_DATE = os.getenv('TRAVEL_DATE')
    TRAIN_NUMBER = os.getenv('TRAIN_NUMBER')
    TRAIN_CLASS = os.getenv('TRAIN_CLASS')

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
    time.sleep(.5)
    input_source.send_keys(Keys.ENTER)

    input_dest = driver.find_element(
        By.CSS_SELECTOR, '#destination > span > input')
    input_dest.send_keys(DEST)
    time.sleep(.5)
    input_dest.send_keys(Keys.ENTER)

    if IS_TATKAL:
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
    try:
        submit_btn = driver.find_element(
            By.CSS_SELECTOR, "button[label='Find Trains'].search_btn.train_Search")
        submit_btn.click()
    except:
        pass
    # checking if navigation was complete "MODIFY SEARCH BUTTON"
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '.hidden-xs.search_btn.btn'))
        )
    except Exception as e:
        print("TIMEOUT: unable to search train", e)
        sys.exit()

    all_trains = driver.find_elements(
        By.CSS_SELECTOR, '.form-group.no-pad.col-xs-12.bull-back.border-all')

    for train in all_trains:
        if TRAIN_NUMBER in train.text:
            print(TRAIN_NUMBER, ": FOUND")
            classes = train.find_elements(
                By.CSS_SELECTOR, 'table td')
            for c in classes:
                if TRAIN_CLASS in c.text:
                    # print("found class ", c.text)
                    class_div = c.find_element(
                        By.CSS_SELECTOR, 'div')
                    class_div.click()
                    break

            else:
                print("TRAIN CLASS: NOT FOUND")
                sys.exit()

            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, 'table td div.AVAILABLE'))
                )
                available = train.find_element(
                    By.CSS_SELECTOR, 'table td div.AVAILABLE')
                print(available.text)
                available.click()
                prices = train.find_elements(
                    By.CSS_SELECTOR, 'strong')
                print(prices[-1].text)

                book_now_btn = train.find_element(
                    By.CSS_SELECTOR, '.btnDefault.train_Search.ng-star-inserted')
                book_now_btn.click()
            except Exception as e:
                print("NO TICKETS AVAILABLE", e)
                sys.exit()
            break
    else:
        print("TRAIN NUMBER: NOT FOUND")

    print("end searching train")
