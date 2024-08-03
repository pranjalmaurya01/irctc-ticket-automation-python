import time

from dotenv import load_dotenv

from utils.driver import get_driver
from utils.login import login
from utils.search_train import search_train


def main():
    load_dotenv()
    driver = get_driver()
    driver.get('https://www.irctc.co.in/nget/train-search')
    login(driver)
    search_train(driver)
    time.sleep(10)

    print("closing browser")
    driver.quit()


if __name__ == "__main__":
    main()
