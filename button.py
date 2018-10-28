import pygame as pg
from settings import *
vec = pg.math.Vector2

class Button(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height, solidColour, highlightColour, text, textSize):
        self.groups = game.allSprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.width = width
        self.height = height
        self.solidColour = solidColour
        self.highlightColour = highlightColour
        self.text = text
        self.textSize = textSize
        self.image = pg.Surface((width, height))
        self.image.fill(solidColour)
        self.rect = self.image.get_rect()
        self.pos = vec(x,y)
        self.rect.center = self.pos
        self.clicked = False



    def highlight(self):
        move = pg.mouse.get_pos()
        event = pg.event.get()
        self.on = "no"
        if self.rect.center[0] - self.width <= move[0] <= self.rect.center[0] + self.width and \
            self.rect.center[1] - self.height <= move[1] <= self.rect.center[1] + self.height:
            self.on = "yes"

            self.image.fill(self.highlightColour)
            if pg.mouse.get_pressed()[0] == 1:
                self.clicked = True
        else:
            self.image.fill(self.solidColour)
        for events in event:
            if events.type == pg.QUIT:
                pg.quit()
        print(self.on)
        self.game.screen.blit(self.image, self.rect)
        self.game.drawText(self.text, self.textSize, BLACK, self.pos[0], self.pos[1])

    def update(self):
        self.highlight()
        # print(self.clicked)
        if self.clicked:
            self.kill()
