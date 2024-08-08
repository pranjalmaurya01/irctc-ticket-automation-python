import uuid
from datetime import UTC, datetime, timedelta
from typing import Annotated

import starlette.status as status
from fastapi import APIRouter, Form, Request, Response
from fastapi.responses import HTMLResponse

from api.config import redis_main_db as rm_db
from api.config import templates
from api.utils import get_redis_user_key

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def get_login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {'request': request})


@router.post("/")
def login(request: Request, response: Response, username: Annotated[str, Form()], password: Annotated[str, Form()]):
    cookie = str(uuid.uuid4())
    r_key = get_redis_user_key(username)
    r_data = rm_db.json().get(r_key)

    if r_data:
        if r_data['USER_PASSWORD'] != password:
            return templates.TemplateResponse("auth/error.html", {'request': request, 'error': 'Invalid Credentials'})
        else:
            r_data['cookie'] = cookie
            rm_db.json().merge((r_key), '$', r_data)

    else:
        rm_db.json().set((r_key), '$', {
            'USER_PASSWORD': password, 'cookie': cookie})

    expires = datetime.now(UTC) + timedelta(hours=1)

    # update if dashboard url updates
    response.headers['HX-Redirect'] = '/dashboard'
    response.set_cookie('auth', f"{username}:{
                        cookie}", httponly=True, expires=expires)
    response.status_code = status.HTTP_302_FOUND
    return response


''' 
user:irctc_user_name -> {
    password: str
    cookie: str
}

'''
