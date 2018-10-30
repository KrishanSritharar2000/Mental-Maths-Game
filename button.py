import pygame as pg
import pygame.freetype
from settings import *

vec = pg.math.Vector2

class Button(pg.sprite.Sprite):
    def __init__(self, game, tag, x, y, width, height, solidColour, highlightColour, text, textSize):
        self.groups = game.allSprites, game.buttons
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.tag = tag
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
        # self.game.drawText(self.text, self.textSize, BLACK, self.pos[0], self.pos[1])
        self.clicked = False
        self.first = True

    def drawTextToButton(self, text, size, x, y, colour=BLACK, surf=None):
        if surf == None:
            surf = self.screen
        fontType = "C:\WINDOWS\FONTS\ARIAL.TTF"
        buttonFont = pg.freetype.Font(fontType, 12)
        textSurf, rect = buttonFont.render(text, BLACK, size=size)
        rect.center = (x,y)
        surf.blit(textSurf, rect)
        buttonFont.render_to(surf, (x, y), text, colour)

    def drawText(self, text, size, colour, x, y, surf=None):
        pg.font.init()
        if surf == None:
            surf = self.game.screen
        fontType = "C:\WINDOWS\FONTS\ARIAL.TTF"
        font = pg.font.Font(fontType, size)
        textSurface = font.render(text, True, colour)
        textRect = textSurface.get_rect()
        textRect.center = (int(x),int(y))#aligns the text to the center
        surf.blit(textSurface, textRect)

    def highlight(self):
        move = pg.mouse.get_pos()
        prevcol = self.game.screen.get_at((int(self.pos[0]), int(self.pos[1])))
        print( "prevcol", prevcol)
        mouseDown = False
        for events in pg.event.get():
            if events.type == pg.MOUSEBUTTONUP:
                mouseDown = True
        colchange = False
        if self.rect.center[0] - self.width/2 <= move[0] <= self.rect.center[0] + self.width/2 and \
            self.rect.center[1] - self.height/2 <= move[1] <= self.rect.center[1] + self.height/2:
            if prevcol[0:3] != self.highlightColour:
                self.image.fill(self.highlightColour)
                # self.game.drawText(self.text, self.textSize, BLACK, self.pos[0], self.pos[1])
                colchange = True
            # if pg.mouse.get_pressed()[0] == 1:
            if pg.mouse.get_pressed()[0] == 1:
                self.clicked = True
        else:
            if prevcol[0:3] != self.solidColour:
                self.image.fill(self.solidColour)
                # self.game.drawText(self.text, self.textSize, BLACK, self.pos[0], self.pos[1])
                colchange = True
        if colchange or self.first:
            if self.first:
                self.first = False
            # self.game.screen.blit(self.image, self.rect)
            self.drawTextToButton(self.text, self.textSize, self.pos[0], self.pos[1], BLACK, self.image)
            print("done")


    def update(self):
        self.highlight()
        # if self.clicked:
        #     self.kill()

    def draw(self):
        pass
