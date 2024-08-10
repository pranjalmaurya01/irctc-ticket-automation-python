from fastapi import HTTPException, Request

from api.config import redis_main_db as rm_db
from api.utils import get_redis_user_key


def cookie_dependency(request: Request):
    cookie_value = request.cookies.get("auth")

    if not cookie_value:
        raise HTTPException(
            status_code=302,
            detail="Not authorized",
            headers={"Location": "/auth"}
        )

    c_sp = cookie_value.split(':')
    r_key = get_redis_user_key(c_sp[0])
    r_data = rm_db.json().get(r_key)

    if r_data is None or c_sp[1] != r_data['cookie']:
        raise HTTPException(
            status_code=302,
            detail="Not authorized",
            headers={"Location": "/auth"}
        )

    r_data['username'] = c_sp[0]
    return r_data
