import pygame as pg
from os import path
import random
from settings import *
from button import *

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
        gameFolder = path.dirname(__file__)
        imgFolder = path.join(gameFolder, 'img')
        self.titleFont = path.join(imgFolder, 'Impacted2.0.TTF')

    def drawText(self, text, size, colour, x, y):
        font_type = "C:\WINDOWS\FONTS\ARIAL.TTF"
        font = pg.font.Font(font_type, size)
        text_surface = font.render(text, True, colour)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)#aligns the text to the center
        self.screen.blit(text_surface, text_rect)

    def new(self):
        #start a new Game
        self.allSprites = pg.sprite.Group()#This groups all the sprties together
        g.showStartScreen()
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
        self.allSprites.update()#Updates all of the sprties at once

    def events(self):
        #Game loop - Events
        for event in pg.event.get():
            #check for closing the window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                    self.running = False

    def draw(self):
        #Game loop - Draw
        self.screen.fill(RED)
        self.drawText("Start Game", 12, BLACK, WIDTH/2, HEIGHT/2)
        self.allSprites.draw(self.screen)#draws all of the sprities to the screen at once
        pg.display.flip()#used for buffered frames- ALWAYS DO THIS LAST AFTER DRAWING EVERYTHING

    def showStartScreen(self):
        self.screen.fill(BLUE)
        self.drawText("Hello World", 12, BLACK, WIDTH/2, HEIGHT/2)
        pg.display.flip()

        # self.button = Button(self, WIDTH/2, HEIGHT *3/4, 75, 50, GREEN, LIGHT_GREEN, "Button", 25)
        # while self.button.clicked == False:
        #     self.button.highlight()
        #     pg.display.flip()
        self.waitForKey()

    def show_go_screen(self):
        #game over/continue screen
        pass

    def waitForKey(self):
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = self.running = False
                if event.type == pg.KEYUP or event.type == pg.MOUSEBUTTONUP:
                    waiting = False

g = Game()
# g.showStartScreen()

while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
