import pygame

#screen size
GAME_WIDTH = 800
GAME_HEIGHT = 600

#map varables
MAP_WIDTH = 50
MAP_HEIGHT = 50
CELL_WIDTH = 10
CEL_HEIGHT = 10
MAP_MAX_NUM_ROOMS = 10

#room definition
ROOM_MAX_HEIGHT = 10
ROOM_MAX_WIDTH = 10
ROOM_MIN_HEIGHT = 8
ROOM_MIN_WIDTH = 8

#color
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREY = (100, 100, 100)

#screen color
COLOR_DEFAULT_BG = COLOR_GREY

#SPRITES
WALL = pygame.transform.scale(pygame.image.load("data/wall.png"),(15, 15))
FLOOR = pygame.transform.scale(pygame.image.load("data/floor.png"),(15, 15))

#GAME_MAP_SAVE
SAVE = 1