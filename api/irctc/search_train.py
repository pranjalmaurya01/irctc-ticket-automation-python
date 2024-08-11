import time
from datetime import datetime, timedelta

import pytz
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .utils import slow_type

# SCREENSHOT_PATH = '/static/screenshot'


def search_train(driver: WebDriver,
                 SOURCE_STATION: str,
                 DESTINATION_STATION: str,
                 IS_TATKAL: str,
                 TRAVEL_DATE: str | None,
                 TRAIN_NUMBER: str,
                 TRAIN_CLASS: str,):

    SRC = SOURCE_STATION
    DEST = DESTINATION_STATION
    IS_TATKAL = IS_TATKAL == 'on'

    if IS_TATKAL:
        india_timezone = pytz.timezone('Asia/Kolkata')
        current_time_in_india = datetime.now(india_timezone)
        tomorrow_date_in_india = current_time_in_india + timedelta(days=1)

        TRAVEL_DATE = tomorrow_date_in_india.date().strftime("%d/%m/%Y")
    elif TRAVEL_DATE is None:
        raise SystemError("TRAVEL_DATE: REQUIRED")

    print("start searching train", SRC, "->", DEST,
          {'IS_TATKAL': IS_TATKAL, 'TRAVEL_DATE': TRAVEL_DATE})

    try:
        input_source = driver.find_element(
            By.CSS_SELECTOR, '#origin > span > input')
        input_dest = driver.find_element(
            By.CSS_SELECTOR, '#destination > span > input')
        input_tatkal = driver.find_element(
            By.CSS_SELECTOR, '#journeyQuota div')
        input_doj = driver.find_element(
            By.CSS_SELECTOR, '#jDate > span > input')
        submit_btn = driver.find_element(
            By.CSS_SELECTOR, "button[label='Find Trains'].search_btn.train_Search")
    except Exception as e:
        print("LOGIN %s", e)
        raise SystemError("NOT-FOUND: source | dest | tatkal | doj") from e

    actions = ActionChains(driver)
    actions.move_to_element(submit_btn).perform()

    # MAIN CODE GOES HERE
    slow_type(input_source, SRC)
    time.sleep(.2)
    # select the first option from custom dropdown
    for _ in range(5):
        actions.send_keys(Keys.UP).perform()
    input_source.send_keys(Keys.ENTER)

    slow_type(input_dest, DEST)
    time.sleep(.2)
    # select the first option from custom dropdown
    for _ in range(5):
        actions.send_keys(Keys.UP).perform()
    input_dest.send_keys(Keys.ENTER)

    if IS_TATKAL:
        input_tatkal.click()
        actions.send_keys("T").send_keys(Keys.ENTER).perform()

    input_doj.send_keys(Keys.CONTROL + "a")
    input_doj.send_keys(Keys.DELETE)
    input_doj.send_keys(TRAVEL_DATE)

    # SUBMIT ENTIRE FORM
    try:
        input_doj.send_keys(Keys.ENTER)
        submit_btn.click()
    except Exception:
        pass

    # checking if navigation was complete "MODIFY SEARCH BUTTON"
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '.hidden-xs.search_btn.btn'))
        )
    except Exception as e:
        raise SystemError("TIMEOUT: unable to search train") from e

    all_trains = driver.find_elements(
        By.CSS_SELECTOR, '.form-group.no-pad.col-xs-12.bull-back.border-all')

    count = 0
    for train in all_trains:
        if TRAIN_NUMBER in train.text:
            classes = train.find_elements(
                By.CSS_SELECTOR, 'table td')
            for c in classes:
                if TRAIN_CLASS in c.text:
                    class_div = c.find_element(
                        By.CSS_SELECTOR, 'div')
                    class_div.click()
                    break

            else:
                raise SystemError("TRAIN CLASS: NOT FOUND")

            try:
                # wait for 10 seconds for loading of selected class
                WebDriverWait(driver, 10).until(
                    EC.invisibility_of_element_located(
                        (By.CSS_SELECTOR, '#preloaderP'))
                )
            except Exception as e:
                raise SystemError("TIMEOUT: Something") from e

            # refresh elements
            all_trains_refreshed = driver.find_elements(
                By.CSS_SELECTOR, '.form-group.no-pad.col-xs-12.bull-back.border-all')
            selected_train = all_trains_refreshed[count]
            # scroll the selected train into view
            driver.execute_script(
                "arguments[0].scrollIntoView(false);", selected_train)
            selected_train.screenshot(
                f"{TRAIN_NUMBER}-{TRAIN_CLASS}.png")

            try:
                available = selected_train.find_element(
                    By.CSS_SELECTOR, 'table td div.AVAILABLE')
                available.click()
                prices = train.find_elements(
                    By.CSS_SELECTOR, 'strong')

                print(prices[-1].text)

                book_now_btn = train.find_element(
                    By.CSS_SELECTOR, '.btnDefault.train_Search.ng-star-inserted')
                book_now_btn.click()
            except Exception as e:
                raise SystemError(f"NO TICKETS AVAILABLE in {
                    TRAIN_NUMBER} for {TRAIN_CLASS}") from e
            break
        count += 1
    else:
        raise SystemError("TRAIN NUMBER: NOT FOUND")

    # let the toast render on screen
    time.sleep(.5)
    # check if any error is raised in toast
    err = ''
    try:
        toast = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '.ui-toast-detail'))
        )
        err = toast.text
    except Exception:
        pass
    if err:
        raise SystemError(err)

    try:
        # .ui-button-icon-left.ui-clickable.pi.pi-check
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '.hidden-xs.search_btn.btn'))
        )
    except Exception as e:
        raise SystemError(f"TIMEOUT: Submit of {
                          TRAIN_NUMBER} for {TRAIN_CLASS}") from e
    print("end searching train")
