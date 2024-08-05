import copy
import json
import os
import pickle
import time
import uuid
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from constants.station import stations
from constants.train_class import train_class
from utils.driver import get_driver
from utils.login import login
from utils.passenger_details import passenger_details
from utils.search_train import search_train

PICKLE_FILE = 'db.pkl'

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(GZipMiddleware)

templates = Jinja2Templates(directory="templates")


def return_saved_data():
    loaded_data = None
    try:
        if os.path.exists(PICKLE_FILE):
            with open(PICKLE_FILE, 'rb') as file:
                loaded_data = json.loads(pickle.load(file))
        return loaded_data if loaded_data is not None else []
    except Exception as e:
        print(e)
        return []


@app.get("/")
async def index(request: Request):
    loaded_data = return_saved_data()
    return templates.TemplateResponse("homepage.html", {'request': request, "stations": stations, 'train_class': train_class, 'loaded_data': loaded_data})


@app.get("/delete-data/{ID}", )
def delete_saved_data(request: Request, ID: str):
    loaded_data = return_saved_data()
    for d in loaded_data:
        if d['ID'] == ID:
            loaded_data.remove(d)
            with open(PICKLE_FILE, 'wb') as file:
                pickle.dump(json.dumps(loaded_data), file)
            break
    return {}


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
    loaded_data = return_saved_data()
    ld_copy = copy.deepcopy(loaded_data)
    with open(PICKLE_FILE, 'wb') as file:
        tmp = {
            'USER_NAME': USER_NAME,
            'USER_PASSWORD': USER_PASSWORD,
            'SOURCE_STATION': SOURCE_STATION,
            'DESTINATION_STATION': DESTINATION_STATION,
            'TRAVEL_DATE': TRAVEL_DATE,
            'TRAIN_NUMBER': TRAIN_NUMBER,
            'TRAIN_CLASS': TRAIN_CLASS,
            'PASSENGER_NAME': PASSENGER_NAME,
            'PASSENGER_AGE': PASSENGER_AGE,
            'PASSENGER_GENDER': PASSENGER_GENDER,
            'PASSENGER_BERTH_CHOICE': PASSENGER_BERTH_CHOICE,
            'PASSENGER_MOB_NO': PASSENGER_MOB_NO,
            'IS_TATKAL': IS_TATKAL,
        }
        for d in loaded_data:
            del d['ID']
            if d == tmp:
                break
        else:
            tmp['ID'] = str(uuid.uuid4())
            ld_copy.append(tmp)
        pickle.dump(json.dumps(ld_copy), file)

    driver = get_driver()
    driver.get('https://www.irctc.co.in/nget/train-search')

    TRAVEL_DATE = datetime.strptime(
        TRAVEL_DATE, "%Y-%m-%d").strftime("%d/%m/%Y")

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
