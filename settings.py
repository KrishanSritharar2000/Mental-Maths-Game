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

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

TILESIZE_TRACK = 32

MENU_SCREENS = ["settingsMenu",
                "mainMenu",
                "levelSelect",
                "stats",
                "leaderboard",
                "shop",
                "startScreen",
                "gameOverScreen",
                "pause"]

#Player properties
PLAYER_ACC = 1.4
BRAKE_ACC = 0.4
PLAYER_FRICTION = -0.05
PLAYER_GRAV = 0.8

#0.5
#-0.12


# define colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHT_RED = (210, 0, 0)
LIGHT_GREEN = (0, 150, 0)
LIGHT_BLUE = (0,0,210)
