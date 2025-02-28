import pygame as pg
from pygame import Surface
from pygame_widgets.button import Button
import pygame_widgets as pgw

from app import logger
from settings import HALF_WIDTH, HALF_HEIGHT, FPS, WIDTH, HEIGHT


class GameOver:
    """
    Класс для отображения окна "Конец игры"
    """
    def __init__(self, screen, clock, score):
        """
        Инициализация экземпляра окна
        :param screen: кран для отрисовки
        :param clock: часы дл контроля FPS
        :param score: очки, которые заработал игрок
        """
        self.screen, self.clock = screen, clock
        self.score = score
        self.background = pg.transform.scale(pg.image.load('app/assets/game_over.jpg'), (WIDTH, HEIGHT))
        self.app_font = pg.font.SysFont('segoeprint', 36)
        self.cursor = pg.transform.scale(pg.image.load(f'app/assets/hand.png'), (64, 84))
        self.cursor_rect = self.cursor.get_rect(center=pg.mouse.get_pos())
        pg.mouse.set_visible(False)
        surf = Surface((500, 100))
        rect = surf.get_rect(center=(HALF_WIDTH, HALF_HEIGHT))
        self.button = Button(
            screen, rect.x, rect.y, rect.width, rect.height, text='Выйти в главное меню',
            fontSize=50, margin=20,
            inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=20,
            onClick=self._go_to_menu
        )
        self.running = True

    def _go_to_menu(self):
        """
        Функция для выхода из окна "Конец игры"
        :return: None
        """
        logger.debug('on exit')
        self.running = False

    def run(self):
        """
        Функция для отображения окна
        :return: None
        """
        # Основной цикл приложения
        while self.running:
            # region Обработка событий
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    self.running = False
            pgw.update(events)
            self.screen.blit(self.background, (0, 0))
            text = self.app_font.render(f'Игра окончена: {self.score} очков набрано', 1, pg.color.Color('darkred'))
            rect = text.get_rect(center=(HALF_WIDTH, HALF_HEIGHT - 100))
            self.screen.blit(text, rect)
            self.button.draw()

            self.cursor_rect.center = pg.mouse.get_pos()
            self.screen.blit(self.cursor, self.cursor_rect)
            pg.display.update()
            # endregion
            self.clock.tick(FPS)
