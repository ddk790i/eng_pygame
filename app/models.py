import sqlalchemy as db

from app import Base


class Leader(Base):
    """
    Класс для реализации ORM для работы с БД
    """
    __tablename__ = 'leaders'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    score = db.Column(db.Integer)
    date = db.Column(db.Date)

    def __init__(self, params: dict):
        """
        Инициализация экземпляра класса
        :param params: словарь с ключами - именами переменных, параметрами - значениями
        """
        super().__init__()
        for var, val in params.items():
            setattr(self, var, val)

    def __repr__(self):
        return f'leader {self.name} with score {self.score}'
