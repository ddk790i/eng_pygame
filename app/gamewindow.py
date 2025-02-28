import pygame as pg
from pygame import Surface
from pygame.sprite import Group
from pygame.time import Clock

from app.assets import levels
from app.interface import Interface
from app.level import Level
from app.player import Player
from app.utils import create_ball, collide_balls
from settings import *


class GameWindow:
    """
    Окно, представляющее игровой процесс
    """

    def __init__(self, screen: Surface, clock: Clock):
        """
        Инициализация окна
        :param screen: дисплей для отрисовки графики
        :param clock: часы для обновления графики
        """
        self.screen, self.clock = screen, clock
        # Загрузка фоновой музыки и музыкальных эффектов
        pg.mixer.music.load('app/assets/music/background.mp3')
        self.game_over_music = pg.mixer.Sound('app/assets/music/game_over.mp3')
        self.success_music = pg.mixer.Sound('app/assets/music/success.mp3')
        self.miss_music = pg.mixer.Sound('app/assets/music/missing.mp3')
        self.next_level_music = pg.mixer.Sound('app/assets/music/next_level.mp3')
        # Загрузка шрифта для вывода сообщений
        self.app_font = pg.font.SysFont('segoeprint', 72)
        # Инициализация игрока и шаров
        self.player = Player()
        self.balls = Group()
        # Инициализация интерфейса
        self.interface = Interface()
        # Загрузка уровней и текущего уровня
        self.current_level_index = 0
        self.current_level = Level(levels[self.current_level_index])
        self.is_next_level_text_visible = False
        # Установка параметров появления шаров
        pg.time.set_timer(USEREVENT, SPAWN_TIMEOUT * self.current_level.spawn_ratio)
        self.game_over = False
        # Скрываем курсор для удобства игрового процесса
        pg.mouse.set_visible(False)

    def run(self) -> int:
        """
        Функция для старта игрового процесса
        :return: счет, набранный игроком или -1 в случае принудительного завершения игры
        """
        # Запуск фоновой музыки
        pg.mixer.music.play(-1)
        running = True
        # Основной цикл приложения
        while running:
            # region Обработка событий
            for event in pg.event.get():
                # Если принудительно вышли из окна
                if event.type == pg.QUIT:
                    pg.mixer.music.stop()
                    return -1
                if event.type == USEREVENT:
                    create_ball(self.balls)
                if event.type == NEXT_LEVEL_TEXT_TIMEOUT:
                    self.is_next_level_text_visible = False
            # endregion
            # Получаем координаты курсора для выставления персонажа
            x, y = pg.mouse.get_pos()
            dx = x - self.player.rect.centerx
            # region Обработка логики приложения
            self.player.update(dx)
            self.balls.update(self.current_level.speed_ratio)
            # Обновляем интерфейс и проверяем, есть ли у игрока жизни
            score, fine = collide_balls(self.player, self.balls, GROUND, self.success_music, self.miss_music)
            self.interface.add_score(score)
            self.interface.remove_lives(fine)
            if self.interface.lives <= 0:
                self.game_over = True
            self.interface.update()
            # Если количество очков превысило порог перехода на новый уровень, то переходим
            # Если значение порога равно -1, то не переходим на следующий уровень (бесконечная игра)
            if self.interface.score >= self.current_level.score_max != -1:
                self.next_level_music.play()
                self.current_level_index += 1
                self.current_level = Level(levels[self.current_level_index])
                self.is_next_level_text_visible = True
                pg.time.set_timer(NEXT_LEVEL_TEXT_TIMEOUT, SPAWN_TIMEOUT, 1)
                pg.time.set_timer(USEREVENT, int(SPAWN_TIMEOUT * self.current_level.spawn_ratio))
            # endregion
            # Отрисовка элементов приложения
            self.screen.blit(self.current_level.background_surf, (0, 0))
            self.interface.draw(self.screen)
            self.balls.draw(self.screen)
            self.player.draw(self.screen)
            # Отрисовка надписи перехода на следующий уровень
            if self.is_next_level_text_visible:
                text = self.app_font.render(f'Уровень:{self.current_level_index + 1}', 1,
                                            pg.color.Color('darkgreen'))
                rect = text.get_rect(center=(HALF_WIDTH, HALF_HEIGHT))
                self.screen.blit(text, rect)
            # Обработка завершения игры
            if self.game_over:
                self.game_over_music.play()
                running = False
            pg.display.update()
            # endregion
            self.clock.tick(FPS)
        pg.mixer.music.stop()
        return self.interface.score
