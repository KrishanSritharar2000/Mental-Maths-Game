import pygame as pg
from settings import *

vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.allSprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.width = 30
        self.height = 30
        self.image = pg.Surface((self.width, self.height))
        self.image.fill(YELLOW)
        # self.image = self.game.playerBikeImage.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.pos = vec(x,y)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.direction = "forward"
        self.last = 0
        self.braking = False

    def jump(self):
        self.vel.y = -20

    def collideWalls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.x > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.y > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.y

    def collideWithWalls(self, dir):
        hitWall = pg.sprite.spritecollide(self.game.player, self.game.walls, False)
        if hitWall:
            if dir == "x":
                if self.game.player.vel.x > 0:#going to the right  [hit left of wall]
                    self.game.player.pos.x = hitWall[0].rect.left - self.game.player.width / 2
                elif self.game.player.vel.x < 0:#going to the left [hit right of wall]
                    self.game.player.pos.x = hitWall[0].rect.right + self.game.player.width / 2
                self.game.player.vel.x = 0
                self.rect.centerx = self.pos.x

            if dir == "y":
                if self.game.player.vel.y > 0:#going down [hit top of wall]
                    self.game.player.pos.y = hitWall[0].rect.top - self.rect.height / 2
                elif self.game.player.vel.y < 0:#going up [hit bottom of wall]
                    self.game.player.pos.y = hitWall[0].rect.bottom + self.game.player.height / 2
                self.game.player.vel.y = 0
                self.rect.centery = self.pos.y

    def update(self):
        if self.game.sceneMan.showPlayer == True:
            # print("Moving Player")

            self.acc = vec(0, PLAYER_GRAV)
            keys = pg.key.get_pressed()

            if keys[pg.K_RIGHT] or keys[pg.K_d]:
                if self.direction == "forward" or self.direction == "stopped":
                    if self.braking == False:
                        self.acc.x = PLAYER_ACC
                        self.direction = "forward"

            if keys[pg.K_LEFT] or keys[pg.K_a]:
                if self.direction == "reverse" or self.direction == "stopped":
                    if self.braking == False:
                        self.acc.x = -PLAYER_ACC
                        self.direction = "reverse"

            if abs(self.vel.x) < 0.5:
                self.direction = "stopped"

            if keys[pg.K_DOWN] or keys[pg.K_s]:
                if self.direction != "stopped":
                    if self.vel.x > 0:
                        self.acc.x = -BRAKE_ACC
                    else:
                        self.acc.x = BRAKE_ACC
                self.braking = True
            else:
                self.braking = False
            # #Debug Motion
            # now = pg.time.get_ticks()
            # if now - self.last > 150:
            #     self.last = now
                # print("{} direction  Velocity X: {} Acceleration X: {}".format(self.direction, round(self.vel.x,0), round(self.acc.x, 0)))
                # print("                   Velocity Y: {} Acceleration Y: {}".format(round(self.vel.y,0), round(self.acc.y, 0)))

            self.acc += self.vel * PLAYER_FRICTION
            self.vel += self.acc
            self.pos += self.vel + 0.5 * self.acc
            self.rect.centerx = self.pos.x
            self.collideWithWalls('x')
            self.rect.centery = self.pos.y
            self.collideWithWalls('y')

            # self.pos = self.rect.center


class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height, colour, mode="platform"):
        self.groups = game.allSprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((width, height))
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        if mode == "platform":
            self.rect.x, self.rect.y = x * TILESIZE, y * TILESIZE
        elif mode == "track":
            self.rect.x, self.rect.y = x, y

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y, colour=None, altColour=None, mode=None, width=None, height=None):
        if mode == "tiled":
            self.groups = game.walls
            pg.sprite.Sprite.__init__(self, self.groups)
            self.rect = pg.Rect(x, y, width, height)
            self.rect.x, self.rect.y = x, y
        else:
            if mode == "end":
                self.groups = game.allSprites, game.endWalls
            else:
                self.groups = game.allSprites, game.walls
            pg.sprite.Sprite.__init__(self, self.groups)
            self.image = pg.Surface((TILESIZE, TILESIZE))
            if mode != "end":
                self.image.fill(colour)
            else:
                self.image.fill(altColour)
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = x * TILESIZE, y * TILESIZE

class Rectangle(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height, colour):
        self.groups = game.allSprites, game.rectangles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((width, height))
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

        # self.image = pg.draw.rect(game.screen, colour, (x, y, width, height))
        # self.rect = self.image.get_rect()

class Track(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height, colour):
        self.groups = game.allSprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((width, height))
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x , y

class WallFile(pg.sprite.Sprite):#This is so the sizes are not multiped by TILESIZE as only one pixel is needed
    def __init__(self, game, x, y, width, height, colour):
        self.groups = game.allSprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((width, height))
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

class Question(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.allSprites, game.questionItems
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.allSprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((30,30))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class InputBox(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height, text='', textSize=32, fontName=None):
        self.groups = game.allSprites, game.userInputBox
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, width, height)
        self.colour = RED
        self.text = text
        if fontName == None:
            self.font = pg.font.SysFont(None, textSize)
        else:
            self.font = pg.font.Font(fontName, textSize)
        self.textSurf = self.font.render(text, True, self.colour)
        self.boxActive = False

    def inputKeys(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.boxActive = not self.boxActive
            else:
                self.boxActive = False
            if self.boxActive:
                self.colour = GREEN
            else:
                self.colour = RED
        if event.type == pg.KEYDOWN:
            if self.boxActive:
                if event.key == pg.K_RETURN:
                    print("This is the text: {}".format(self.text))
                    if self.game.sceneMan.currentScene == 'levelComplete':
                        self.game.sceneMan.updateHighscore(self.game.sceneMan.nextLevelTagNumber-1, self.game.score)
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                print(self.text)
                self.game.screen.fill(WHITE, (WIDTH*5/8, HEIGHT*7/11, self.rect.width+10, 32))
                self.textSurf = self.font.render(self.text, True, self.colour)

    def update(self):
        newWidth = max(150, self.textSurf.get_width()+10)
        self.rect.width = newWidth

    def draw(self, surf):
        surf.blit(self.textSurf, (self.rect.x+5, self.rect.y+5))
        pg.draw.rect(surf, self.colour, self.rect, 2)

class Button(pg.sprite.Sprite):
    def __init__(self, game, tag, x, y, width, height, solidColour, highlightColour, text, textSize=None, solidButtonImage=None, highlightButtonImage=None):
        self.groups = game.buttons
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.tag = tag
        self.width = width
        self.height = height
        self.solidColour = solidColour
        self.highlightColour = highlightColour
        self.text = text
        if textSize == None:
            self.textSize = int(width/(len(text)*0.45))
            # print("Text Size {} for {}".format(self.textSize, self.tag))
            if self.textSize > 24:
                self.textSize = 24
        else:
            self.textSize = textSize
        self.pos = vec(x,y)
        self.rectDimensions = (self.pos[0]-self.width/2, self.pos[1]-self.height/2, self.width, self.height)
        # self.image = pg.draw.rect(self.game.screen, self.solidColour, self.rectDimensions , 0)
        if solidButtonImage == None:
            self.solidImage = pg.transform.scale(self.game.menuButtonSolid,(int(self.width), int(self.height)))
            self.highlightImage = pg.transform.scale(self.game.menuButtonHighlight,(int(self.width), int(self.height)))

        else:
            self.solidImage = pg.transform.scale(solidButtonImage,(int(self.width), int(self.height)))
            self.highlightImage = pg.transform.scale(highlightButtonImage,(int(self.width), int(self.height)))
        self.image = self.solidImage
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.clicked = False
        self.colchange = False
        self.first = True

    def highlight(self):
        mousePos = pg.mouse.get_pos()
        # prevcol = self.game.screen.get_at((int(self.pos[0]-self.width/2), int(self.pos[1]-self.height/2)))
        if self.pos[0] - self.width/2  <= mousePos[0] <= self.pos[0] + self.width/2 and \
            self.pos[1] - self.height/2 <= mousePos[1] <= self.pos[1] + self.height/2:
            if self.image != self.highlightImage:
                # self.image = pg.draw.rect(self.game.screen, self.highlightColour, self.rectDimensions , 0)
                self.image = self.highlightImage
                self.colchange = True
            if pg.mouse.get_pressed()[0] == 1:
                self.clicked = True
        else:
            if self.image != self.solidImage:
                # self.image = pg.draw.rect(self.game.screen, self.solidColour, self.rectDimensions , 0)
                self.image = self.solidImage
                self.colchange = True


    def update(self):
        self.highlight()
        if self.clicked:
            for button in self.game.buttons:
                if button != self:
                    button.kill()

    def draw(self, surface):
        if self.colchange == True or self.first == True:
            surface.blit(self.image,self.rect)
            print("drawn this button", self.tag)
            if self.first:
                # print(self.first, "self.first")
                self.first = False
            self.game.drawText(self.text, self.textSize, BLACK, self.pos[0], self.pos[1], surf=surface)
            self.colchange = False
