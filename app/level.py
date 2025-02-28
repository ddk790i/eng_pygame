import pygame as pg

from settings import WIDTH, HEIGHT


class Level:
    """
    Класс, содержащий настройки игрового уровня
    """

    def __init__(self, params: dict):
        """
        Инициализация уровня
        :param params:
        """
        # Задний фон
        self.background = ""
        # Количество очков для перехода на новый уровень
        self.score_max = 0
        # Коэффициент ускорения мячей
        self.speed_ratio = 1
        # Вероятность выпадения жизни (не используется)
        self.life_chance = 0.1
        # Коэффициент ускорения скорости генерации мячей
        self.spawn_ratio = 1

        for var, val in params.items():
            setattr(self, var, val)
            if var == 'background':
                if '.png' in val:
                    self.background_surf = pg.image.load(f'app/assets/locations/{val}').convert_alpha()
                elif '.jpg' in val:
                    self.background_surf = pg.image.load(f'app/assets/locations/{val}').convert()
                self.background_surf = pg.transform.scale(self.background_surf, (WIDTH, HEIGHT))
