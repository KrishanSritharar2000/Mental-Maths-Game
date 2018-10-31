import pygame as pg
from os import path
import random
from settings import *
from button import *
from sceneManager import *

class Game:
    def __init__(self):
        #initializes game window
        pg.init()
        pg.mixer.init()#This handles all the sound and music in the game
        pg.font.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))#This creates the screen with the specified dimensions
        pg.display.set_caption(TITLE)#sets the title of the window
        self.clock = pg.time.Clock()#starts the internal clock to sync the program
        self.running = True
        self.loadData()

    def loadData(self):
        gameFolder = path.dirname(__file__)
        imgFolder = path.join(gameFolder, 'img')

    def drawText(self, text, size, colour, x, y, surf=None):
        if surf == None:
            surf = self.screen
        fontType = "C:\WINDOWS\FONTS\ARIAL.TTF"
        font = pg.font.SysFont('arial', size)
        textSurface = font.render(text, True, colour)
        textRect = textSurface.get_rect()
        textRect.center = (int(x),int(y))#aligns the text to the center
        surf.blit(textSurface, textRect)

    def new(self):
        #start a new Game
        self.allSprites = pg.sprite.Group()#This groups all the sprties together
        self.buttons = pg.sprite.Group()
        sceneMan = sceneManager(self)
        self.sceneMan = sceneMan
        sceneMan.loadLevel('startScreen')
        self.run()

    def run(self):
        #Game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        #Game loop - Update
        self.sceneMan.update()
        # self.allSprites.update()#Updates all of the sprties at once

    def events(self):
        #Game loop - Events
        for event in pg.event.get():
            #check for closing the window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                    self.running = False

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        #Game loop - Draw
        # self.screen.fill(RED)
        # self.drawText("Start Game", 12, BLACK, WIDTH/2, HEIGHT/2)
        self.allSprites.draw(self.screen)#draws all of the sprities to the screen at once
        pg.display.flip()#used for buffered frames- ALWAYS DO THIS LAST AFTER DRAWING EVERYTHING





g = Game()

while g.running:
    g.new()

pg.quit()
