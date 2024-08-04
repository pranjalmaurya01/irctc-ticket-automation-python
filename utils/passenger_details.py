import os

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def passenger_details(driver: WebDriver):
    PASSENGER_NAME = os.getenv('PASSENGER_NAME')
    PASSENGER_AGE = os.getenv('PASSENGER_AGE')
    PASSENGER_GENDER = os.getenv('PASSENGER_GENDER')
    PASSENGER_BERTH_CHOICE = os.getenv('PASSENGER_BERTH_CHOICE')
    PASSENGER_MOB_NO = os.getenv('PASSENGER_MOB_NO')

    print("start filling in passenger details",
          PASSENGER_NAME, PASSENGER_AGE, PASSENGER_GENDER, PASSENGER_BERTH_CHOICE, PASSENGER_MOB_NO)

    try:
        input_passenger_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[placeholder='Passenger Name']"))
        )
        input_passenger_age = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[placeholder='Age']"))
        )
        input_passenger_gender = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "select[formcontrolname='passengerGender']"))
        )
        input_passenger_berth = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "select[formcontrolname='passengerBerthChoice']"))
        )
        input_passenger_mno = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[formcontrolname='mobileNumber']"))
        )

    except Exception as e:
        print(e)

    input_passenger_name.click()
    input_passenger_name.send_keys(PASSENGER_NAME)
    input_passenger_age.click()
    input_passenger_age.send_keys(PASSENGER_AGE)
    input_passenger_gender.click()
    input_passenger_gender.send_keys(PASSENGER_GENDER)
    input_passenger_berth.click()
    input_passenger_berth.send_keys(PASSENGER_BERTH_CHOICE)
    input_passenger_mno.click()
    input_passenger_mno.send_keys(PASSENGER_MOB_NO)

    payment_method_upi = driver.find_elements(
        By.CSS_SELECTOR, '.ui-radiobutton-box.ui-widget.ui-state-default')

    payment_method_upi[-1].click()

    btn_passenger_det_submit = driver.find_element(
        By.CSS_SELECTOR, 'button.train_Search.btnDefault')

    btn_passenger_det_submit.click()
