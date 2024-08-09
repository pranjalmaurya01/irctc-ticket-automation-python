import logging

import redis
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

redis_main_db = redis.Redis(host='localhost', port=6379, db=0)

# logging.basicConfig(level=logging.INFO, filename='api.log',
# filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)
