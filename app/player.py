from typing import Any

from pygame import Surface
from pygame.sprite import Sprite

from settings import *
import pygame as pg


class Player(Sprite):
    """
    Класс для представления игрока на экране игры
    """

    def __init__(self):
        """
        Инициализация игрока
        """
        super(Player, self).__init__()
        self.image = pg.image.load('app/assets/player.png').convert_alpha()
        self.image = pg.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.rect = self.image.get_rect(center=(HALF_WIDTH, 0), bottom=GROUND)

    def update(self, *args: Any, **kwargs: Any) -> None:
        """
        Обновление основных конструкций класса в зависимости от смещения курсора мыши
        :param args:
        :param kwargs:
        :return: None
        """
        if args[0] > 0:
            dx = args[0] if self.rect.right + args[0] < WIDTH else 0
        else:
            dx = args[0] if self.rect.left + args[0] > 0 else 0
        self.rect.move_ip(dx, 0)

    def draw(self, screen: Surface):
        """
        Функция для отрисовки персонажа
        :param screen: экран, на котором отображается персонаж
        :return: None
        """
        screen.blit(self.image, self.rect)
