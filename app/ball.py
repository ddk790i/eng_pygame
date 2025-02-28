import random
from typing import Any

from pygame import Surface, Rect
from pygame.sprite import Sprite, Group

from settings import *
import pygame as pg


class Ball(Sprite):
    """
    Класс для отображения мячей на экране игры
    """

    def __init__(self, image_surface: Surface, width: int, height: int, speed: int, group: Group):
        super(Ball, self).__init__()
        self.image = image_surface
        self.image = pg.transform.scale(self.image, (width, height))
        self.x = random.randint(0, WIDTH)
        self.rect = self.image.get_rect(center=(self.x, 0), bottom=0)
        self.add(group)
        self.speed = speed

    def update(self, *args: Any, **kwargs: Any) -> None:
        """
        Функция для обновления местоположения предмета
        :param args:
        :param kwargs:
        :return: None
        """
        self.rect.bottom += self.speed * args[0]
