from sqlalchemy.orm import Session

from app import Base, engine, logger
from app.models import Leader


def create_table():
    """
    Функция для создания таблиц в БД
    :return:
    """
    Base.metadata.create_all(engine)


def add_leader(db: Session, leader: Leader):
    """
    Функция для добавления игрока в баку данных
    :param db: экземпляр БД
    :param leader: информация об игроке
    :return: None
    """
    try:
        db.add(leader)
        db.commit()
    except Exception as e:
        logger.error(e)


def get_leaders(db: Session, count: int):
    """
    Функция для получения списка лучших игроков
    :param count: сколько игроков необходимо вернуть
    :param db: экземпляр БД
    :return: список игроков
    """
    try:
        return db.query(Leader).order_by(Leader.score.desc()).all()[:count]
    except Exception as e:
        logger.error(e)
        return []


def delete_leaders(db: Session):
    """
    Функция для очистки таблицы с игроками
    :param db: экземпляр БД
    :return: число уделенных записей
    """
    count = db.query(Leader).delete()
    db.commit()
    return count
