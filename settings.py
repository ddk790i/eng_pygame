# Настройки размеров экрана и количества кадров в секунду
from pygame import USEREVENT

APP_SETTINGS_FILE_NAME = 'app_settings.json'
LOG_FILE_NAME = 'log.txt'
WIDTH = 1200
HEIGHT = 750
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
GROUND = HEIGHT - 10
FPS = 60
# Настройки игрока
PLAYER_WIDTH = 100
PLAYER_HEIGHT = 127
PLAYER_SPEED = 5
LIVES_COUNT = 3
# Настройки игры
SPAWN_TIMEOUT = 2000
NEXT_LEVEL_TEXT_TIMEOUT = USEREVENT + 1
PLAYERS_LIST_COUNT = 5
