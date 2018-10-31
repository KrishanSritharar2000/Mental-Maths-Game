import pygame as pg
import pygame.freetype
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
        self.textSize = textSize
        self.pos = vec(x,y)
        self.rectDimensions = (self.pos[0], self.pos[1], self.width, self.height)
        self.image = pg.Surface((self.width, self.height)).convert_alpha()
        self.image.fill(solidColour)
        # prnt("self.rect", self.rect)
        # self.game.drawText(self.text, self.textSize, BLACK, self.pos[0], self.pos[1])
        # self.game.screen.fill(self.solidColour, (self.pos[0]-self.width, self.pos[1]-self.height, self.width, self.height))
        # self.image = pg.draw.rect(self.game.screen, self.solidColour, self.rectDimensions , 0)
        self.rect = self.image.get_rect()
        # print(self.rect,"rect")
        self.rect.center = self.pos
        self.clicked = False
        self.first = True
        # font = pg.font.SysFont('arial', self.textSize)
        # textSurface = font.render(self.text, 1, BLACK)
        # textRect = textSurface.get_rect()
        # textRect.center = (int(self.pos[0]), int(self.pos[1]))
        # self.game.screen.blit(textSurface, textRect)
        # self.game.drawText(self.text, self.textSize, BLACK, self.pos[0], self.pos[1])

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
        prevcol = self.game.screen.get_at((int(self.pos[0]+1), int(self.pos[1]+1)))
        # print(prevcol)
        # mouseDown = False
        # for events in pg.event.get():
        #     if events.type == pg.MOUSEBUTTONUP:
        #         mouseDown = True
        colchange = False
        if self.rect.center[0] - self.width/2 <= move[0] <= self.rect.center[0] + self.width/2 and \
            self.rect.center[1] - self.height/2 <= move[1] <= self.rect.center[1] + self.height/2:
            # print("OVER")
            if prevcol[0:3] != self.highlightColour:
                self.image.fill(self.highlightColour)
                colchange = True
                # self.image = pg.draw.rect(self.game.screen, self.highlightColour, self.rectDimensions , 0)
                # self.game.screen.fill(self.highlightColour, (self.pos[0]-self.width, self.pos[1]-self.height, self.width, self.height))
                # self.game.drawText(self.text, self.textSize, BLACK, self.pos[0], self.pos[1])
            if pg.mouse.get_pressed()[0] == 1:
                self.clicked = True
        else:
            if prevcol[0:3] != self.solidColour:
                # self.image = pg.draw.rect(self.game.screen, self.solidColour, self.rectDimensions , 0)
                # self.game.screen.fill(self.solidColour, (self.pos[0]-self.width, self.pos[1]-self.height, self.width, self.height))
                self.image.fill(self.solidColour)
                colchange = True
        if colchange or self.first:
            if self.first:
                self.first = False
            self.game.screen.blit(self.image, self.rect)
            self.game.drawText(self.text, self.textSize, BLACK, self.pos[0], self.pos[1])
            # self.drawTextToButton(self.text, self.textSize, self.pos[0], self.pos[1], BLACK, self.image)
            print("text drawn", self.tag)


    def update(self):
        self.highlight()
        # if self.clicked:
        #     for button in self.game.buttons:
        #         if button != self:
        #             button.kill()

    def draw(self):
        pass
