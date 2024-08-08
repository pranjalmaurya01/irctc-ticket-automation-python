import redis
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

redis_main_db = redis.Redis(host='localhost', port=6379, db=0)
