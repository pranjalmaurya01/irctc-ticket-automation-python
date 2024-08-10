from typing import Annotated

import starlette.status as status
from fastapi import APIRouter, Depends, Form, HTTPException, Request, Response

from api.config import redis_main_db as rm_db
from api.config import templates
from api.dependency import cookie_dependency
from api.irctc.driver import get_driver
from api.irctc.login import login
from api.irctc.search_train import search_train
from api.utils import get_redis_user_key

from .constants import station, train_class

router = APIRouter(dependencies=[Depends(cookie_dependency)])


@router.get('/', name='get_dashboard_page')
def get_dashboard_page(request: Request, user=Depends(cookie_dependency)):
    return templates.TemplateResponse("dashboard/index.html", {'request': request, 'username': user['username']})


@router.get('/settings', name='get_settings_page')
def get_settings_page(request: Request, user=Depends(cookie_dependency)):
    return templates.TemplateResponse("dashboard/user_details_form.html", {'request': request,  'username': user['username'], 'user': user, "stations": station.STATIONS, 'train_class': train_class.train_class, })


@router.post('/settings', name='save_settings')
def save_settings(request: Request,
                  USER_PASSWORD: Annotated[str, Form()],
                  SOURCE_STATION: Annotated[str, Form()],
                  DESTINATION_STATION: Annotated[str, Form()],
                  TRAVEL_DATE: Annotated[str, Form()],
                  TRAIN_NUMBER: Annotated[str, Form()],
                  TRAIN_CLASS: Annotated[str, Form()],
                  PASSENGER_NAME: Annotated[str, Form()],
                  PASSENGER_AGE: Annotated[str, Form()],
                  PASSENGER_GENDER: Annotated[str, Form()],
                  PASSENGER_BERTH_CHOICE: Annotated[str, Form()],
                  PASSENGER_MOB_NO: Annotated[str, Form()],
                  IS_TATKAL:  Annotated[str, Form()] = 'off',
                  user=Depends(cookie_dependency)):

    user_k = get_redis_user_key(user['username'])

    tmp_d = {
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

    rm_db.json().merge((user_k), '$', tmp_d)

    tmp_d['username'] = user['username']

    return templates.TemplateResponse("dashboard/user_details_form.html", {'request': request,  'username': user['username'], 'user': tmp_d, "stations": station.STATIONS, 'train_class': train_class.train_class, 'saved': True})


@router.post('/book_ticket', name='book_ticket')
def book_ticket(request: Request, user=Depends(cookie_dependency)):
    driver = get_driver()
    err = ''
    try:
        driver.get('https://www.irctc.co.in/nget/train-search')

        try:
            # login(driver, user['username'], user['USER_PASSWORD'])
            search_train(driver,
                         user['SOURCE_STATION'],
                         user['DESTINATION_STATION'],
                         user['IS_TATKAL'],
                         user['TRAVEL_DATE'],
                         user['TRAIN_NUMBER'],
                         user['TRAIN_CLASS']
                         )
        except SystemError as e:
            err = str(e)

    finally:
        driver.quit()

    return err
