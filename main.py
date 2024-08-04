import time

from dotenv import load_dotenv

from utils.driver import get_driver
from utils.login import login
from utils.passenger_details import passenger_details
from utils.search_train import search_train


def main():
    load_dotenv()
    driver = get_driver()
    driver.get('https://www.irctc.co.in/nget/train-search')
    login(driver)
    search_train(driver)
    passenger_details(driver)
    time.sleep(30)

    print("closing browser")
    driver.quit()


if __name__ == "__main__":
    main()
