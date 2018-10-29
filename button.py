import pygame as pg
from settings import *

vec = pg.math.Vector2

class Button(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height, solidColour, highlightColour, text, textSize):
        self.groups = game.allSprites, game.buttons
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
        prevcol = self.game.screen.get_at((int(self.pos[0]), int(self.pos[1])))
        colchange = False
        if self.rect.center[0] - self.width/2 <= move[0] <= self.rect.center[0] + self.width/2 and \
            self.rect.center[1] - self.height/2 <= move[1] <= self.rect.center[1] + self.height/2:
            if prevcol[0:3] != self.highlightColour:
                self.image.fill(self.highlightColour)
                colchange = True
            if pg.mouse.get_pressed()[0] == 1:
                self.clicked = True
        else:
            if prevcol[0:3] != self.solidColour:
                self.image.fill(self.solidColour)
                colchange = True
        for events in event:
            if events.type == pg.QUIT:
                pg.quit
        if colchange:
            self.drawText(self.text, self.textSize, BLACK, self.pos[0], self.pos[1])
            # self.game.screen.blit(self.image, self.rect)
            print("done")
    def drawText(self, text, size, colour, x, y):
        font_type = "C:\WINDOWS\FONTS\ARIAL.TTF"
        font = pg.font.Font(font_type, size)
        text_surface = font.render(text, True, colour)
        text_rect = text_surface.get_rect()
        text_rect.center = (int(x),int(y))#aligns the text to the center
        self.game.screen.blit(text_surface, text_rect)

    def update(self):
        self.highlight()
        if self.clicked:
            self.kill()

    def draw(self):
        pass
