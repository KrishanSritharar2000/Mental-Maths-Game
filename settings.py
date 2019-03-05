import pygame as pg
#Game options/settings

TITLE = "Demo"
# WIDTH = 360
# HEIGHT = 480
# WIDTH = 512
# HEIGHT = 384
WIDTH = 768
HEIGHT = 576
# WIDTH = 1024
# HEIGHT = 768
FPS = 60

TILESIZE = 32 #32
TILESIZE_TRACK = 32

GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

TIME_FOR_EASY_Q = 10
TIME_FOR_MEDIUM_Q = 15
TIME_FOR_HARD_Q = 20


MENU_SCREENS = ["settingsMenu",
                "mainMenu",
                "levelSelect",
                "stats",
                "leaderboard",
                "shop",
                "startScreen",
                "gameOverScreen",
                "pause",
                "levelComplete"]

LEVEL_SCREENS = ["level1",
                "level2",
                "level3",
                "level4",
                "level5",
                "level6",
                "level7",
                "level8",
                "minigame"]


#Player properties
PLAYER_ACC = 0.65
BRAKE_ACC = 0.4
PLAYER_FRICTION = -0.08
PLAYER_GRAV = 0.8

#Layers
PLAYER_LAYER = 2
PLATFORM_LAYER = 1
WALL_LAYER = 1
TRACK_LAYER = 1
RECTANGLE_LAYER = 2
QUESTION_LAYER = 3
COIN_LAYER = 3
INPUT_BOX_LAYER = 1
BUTTON_LAYER = 1


# define colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
LIGHT_RED = (210, 0, 0)
LIGHT_GREEN = (0, 150, 0)
LIGHT_BLUE = (0,0,210)
HUD_COLOUR = BLACK

#Images
COIN_IMAGES = ["coin1.png",
               "coin2.png",
               "coin3.png",
               "coin4.png",
               "coin5.png",
               "coin6.png"]
QUESTION_IMAGE = "boxQuestion.png"
