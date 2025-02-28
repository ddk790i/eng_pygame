import random

import pygame as pg
from pygame.mixer import Sound
from pygame.sprite import Group

from app.assets import balls
from app.ball import Ball
from app.player import Player

import json

from settings import APP_SETTINGS_FILE_NAME

# Настройки по умолчанию (в случае, если затрется конфигурационный файл)
app_settings = {
    'player_name': 'DD'
}


def load_settings(filename) -> dict:
    """
    Функция для получения списка настроек по пути файла
    :param filename: путь к файлу
    :return: словарь "имя настройки - значение"
    """
    return json.load(open(filename))


def save_settings(filename, settings):
    """
    Функция для сохранения настроек в файл
    :param filename: путь к файлу
    :param settings: словарь "имя настройки - значение"
    :return: None
    """
    with open(filename, 'w') as settings_file:
        settings_file.write(json.dumps(settings))


def create_ball(group: Group):
    """
    Функция для создания мяча
    Скорость, изображение и характеристики мяча выбираются случайно из массива мячей
    :param group: группа, в которую помещается игровой предмет
    :return: экземпляр класса Ball
    """
    ball_properties = random.choice(balls)
    min_speed = ball_properties['min_speed']
    max_speed = ball_properties['max_speed']
    speed = random.randint(min_speed, max_speed)
    image_surf = pg.image.load(f"app/assets/balls/{ball_properties['image']}").convert_alpha()
    width = ball_properties['width']
    height = ball_properties['height']
    return Ball(image_surf, width, height, speed, group)


def collide_balls(player: Player, balls: Group, ground, success_music: Sound, miss_music: Sound) -> tuple[int, int]:
    """
    Функция для определения прикосновения мячей с игроком, а также вылета мячей за пределы экрана
    :param player: игровой персонаж
    :param balls: группа мячей
    :param ground: y - координата поверхности, за которую может улететь мяч (мячи летят сверху-вниз)
    :param success_music: музыка, воспроизводящаяся при успешной ловле мяча
    :param miss_music: музыка, воспроизводящаяся, когда мяч вылетает за пределы экрана
    :return: пара значений количество заработанных очков, количество потерянных жизней
    """
    score, fine = 0, 0
    for ball in balls:
        # если игрок поймал мяч, мяч удаляется из группы, игроку добавляются очки
        if ball.rect.colliderect(player.rect):
            score += 100
            success_music.play()
            balls.remove(ball)
        elif ball.rect.top > ground:
            # если игрок пропустил мяч, тот упал (вышел за пределы экрана), у игрока отнимается 1 жизнь
            fine -= 1
            miss_music.play()
            balls.remove(ball)
    return score, fine


# Перовидное создание конфигурационного файла
if __name__ == '__main__':
    save_settings(APP_SETTINGS_FILE_NAME, app_settings)
