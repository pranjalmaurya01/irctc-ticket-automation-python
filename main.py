import time

from fastapi import FastAPI, Request
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import Field

from constants.station import stations
from constants.train_class import train_class
from utils.driver import get_driver
from utils.login import login
from utils.passenger_details import passenger_details
from utils.search_train import search_train

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(GZipMiddleware)

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("homepage.html", {'request': request, "stations": stations, 'train_class': train_class})


@app.get("/book-ticket")
def book_ticket(
    USER_NAME: str,
    USER_PASSWORD: str,
    SOURCE_STATION: str,
    DESTINATION_STATION: str,
    TRAVEL_DATE: str,
    TRAIN_NUMBER: str,
    TRAIN_CLASS: str,
    PASSENGER_NAME: str,
    PASSENGER_AGE: int,
    PASSENGER_GENDER: str,
    PASSENGER_BERTH_CHOICE: str,
    PASSENGER_MOB_NO: int,
    IS_TATKAL:  str | None = 'off',
):

    driver = get_driver()
    driver.get('https://www.irctc.co.in/nget/train-search')
    from datetime import datetime

    TRAVEL_DATE = datetime.strptime(
        TRAVEL_DATE, "%Y-%m-%d").strftime("%d/%m/%Y")
    print({'TRAVEL_DATE': TRAVEL_DATE})
    try:
        login(driver,
              USER_NAME,
              USER_PASSWORD)

        search_train(driver,
                     SOURCE_STATION,
                     DESTINATION_STATION,
                     IS_TATKAL,
                     TRAVEL_DATE,
                     TRAIN_NUMBER,
                     TRAIN_CLASS,)

        passenger_details(driver,
                          PASSENGER_NAME,
                          PASSENGER_AGE,
                          PASSENGER_GENDER,
                          PASSENGER_BERTH_CHOICE,
                          PASSENGER_MOB_NO,)
        time.sleep(120)
        driver.quit()
    except Exception as e:
        print(e)

    print("closing browser")
    return {"Hello": "World"}
