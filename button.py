import pygame as pg
from settings import *

vec = pg.math.Vector2

class Button(pg.sprite.Sprite):
    def __init__(self, game, tag, x, y, width, height, solidColour, highlightColour, text, textSize):
        self.groups = game.buttons
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.tag = tag
        self.width = width
        self.height = height
        self.solidColour = solidColour
        self.highlightColour = highlightColour
        self.text = text
        # if textSize == None:
        #     self.textSize = int(width/(len(text)*0.45))
        #     print("Text Size {} for {}".format(self.textSize, self.tag))
        #     if self.textSize > 24:
        #         self.textSize = 24
        # else:
        self.textSize = textSize
        self.pos = vec(x,y)
        self.rectDimensions = (self.pos[0]-self.width/2, self.pos[1]-self.height/2, self.width, self.height)
        self.image = pg.draw.rect(self.game.screen, self.solidColour, self.rectDimensions , 0)
        self.clicked = False
        self.first = True

    def highlight(self):
        mousePos = pg.mouse.get_pos()
        prevcol = self.game.screen.get_at((int(self.pos[0]-self.width/2), int(self.pos[1]-self.height/2)))
        colchange = False
        if self.pos[0] - self.width/2  <= mousePos[0] <= self.pos[0] + self.width/2 and \
            self.pos[1] - self.height/2 <= mousePos[1] <= self.pos[1] + self.height/2:
            if prevcol[0:3] != self.highlightColour:
                self.image = pg.draw.rect(self.game.screen, self.highlightColour, self.rectDimensions , 0)
                colchange = True
            if pg.mouse.get_pressed()[0] == 1:
                self.clicked = True
        else:
            if prevcol[0:3] != self.solidColour:
                self.image = pg.draw.rect(self.game.screen, self.solidColour, self.rectDimensions , 0)
                colchange = True
        if colchange == True or self.first == True:
            if self.first:
                print(self.first, "self.first")
                self.first = False
            self.game.drawText(self.text, self.textSize, BLACK, self.pos[0], self.pos[1])

    def update(self):
        self.highlight()
        if self.clicked:
            for button in self.game.buttons:
                if button != self:
                    button.kill()
