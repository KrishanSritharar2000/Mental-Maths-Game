import pygame as pg
from settings import *
from sprites import *


class sceneManager():
    def __init__(self, game):
        self.game = game
        self.currentScene = 'startScreen'
        self.backgroundColour = BLACK


    def loadLevel(self, level=None):
        self.level = level
        if self.level == "settingsMenu":
            self.settingsMenu()
        if self.level == "mainMenu":
            self.mainMenu()
        if self.level == "levelSelect":
            self.levelSelect()
        if self.level == "stats":
            self.stats()
        if self.level == "leaderboard":
            self.leaderboard()
        if self.level == "shop":
            self.shop()
        if self.level == "startScreen":
            self.startScreen()
        if self.level == "gameOverScreen":
            self.gameOverScreen()
        if self.level == "level1":
            self.level1()

    def settingsMenu(self):
        self.game.screen.fill((30, 210, 110))
        self.game.drawText("Change the Game Settings", 25, BLACK, WIDTH/2, HEIGHT*1/6)
        self.mainMenuButton = Button(self.game, "mainMenu", WIDTH*1/8, HEIGHT*1/12, 60, 25, YELLOW, LIGHT_BLUE, "Back", 18)

    def levelSelect(self):
        self.game.screen.fill((160, 160, 160))
        self.game.drawText("Select the Level you want to play!", 25, BLACK, WIDTH/2, HEIGHT*1/6)
        self.mainMenuButton = Button(self.game, "mainMenu", WIDTH*1/8, HEIGHT*1/12, 60, 25, YELLOW, LIGHT_BLUE, "Back", 18)
        self.level1Button = Button(self.game, "level1", WIDTH*1/2, HEIGHT*1/2, WIDTH/6, HEIGHT/12, YELLOW, LIGHT_BLUE, "Level One")

    def stats(self):
        self.game.screen.fill((220, 110, 250))
        self.game.drawText("View your statistics", 25, BLACK, WIDTH/2, HEIGHT*1/6)
        self.mainMenuButton = Button(self.game, "mainMenu", WIDTH*1/8, HEIGHT*1/12, 60, 25, YELLOW, LIGHT_BLUE, "Back", 18)

    def leaderboard(self):
        self.game.screen.fill((50, 250, 160))
        self.game.drawText("Leader Board Tables", 25, BLACK, WIDTH/2, HEIGHT*1/6)
        self.mainMenuButton = Button(self.game, "mainMenu", WIDTH*1/8, HEIGHT*1/12, 60, 25, YELLOW, LIGHT_BLUE, "Back", 18)

    def shop(self):
        self.game.screen.fill((255, 180, 0))
        self.game.drawText("Spend you coins in the shop", 25, BLACK, WIDTH/2, HEIGHT*1/6)
        self.mainMenuButton = Button(self.game, "mainMenu", WIDTH*1/8, HEIGHT*1/12, 60, 25, YELLOW, LIGHT_BLUE, "Back", 18)

    def mainMenu(self):
        self.game.screen.fill((255,90,70))
        self.game.drawText("This is the Main Menu", 25, BLACK, WIDTH/2, HEIGHT*1/4)
        self.startScreenButton = Button(self.game, "startScreen", WIDTH/4, HEIGHT*3/8, WIDTH/6, HEIGHT/12, YELLOW, LIGHT_BLUE, "Start Screen")
        self.levelSelectButton = Button(self.game, "levelSelect", WIDTH*3/4, HEIGHT*3/8, WIDTH/6, HEIGHT/12, YELLOW, LIGHT_BLUE, "Select Level")
        self.settingsMenuButton = Button(self.game, "settingsMenu", WIDTH/4, HEIGHT*5/8, WIDTH/6, HEIGHT/12, YELLOW, LIGHT_BLUE, "Settings")
        self.shopButton = Button(self.game, "shop", WIDTH*3/4, HEIGHT*5/8, WIDTH/6, HEIGHT/12, YELLOW, LIGHT_BLUE, "Shop")
        self.leaderboardButton = Button(self.game, "stats", WIDTH/4, HEIGHT*7/8, WIDTH/6, HEIGHT/12, YELLOW, LIGHT_BLUE, "Stats")
        self.statsButton = Button(self.game, "leaderboard", WIDTH*3/4, HEIGHT*7/8, WIDTH/6, HEIGHT/12, YELLOW, LIGHT_BLUE, "Leaderboard")

    def startScreen(self):
        #game spalsh/start screen
        self.game.screen.fill((70,210,255))
        self.game.drawText("Welome to my Game", 24, BLACK, WIDTH/2, HEIGHT*1/4)
        self.game.drawText("Press a button to conitnue!", 12, BLACK, WIDTH/2, HEIGHT*3/4)
        pg.display.flip()
        self.waitForKey()
        self.loadLevel('mainMenu')

    def gameOverScreen(self):
        #game over/continue screen
        pass

    def level1(self):
        self.game.screen.fill(BLACK)
        self.showPlayer = True
        Platform(self.game, 0, HEIGHT*7/8, WIDTH, HEIGHT/8)

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
                # print("tag",button.tag)
                if button.tag == "startScreen":
                    self.loadLevel('startScreen')
                if button.tag == "levelSelect":
                    self.loadLevel('levelSelect')
                if button.tag == "shop":
                    self.loadLevel('shop')
                if button.tag == 'mainMenu':
                    self.loadLevel('mainMenu')
                if button.tag == "settingsMenu":
                    self.loadLevel('settingsMenu')
                if button.tag == 'leaderboard':
                    self.loadLevel('leaderboard')
                if button.tag == 'stats':
                    self.loadLevel('stats')
                if button.tag == 'level1':
                    self.loadLevel('level1')
                self.currentScene = button.tag
                button.kill()
        if self.currentScene != "level1":
            self.showPlayer = False
