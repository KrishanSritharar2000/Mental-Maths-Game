import pygame as pg
from settings import *
from button import *


class sceneManager():
    def __init__(self, game):
        self.game = game


    def loadLevel(self, level=None):
        self.level = level
        if self.level == "settings":
            self.settingsMenu()
        if self.level == "levelSelect":
            self.levelSelect()
        if self.level == "stats":
            self.stats()
        if self.level == "shop":
            self.shop()
        if self.level == "mainMenu":
            self.mainMenu()
        if self.level == "startScreen":
            self.startScreen()
        if self.level == "gameOverScreen":
            self.gameOverScreen()

    def settingsMenu(self):
        pass

    def levelSelect(self):
        pass

    def stats(self):
        pass

    def shop(self):
        pass

    def mainMenu(self):
        self.game.screen.fill(RED)
        self.game.drawText("This is the Main Menu", 25, BLACK, WIDTH/2, HEIGHT*1/4)
        self.startScreenButton = Button(self.game, "startScreen", WIDTH/2, HEIGHT*3/4, 75, 50, GREEN, LIGHT_GREEN, "Go to start screen", 25)

    def startScreen(self):
        #game spalsh/start screen
        self.game.screen.fill(BLUE)
        self.game.drawText("Welome to my Game", 24, BLACK, WIDTH/2, HEIGHT*1/4)
        self.game.drawText("Press a button to conitnue!", 12, BLACK, WIDTH/2, HEIGHT*3/4)
        pg.display.flip()
        self.waitForKey()
        self.loadLevel('mainMenu')

    def gameOverScreen(self):
        #game over/continue screen
        pass

    def waitForKey(self, key = True, click = True):#key contiues if a key is get_pressed
        pg.event.wait()#click continues if the mouse button is pressed
        waiting = True
        while waiting:
            self.game.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    # waiting = self.game.running = False
                if event.type == pg.KEYUP and key:
                    waiting = False
                if event.type == pg.MOUSEBUTTONUP and click:
                    waiting = False

    def waitForButtonPress(self, button, clicked):
        while clicked == False:
            button.update()
            pg.display.flip()

    def update(self):
        # pg.display.set_caption("{:.2f}".format(self.game.clock.get_fps()))
        self.game.buttons.update()
        # pg.display.flip()
        for button in self.game.buttons:
            if button.clicked == True:
                print("tag",button.tag)
                if button.tag == "startScreen":
                    self.loadLevel('startScreen')
                button.kill()
