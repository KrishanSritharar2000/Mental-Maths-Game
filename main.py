import pygame as pg
from os import path
import random
from settings import *
from sprites import *
from management import *

vec = pg.math.Vector2

class Game:
    def __init__(self):
        #initializes game window
        pg.init()
        pg.mixer.init()#This handles all the sound and music in the game
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))#This creates the screen with the specified dimensions
        pg.display.set_caption(TITLE)#sets the title of the window
        self.clock = pg.time.Clock()#starts the internal clock to sync the program
        self.running = True
        self.loadData()

    def loadData(self):
        self.gameFolder = path.dirname(__file__)
        self.imgFolder = path.join(self.gameFolder, 'img')
        self.menuButtonSolid = pg.image.load(path.join(self.imgFolder, 'blue_button01.png')).convert_alpha()
        self.menuButtonHighlight = pg.image.load(path.join(self.imgFolder, 'green_button01.png')).convert_alpha()
        self.interfaceFont = path.join(self.imgFolder, 'Future.ttf')
        self.buttonFont = path.join(self.imgFolder, 'PixelSquare.ttf')
        self.menuImages = {}
        self.menuImages["startScreen"] =  pg.image.load(path.join(self.imgFolder, 'grey_background.jpg')).convert_alpha()
        self.menuImages["mainMenu"] =  pg.image.load(path.join(self.imgFolder, 'blue_background.jpg')).convert_alpha()
        self.menuImages["settingsMenu"] =  pg.image.load(path.join(self.imgFolder, 'Grey_yellow_background.jpg')).convert_alpha()
        self.menuImages["levelSelect"] =  pg.image.load(path.join(self.imgFolder, 'Grey_blue_background.jpg')).convert_alpha()
        self.menuImages["stats"] =  pg.image.load(path.join(self.imgFolder, 'Grey_green_background.jpg')).convert_alpha()
        self.menuImages["leaderboard"] =      pg.image.load(path.join(self.imgFolder, 'Grey_violet_background.jpg')).convert_alpha()
        self.menuImages["shop"] =  pg.image.load(path.join(self.imgFolder, 'Grey_orange_background.jpg')).convert_alpha()
        self.menuImages["pause"] =  pg.image.load(path.join(self.imgFolder, 'Grey_red_background.jpg')).convert_alpha()
        self.pauseIMGWhite = pg.image.load(path.join(self.imgFolder, 'pauseWhite.png')).convert_alpha()
        self.pauseIMGBlack = pg.image.load(path.join(self.imgFolder, 'pauseBlack.png')).convert_alpha()
        self.playerBikeImage = pg.transform.scale(pg.image.load(path.join(self.imgFolder, 'bike.png')).convert_alpha(), (30, 30))



    def drawText(self, text, size, colour, x, y, surf=None, align=None, fontName=None):
        if surf == None:
            surf = self.screen
        fontType = "C:\WINDOWS\FONTS\ARIAL.TTF"
        if fontName == None:
            font = pg.font.SysFont('arial', size)
        else:
            font = pg.font.Font(fontName, size)
        textSurface = font.render(text, True, colour)
        textRect = textSurface.get_rect()
        if align == None:
            textRect.center = (int(x),int(y))#aligns the text to the center
        if align == "tl":
            textRect.topleft = (int(x),int(y))
        surf.blit(textSurface, textRect)

    def new(self):
        #start a new Game
        self.allSprites = pg.sprite.Group()#This groups all the sprties together
        self.buttons = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.map = None
        self.camera = None
        #Map(path.join(self.gameFolder,'map2.txt', 'LevelTest2'))
        #Camera(self.map.width, self.map.height)
        self.sceneMan = sceneManager(self)
        self.player = None
        self.prevRotate = 0
        self.sceneMan.loadLevel('startScreen')
        self.run()

    def run(self):
        #Game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def rot_center(self, image, angle):
        """rotate an image while keeping its center and size"""
        orig_rect = image.get_rect()
        rot_image = pg.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def update(self):
        #Game loop - Update
        self.sceneMan.update()
        self.allSprites.update()#Updates all of the sprties at once
        if self.sceneMan.currentScene not in MENU_SCREENS:
            self.camera.update(self.player)

            hitPlatform = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hitPlatform:
                self.player.pos.y = hitPlatform[0].rect.y - self.player.height / 2
                self.player.vel.y = 0


##                self.vecToPlayer = self.player.pos - vec(0, HEIGHT)
##                self.rotate = self.vecToPlayer.angle_to(vec(1, 0))
##                print(self.player.pos)
##                print(self.rotate)
##                if self.prevRotate != round(self.rotate,2):
##                    self.player.image = self.rot_center(self.player.image, self.rotate)
##                    # self.player.image = pg.transform.rotate(self.player.image, self.rotate)
##                    # self.player.rect = self.player.image.get_rect()
##                    # self.player.rect.center = self.player.pos
##                    self.prevRotate = round(self.rotate,2)

    def events(self):
        #Game loop - Events
        for event in pg.event.get():
            #check for closing the window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                    self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        for button in self.buttons:
            button.draw()
        # self.buttons.draw(self.screen)
        if self.sceneMan.currentScene not in MENU_SCREENS:
            for sprite in self.allSprites:
                self.screen.blit(sprite.image, self.camera.applyOffset(sprite))

            # self.allSprites.draw(self.screen)#draws all of the sprities to the screen at once
        pg.display.flip()#used for buffered frames- ALWAYS DO THIS LAST AFTER DRAWING EVERYTHING

g = Game()

while g.running:
    g.new()

pg.quit()
