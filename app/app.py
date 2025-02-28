from datetime import datetime

import pygame as pg
import pygame_menu as pgm

from app import logger, db
from app.crud import get_leaders, delete_leaders, add_leader
from app.gameover import GameOver
from app.models import Leader
from app.utils import load_settings, save_settings
from app.gamewindow import GameWindow
from settings import *


class App:
    """
    Основной класс Pygame, содержащий каркас приложения
    """

    def __init__(self):
        # Создание иконки и текста приложения
        icon = pg.transform.scale(pg.image.load('app/assets/balls/football.png'), (40, 40))
        pg.display.set_icon(icon)
        pg.display.set_caption('')
        # Инициализация дисплея и системных часов
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        # Загрузка начальных настроек окна, которые сохраняются при выходе из приложения
        self.settings = load_settings(APP_SETTINGS_FILE_NAME)
        # Инициализация таблицы лидеров
        self.scores = []
        self._init_leaderboard()
        # Инициализация главного меню
        self.__init_menu()

    def __init_menu(self):
        """
        Функиия для инициализации главного меню
        :return: None
        """
        my_theme = pgm.themes.THEME_DARK
        my_theme.title_bar_style = pgm.widgets.MENUBAR_STYLE_NONE
        self.menu = pgm.Menu('Игра pygame инжинириум', WIDTH, HEIGHT, theme=my_theme)
        self.textinput = self.menu.add.text_input('Имя :', default=self.settings['player_name'],
                                                  onchange=self._update_app_settings)
        self.menu.add.button('Играть', self._run_game)
        self.menu.add.button('Топ-5 лидеров', self.leader_board)
        self.menu.add.button('Очистить таблицу лидеров', self._delete_leaders)
        self.menu.add.button('Выход', pgm.events.EXIT)

    def _update_app_settings(self, name):
        """
        Функция для сохранения настроек приложения
        :param name: Имя игрока
        :return: None
        """
        logger.debug(name)
        self.settings['player_name'] = name
        save_settings(APP_SETTINGS_FILE_NAME, self.settings)

    def _delete_leaders(self):
        count = delete_leaders(db)
        logger.debug(f'Удалено {count} строк')
        self._update_leaderboard()

    def _init_leaderboard(self):
        """
        Функция для инициализации таблицы лидеров
        :return: None
        """
        self.leader_board = pgm.Menu('Топ-5 игроков', WIDTH, HEIGHT, theme=pgm.themes.THEME_DARK)
        self.leaders_table = self.leader_board.add.table()
        self.leaders_table.default_cell_padding = 5
        bold_font = pgm.font.FONT_OPEN_SANS
        self.leaders_table.add_row(['№', 'Имя', 'Очки', 'Время'], cell_font=bold_font)
        self._update_leaderboard()

    def _update_leaderboard(self):
        """
        Функция для обновления таблицы лидеров
        :return: None
        """
        for score in self.scores:
            self.leaders_table.remove_row(score)
        self.scores = []
        data = get_leaders(db, PLAYERS_LIST_COUNT)
        for i, row in enumerate(data):
            row: Leader
            score = self.leaders_table.add_row([i + 1, row.name, row.score, str(row.date)])
            self.scores.append(score)

    def run(self):
        """
        Функция для запуска основного окна приложения
        :return: None
        """
        self.menu.mainloop(self.screen)

    def _run_game(self):
        """
        Функция для запуска игрового процесса
        :return: None
        """
        pg.mouse.set_visible(False)
        game_window = GameWindow(self.screen, self.clock)
        # Если игра возвращает -1, значит вышли из игры без сохранения результата
        score = game_window.run()
        if score != -1:
            logger.debug('Закончили игру')
            add_leader(db, Leader({'name': self.textinput.get_value(), 'score': score, 'date': datetime.now()}))
            self._update_leaderboard()
            # Если игрок проиграл, то показываем окно окончания игры
            game_over_window = GameOver(self.screen, self.clock, score)
            game_over_window.run()
