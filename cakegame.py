# import everything
import os, pygame, random, time, sys, copy
from pygame.locals import *

main_dir = os.path.split(os.path.abspath(__file__))[0]

# helper functions to load images
def load_image(name):
    path = os.path.join(main_dir, 'images', name)
    return pygame.image.load(path).convert_alpha()
def load_images(*files):
    imgs = []
    for file in files:
        imgs.append(load_image(file))
    return imgs

# set up screen and data
class Data(object):
    def __init__(self):
        self.screenRect = Rect(0, 0, 1000, 750)
        self.screenSurf = pygame.display.set_mode((1000, 750))
        
        self.width = self.screenRect[2]
        self.height = self.screenRect[3]
        self.margin = [25, 25]
        
        # game state info
        self.gameOver = False
        self.showCollectPrizes = False
        self.showGameOver = True
        self.messages = {"dessertScore" : "Cakes Consumed: ", \
                         "bobaScore" : "Bobas Consumed: ", \
                         "donutScore" : "Donuts Consumed: ", \
                         "hit count" : "Hits taken (out of 5): ", \
                         "game over" : "Oh no, you ate too much! Game over :(", \
                         "collect prizes" : "Collect your prizes!", \
                         "prizes" : "You earned these prizes:", \
                         "back" : "Quit", \
                         "back to game" : "Back to the map", \
                         "no message" : ""}
        self.values = {"dessertScore" : 0, "bobaScore" : 0, "donutScore" : 0, \
                       "hit count" : 0, \
                       "prizes": [0, " cakes, ",  0, " bobas, and ", 0, " donuts!"]}
        self.bobaHits = 3
        self.minDonutR = 50
        self.desserts = set()
        
        # predefined coordinates
        self.playerPos = (self.width // 2, self.height - self.margin[1])
        self.messageX = self.width - self.margin[0] - 200
        self.messageY = self.height // 10
        self.scorePad = self.height // 11
        self.scorePos = (self.messageX, self.messageY)        
        self.scorePos2 = (self.messageX, self.messageY + self.scorePad) 
        self.scorePos3 = (self.messageX, self.messageY + self.scorePad*2)
        self.playerHitCountPos = (self.messageX, self.messageY + self.scorePad*3)
        self.buttonPos = (self.screenRect.centerx, self.screenRect.centery + self.margin[1])
        self.buttonPos2 = (self.screenRect.centerx, self.screenRect.centery + self.margin[1] + 10)
        
        # bg image info
        self.bgWidth = 1074
        self.bgX = (self.bgWidth - self.screenRect.width) * (-1)
        
        # images
        self.dessertImages = [pygame.transform.smoothscale(load_image('cake.png'), (150, 150)), \
                              pygame.transform.smoothscale(load_image('boba.png'), (77, 160)), \
                              pygame.transform.smoothscale(load_image('donut.png'), (200, 200))]
        self.forkImage = pygame.transform.smoothscale(load_image('fork.png'), (20, 100))
        
        # colors
        self.black = (0, 0, 0)
        self.grey = (176, 169, 178)
        self.white = (250, 250, 250)
        self.pink = (255, 129, 231)
        self.blue = (120, 169, 255)
        
data = Data()

# player class
class Player(object):
    def __init__(self, image):
        self.speed = [50, 50]
        self.image = image
        self.flipped = False
        self.flippedImage = pygame.transform.flip(self.image, 1, 0)
        
        self.size = self.image.get_size()
        self.rect = self.image.get_rect()
        self.rect.midbottom = data.playerPos
        
    # move player based on input direction (left or right)
    def move(self, dx, dy):
        # use left or right-facing image
        if dx < 0:
            self.flipped = False
        elif dx > 0:
            self.flipped = True
        
        x = dx * self.speed[0]
        y = dy * self.speed[1]
        self.rect.move_ip(x, y)
        
    def draw(self):
        if self.flipped:
            data.screenSurf.blit(self.flippedImage, self.rect)
        else:
            data.screenSurf.blit(self.image, self.rect)
    
    # controls where the fork originates
    def forkPos(self):
        return self.rect.centerx, self.rect.centery
        
    def collisionCheck(self, other):
        return self.rect.colliderect(other.rect)
            
# basic obstacle: cake
class Dessert(object):
    def __init__(self):
        self.image = data.dessertImages[0]
        self.rect = self.image.get_rect(bottomright = (0,0))
        self.speed = [random.randint(5, 20), random.randint(2,5)]
        self.hits = 0
        self.hitPlayer = False
        
    def update(self):
        # check if pastries have gone offscreen, bounce and return to rect
        if not data.screenRect.contains(self.rect):
            if (self.rect.right > data.screenRect.right) or (self.rect.left < 0):
                self.speed[0] *= (-1)
                if self.rect.right > data.screenRect.right:
                    self.rect.right = data.screenRect.right
                elif self.rect.left < 0:
                    self.rect.left = 0
            if (self.rect.bottom > data.screenRect.bottom) or (self.rect.top < 0):
                self.speed[1] *= (-1)
                if self.rect.bottom > data.screenRect.bottom:
                    self.rect.bottom = data.screenRect.bottom
                elif self.rect.top < 0:
                    self.rect.top = 0
        self.rect.move_ip(self.speed[0], self.speed[1])
    
    def draw(self):
        data.screenSurf.blit(self.image, self.rect.topleft)

# shrinking obstacle: boba
class Boba(Dessert):
    def __init__(self):
        super().__init__()
        self.image = data.dessertImages[1]
        self.rect = self.image.get_rect(bottomright = (0, 0))
        self.coefficient = 0.7
        
    def shrink(self):
        self.newWidth = int(self.image.get_width() * self.coefficient)
        self.newHeight = int(self.image.get_height() * self.coefficient)
        self.image = pygame.transform.smoothscale(self.image, (self.newWidth, self.newHeight))
        self.newRect = self.image.get_rect()
        self.x, self.y = self.newRect.x, self.newRect.y
        self.rect.move_ip(self.x, self.y)
        self.rect.width, self.rect.height = self.newRect.width, self.newRect.height
        
# splitting obstacle: donut
class Donut(Boba):
    def __init__(self):
        super().__init__()
        self.image = data.dessertImages[2]
        self.rect = self.image.get_rect(bottomright = (0, 0))
        self.coefficient = 0.5
        
# bullet class
class Fork(object):
    def __init__(self, pos):
        self.image = data.forkImage
        self.rect = self.image.get_rect(midbottom = pos)
        self.speed = [0, -40]
        self.hit = False

    def update(self):
        self.rect.move_ip(self.speed[0], self.speed[1])
    
    def draw(self):
        data.screenSurf.blit(self.image, self.rect.topleft)
        
    def collisionCheck(self, other):
        return self.rect.colliderect(other.rect)
        
### THIS CODE DRAWS A ROUNDED RECTANGLE AND WAS TAKEN FROM THE FOLLOWING SOURCE:
# code by josmiley on https://www.pygame.org/project-AAfilledRoundedRect-2349-.html
def roundedRect(surface,rect,color,radius=0.4):
    rect         = Rect(rect)
    color        = Color(*color)
    alpha        = color.a
    color.a      = 0
    pos          = rect.topleft
    rect.topleft = 0,0
    rectangle    = pygame.Surface(rect.size,SRCALPHA)

    circle       = pygame.Surface([min(rect.size)*3]*2,SRCALPHA)
    pygame.draw.ellipse(circle,(0,0,0),circle.get_rect(),0)
    circle       = pygame.transform.smoothscale(circle,[int(min(rect.size)*radius)]*2)

    radius              = rectangle.blit(circle,(0,0))
    radius.bottomright  = rect.bottomright
    rectangle.blit(circle,radius)
    radius.topright     = rect.topright
    rectangle.blit(circle,radius)
    radius.bottomleft   = rect.bottomleft
    rectangle.blit(circle,radius)

    rectangle.fill((0,0,0),rect.inflate(-radius.w,0))
    rectangle.fill((0,0,0),rect.inflate(0,-radius.h))

    rectangle.fill(color,special_flags=BLEND_RGBA_MAX)
    rectangle.fill((255,255,255,alpha),special_flags=BLEND_RGBA_MIN)

    return rectangle
    
### UI ELEMENTS 
# message class: derived from button class, see 'code cited' section
class Message(object):
    def __init__(self, msg, location, orientation, mode, alwaysShown=True):
        self.color = data.white
        self.bg, self.fg = data.white, data.black
        self.margin = 10
        self.mode = mode
        self.font = pygame.font.Font(None, 36)
        self.msg = data.messages[msg]

        self.alwaysShown = alwaysShown

        self.size = self.font.size(self.msg)
        self.size = (self.size[0] + self.margin, self.size[1] + self.margin)
        self.msgSurf = self.font.render(self.msg, 1, self.fg)
        self.msgRect = self.msgSurf.get_rect(center = [s//2 for s in self.size])

        self.surface = pygame.surface.Surface(self.size)

        self.surface = pygame.surface.Surface(self.size)
        if orientation == "midtop":
            self.rect = self.surface.get_rect(midtop = location)
        elif orientation == "topleft":
            self.rect = self.surface.get_rect(topleft = location)
        elif orientation == "center":
            self.rect = self.surface.get_rect(center = location)
        elif orientation == "topright":
            self.rect = self.surface.get_rect(topright = location)
            
        self.roundRect = self.rect
        self.roundRect[2] += self.margin
        self.roundRect[3] += self.margin
        self.msgX = self.roundRect.width//2 - (self.size[0]//2) + (self.margin//2)
        self.msgY = self.roundRect.height//2 - (self.size[1]//2) + (self.margin//2)
        self.msgPos = self.msgX, self.msgY

    def draw(self):
        self.surface = roundedRect(self.surface, self.roundRect, data.white)
        self.surface.blit(self.msgSurf, self.msgPos)
        data.screenSurf.blit(self.surface, self.roundRect)

# button class,  see 'code cited' section
class Button(Message):
    def __init__(self, msg, location, orientation, mode, outline=False):
        super().__init__(msg, location, orientation, mode)
        self.outline = outline
    def draw(self):
        self.mouseover()
        super().draw()
        if self.outline:
            pygame.draw.rect(data.screenSurf, data.pink, self.rect, 2)
    def mouseover(self):
        self.bg = self.color
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.bg = data.grey
    def mouseClick(self):
        mousePos = pygame.mouse.get_pos()
        if (self.rect.left < mousePos[0] < self.rect.right) and \
            (self.rect.top < mousePos[1] < self.rect.bottom):
                return True
        else:
            return False
            
# text box class: updates based on user or game state. see 'code cited' section
class TextBox(Button):
    def __init__(self, msg, location, orientation, mode):
        super().__init__(msg, location, orientation, mode)
        self.msg = msg
        self.text = ""
        self.active = False
        self.textSurf = self.font.render(self.text, 1, data.black)
        self.desc = data.messages[msg]
        self.descFont = pygame.font.Font(None, 30)
        self.descSurf = self.descFont.render(self.desc, 1, data.black)

    def update(self):
        text = ""
        if (type(data.values[self.msg]) == list) and (len(data.values[self.msg]) > 1):
            for c in data.values[self.msg]:
                text += str(c)
            self.text = text
        else:
            self.text = str(data.values[self.msg])
            
        self.width = max(self.descSurf.get_width() + 10, self.textSurf.get_width() + 10)
        self.height = self.textSurf.get_height()
        self.rect.width = self.width

    def draw(self):
        self.surface = pygame.surface.Surface((self.width, self.height))
        self.surface.fill(self.bg)
        self.textSurf = self.font.render(self.text, 1, data.black)
        data.screenSurf.blit(self.surface, self.rect)
        data.screenSurf.blit(self.descSurf, (self.rect.x, self.rect.y - 30))
        data.screenSurf.blit(self.textSurf, (self.rect.x, self.rect.y))

# draw game over screen
class MessageBox(Message):
    def __init__(self, msg, location, orientation, mode):
        super().__init__(msg, location, orientation, mode)
        self.x = data.width//2
        self.y = data.height//2
        self.text = data.messages[msg]
        self.size = self.font.size(self.text)
        self.width = max((self.size[0]+ data.margin[0]*2), 500)
        self.height = self.size[1] + data.margin[1]*2 + 100
        
        self.rect.width, self.rect.height = self.width, self.height
        self.rect.center = (self.x, self.y)
        
        self.textSurf = self.font.render(self.text, 1, data.black)
        self.textRect = Rect(0, 0, self.size[0], self.size[1])
        self.textRect.centerx = self.rect.centerx
        self.textRect.centery = self.rect.centery - data.margin[1]
        
    def draw(self):
        self.surface = pygame.surface.Surface((self.width, self.height))
        self.surface.fill(self.bg)
        data.screenSurf.blit(self.surface, self.rect)
        data.screenSurf.blit(self.textSurf, self.textRect)
    
# main game function
def main(petImg):
    pygame.init()
    
    # load images
    background = pygame.transform.smoothscale(load_image('background.jpg'), (data.bgWidth, data.screenRect.height))
    playerImg = pygame.transform.smoothscale(load_image(petImg), (120, 120))

    # scale the background image so that it fills the window and
    # successfully overwrites the old sprite position.
    #background = pygame.transform.scale2x(background)
    data.screenSurf.blit(background, (data.bgX, 0))
    pygame.display.flip()
    
    # create clock to keep track of time
    clock = pygame.time.Clock()

    # group sprites
    forks = set()
    messages = set()
    
    # create player
    player = Player(playerImg)
     
    # create score
    if pygame.font:
        backButton = Button("back", (data.margin[0], data.margin[1]), "topleft", 4)
        dessertScore = TextBox("dessertScore", data.scorePos, "topleft", 4)
        bobaScore = TextBox("bobaScore", data.scorePos2, "topleft", 4)
        donutScore = TextBox("donutScore", data.scorePos3, "topleft", 4)
        playerHitCount = TextBox("hit count", data.playerHitCountPos, "topleft", 4)
        messages.update([backButton, dessertScore, bobaScore, donutScore, playerHitCount])
        # game over
        gameOverBox = MessageBox("game over", data.screenRect.center, "center", 4)
        collectPrizesButton = Button("prizes", data.buttonPos, "center", 4, True)
        # collect prizes
        collectPrizesBox = MessageBox("no message", data.screenRect.center, "center", 4)
        prizes = TextBox("prizes", data.screenRect.center, "center", 4)
        backToGameButton = Button("back to game", data.buttonPos2, "center", 4, True)
        
    # timer to create pastries every 3 sec
    pygame.time.set_timer(USEREVENT, 3000)
    dessertTime = 0
    
    ### Game Loop ###
    going = True
    while going:
        #clock.tick(400)
        
        # event queue
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
                
            elif event.type == KEYDOWN:
                # move left or right
                if event.key == K_LEFT:
                    if player.rect.left > 0:
                        player.move(-1, 0)
                elif event.key == K_RIGHT:
                    if player.rect.right < data.screenRect.right:
                        player.move(1, 0)
                elif event.key == K_DOWN:
                    if player.rect.bottom < data.screenRect.bottom:
                        player.move(0, 1)
                elif event.key == K_UP:
                    if player.rect.top > 0:
                        player.move(0, -1)
                # shoot a fork
                elif event.key == K_SPACE:
                    fork = Fork(player.forkPos())
                    forks.add(fork)
                
            # create pastry, called every second
            elif event.type == USEREVENT:
                dessertTime += 1
                if dessertTime % 3 == 0:
                    boba = Boba()
                    data.desserts.add(boba)
                elif dessertTime % 7 == 0:
                    donut = Donut()
                    data.desserts.add(donut)
                else:
                    dessert = Dessert()
                    data.desserts.add(dessert)
                    
            # mouse click for the buttons
            elif event.type == MOUSEBUTTONDOWN and backButton.mouseClick():
                    data.gameOver = True
                    data.showGameOver = True
                
            elif event.type == MOUSEBUTTONDOWN and backToGameButton.mouseClick() and (not data.showGameOver):
                return (data.values["dessertScore"], \
                        data.values["bobaScore"], data.values["donutScore"])
                    
            elif event.type == MOUSEBUTTONDOWN and collectPrizesButton.mouseClick():
                data.showGameOver = False
                
                data.values["prizes"][0] = data.values["dessertScore"]
                data.values["prizes"][2] = data.values["bobaScore"]
                data.values["prizes"][4] = data.values["donutScore"]
                prizes.update()
                
                if data.values["dessertScore"] == 1:
                    data.values["prizes"][1] == " cake, "                    
                elif data.values["bobaScore"] == 1:
                    data.values["prizes"][3] == " boba, and"                
                elif data.values["donutScore"] == 1:
                    data.values["prizes"][3] == " donut!"

                data.showCollectPrizes = True
                
        ### COLLISIONS
        # detect collisions
        newDesserts, newForks = set(), set()
        # fork / dessert collisions
        for fork in forks:
            for dessert in data.desserts:
                if fork.collisionCheck(dessert):
                    dessert.hits += 1
                    fork.hit = True
                    
                    # shrink bobas
                    if type(dessert) == Boba:
                        if dessert.hits >= data.bobaHits:
                            data.values["bobaScore"] += 1
                        dessert.shrink()
                        
                    # split donuts
                    elif type(dessert) == Donut:
                        dessert.shrink()
                        # create a new donut
                        donut2 = Donut()
                        donut2.rect.x = dessert.rect.x
                        donut2.rect.y = dessert.rect.y
                        donut2.update()
                        donut2.shrink()
                        donut2.speed = [dessert.speed[0]*(-1), dessert.speed[1]*(-1)]
                        data.desserts.add(donut2)
                        donut2.update()
                        
                        if dessert.image.get_width() < data.minDonutR:
                            data.values["donutScore"] += 1
                    # cake score
                    else:
                        data.values["dessertScore"] += 1
                        
                    break
                    
        # player / dessert collisions
        for dessert in data.desserts:
            if player.collisionCheck(dessert):
                dessert.hitPlayer = True
                data.values["hit count"] += 1
        for fork in forks:
            if (not fork.hit) and not (fork.rect.bottom < 0):
                newForks.add(fork)
        # add to new sets
        for dessert in data.desserts:
            if not (dessert.hitPlayer):
                # cakes
                if (dessert.hits < 1):
                    newDesserts.add(dessert)
                # bobas
                elif (type(dessert) == Boba) and (dessert.hits < data.bobaHits):
                    newDesserts.add(dessert)
                # donuts
                elif (type(dessert) == Donut) and (dessert.image.get_width() >= data.minDonutR):
                    newDesserts.add(dessert)
        data.desserts = newDesserts
        forks = newForks
        
        ### UPDATES
        # update all objects
        if not data.gameOver:
            for dessert in data.desserts:
                dessert.update()
            for fork in forks:
                fork.update()
            # update scores
            dessertScore.update()
            bobaScore.update()
            donutScore.update()

        playerHitCount.update()
        
        ### DRAW
        # draw all objects
        data.screenSurf.blit(background, (0, 0))
        if not data.gameOver:
            for dessert in data.desserts:
                dessert.draw()
            for fork in forks:
                fork.draw()
        player.draw()
        
        # draw messages 
        for message in messages:
            message.draw()
        
        # game over
        if (data.values["hit count"] > 4):
            data.gameOver = True
            if not data.showCollectPrizes:
                data.showGameOver = True
        
        if data.gameOver: 
            if data.showGameOver:
                player.rect.midbottom = data.playerPos
                gameOverBox.draw()
                collectPrizesButton.draw()
            elif data.showCollectPrizes:
                collectPrizesBox.draw()
                prizes.draw()
                backToGameButton.draw()
        
        pygame.display.flip()
        
    # end of loop
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
