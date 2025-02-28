import pygame as pg
from pygame import Surface
from pygame.sprite import Sprite

from settings import WIDTH, LIVES_COUNT


class Interface(Sprite):
    """
    Клаcс, содержащий логику и функции отображения интерфейса игрового процесса
    """

    def __init__(self):
        """
            Инициализация основных элементов интерфейса
        """
        super().__init__()
        self.font = pg.font.SysFont('segoeprint', 32)
        self.image = self.font.render(f"Количество очков: {0}", 1, pg.Color("black"))
        self.rect = self.image.get_rect(topright=(WIDTH, 0))
        self.life_surf = pg.transform.scale(pg.image.load('app/assets/life.png').convert_alpha(), (40, 40))
        self.score = 0
        self.lives = LIVES_COUNT

    def add_score(self, score: int):
        """
        Функция для обновления счета
        :param score: очки, которые необходимо добавить
        :return: None
        """
        self.score += score

    def remove_lives(self, lives: int):
        """
        Функция для обновления количества жизней
        :param lives: количество жизней, которые нужно убавить
        :return: None
        """
        self.lives += lives

    def __draw_lives(self, screen: Surface):
        """
        Функция для отрисовки жизней на экране
        :param screen:
        :return: None
        """
        for i in range(self.lives):
            rect = self.life_surf.get_rect(topright=(WIDTH - 45 * i, self.rect.bottom + 5))
            screen.blit(self.life_surf, rect)

    def update(self, *args, **kwargs):
        """
        Функция обновления интерфейса
        """
        self.image = self.font.render(f"Количество очков: {self.score}", 1, pg.Color("black"))
        self.rect = self.image.get_rect(topright=(WIDTH, 0))

    def draw(self, screen: Surface):
        """
        Функция для отрисовки интерфейса
        :param screen: экран отображения
        :return: None
        """
        screen.blit(self.image, self.rect)
        self.__draw_lives(screen)
