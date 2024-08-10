import time

from selenium.webdriver.remote.webelement import WebElement


def slow_type(element: WebElement, text: str, delay=0.1):
    """Send a text to an element one character at a time with a delay."""

    for character in text:
        element.send_keys(character)
        time.sleep(delay)
