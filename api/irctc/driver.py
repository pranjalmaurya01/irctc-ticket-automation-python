from fake_useragent import UserAgent
from selenium import webdriver


def get_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--window-size=1400,1400")
    chrome_options.add_argument("--disable-notifications")
    user_agent = UserAgent().random
    chrome_options.add_argument(f"user-agent={user_agent}")
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")
    chrome_options.add_argument(
        "--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=chrome_options)
    return driver
