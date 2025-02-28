import logging

import pygame as pg
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from settings import LOG_FILE_NAME

# переменные для работы с БД SQLITE
engine = db.create_engine('sqlite:///pygame_eng.db')
Base = declarative_base()
db = Session(engine)
# переменная для записи логов приложения
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARNING)
file_handler = logging.FileHandler(LOG_FILE_NAME)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s'))
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
logger.addHandler(file_handler)
logger.addHandler(console_handler)

from app.app import App

# экземпляр основного приложения
pg.init()
app = App()
