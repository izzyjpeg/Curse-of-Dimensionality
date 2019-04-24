# import everything
import os, pygame, random, time, sys
from pygame.locals import *

main_dir = os.path.split(os.path.abspath(__file__))[0]

# set up screen and data
class Data(object):
    def __init__(self):
        self.screenRect = Rect(0, 0, 1000, 700)
        self.screenSurf = pygame.display.set_mode((1000, 700))
        
        self.width = self.screenRect[2]
        self.height = self.screenRect[3]
        self.margin = [25, 25]
        
        # game state info
        self.gameOver = False
        self.showCollectPrizes = False
        self.messages = {"dessertScore" : "Total Treats Consumed: ", \
                         "bobaScore" : "Bobas Consumed: ", \
                         "hit count" : "Hits taken: ", \
                         "game over" : "Oh no, you ate too much! Game over :(", \
                         "collect prizes" : "Collect your prizes!", \
                         "prizes" : "You earned these prizes:", \
                         "back" : "Back to the map", \
                         "no message" : ""}
        self.values = {"dessertScore" : 0, "bobaScore" : 0, "hit count" : 0, \
                       "prizes": [0, " cakes and ",  0, " bobas!"]}

        self.playerPos = (self.width // 2, self.height - self.margin[1])
        self.messageX = self.width - self.margin[0] - 200
        self.messageY = self.height // 10
        
        self.scorePos = (self.messageX, self.messageY)        
        self.scorePos2 = (self.messageX, self.messageY + 60)
        self.playerHitCountPos = (self.messageX, self.messageY + 120)
        self.buttonPos = (self.screenRect.centerx, self.screenRect.centery + self.margin[1])
        self.buttonPos2 = (self.screenRect.centerx, self.screenRect.centery + self.margin[1] + 10)
        
        # colors
        self.black = (0, 0, 0)
        self.grey = (176, 169, 178)
        self.white = (250, 250, 250)
        
data = Data()

# player class
class Player(object):
    def __init__(self, image):
        self.speed = [50, 0]
        self.image = image
        self.flipImage = pygame.transform.flip(self.image, 1, 0)
        self.facing = -1
        
        self.size = self.image.get_size()
        self.pos = data.playerPos
        self.rect = self.image.get_rect(midbottom = self.pos)
        
    # move player based on input direction (left or right)
    def move(self, direction):
        if direction:
            self.facing = direction
        self.rect.move_ip(direction * self.speed[0], 0)
        # use left or right-facing image
        if direction < 0:
            self.image = self.image
        elif direction > 0:
            self.image = self.flipImage
        
    def draw(self):
        data.screenSurf.blit(self.image, self.rect.center)
    
    # controls where the fork originates
    def forkPos(self):
        forkPos = self.rect.centerx
        return forkPos, self.rect.centery
        
    def collisionCheck(self, other):
        return self.rect.colliderect(other.rect)
            
# basic obstacle: cake
class Dessert(object):
    images = []
    def __init__(self):
        self.image = self.images[0]
        self.rect = self.image.get_rect(topright = (0,0))
        self.speed = [random.randint(1, 25), random.randint(0,5)]
        self.hit = False
        
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
        data.screenSurf.blit(self.image, self.rect.center)

# faster obstacle: boba
class Boba(Dessert):
    def __init__(self):
        super().__init__()
        self.image = self.images[1]
        self.speed = [random.randint(5, 18), random.randint(8, 25)]
            
# bullet class
class Fork(object):
    images = []
    def __init__(self, pos):
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom = pos)
        self.speed = [0, -20]
        self.hit = False

    def update(self):
        self.rect.move_ip(self.speed[0], self.speed[1])
    
    def draw(self):
        data.screenSurf.blit(self.image, self.rect.midbottom)
        
    def collisionCheck(self, other):
        return self.rect.colliderect(other.rect)

# message class: derived from button class, see 'code cited' section
class Message(object):
    def __init__(self, msg, location, orientation, mode, alwaysShown=True):
        self.color = data.white
        self.bg, self.fg = data.white, data.black
        self.mode = mode
        self.font = pygame.font.Font(None, 36)
        self.msg = data.messages[msg]

        self.alwaysShown = alwaysShown

        self.size = self.font.size(str(self.msg))
        self.msgSurf = self.font.render(self.msg, 1, self.fg)
        self.msgRect = self.msgSurf.get_rect(center = [s//2 for s in self.size])

        self.surface = pygame.surface.Surface(self.size)
        if orientation == "midtop":
            self.rect = self.surface.get_rect(midtop = location)
        elif orientation == "topleft":
            self.rect = self.surface.get_rect(topleft = location)
        elif orientation == "center":
            self.rect = self.surface.get_rect(center = location)
        elif orientation == "topright":
            self.rect = self.surface.get_rect(topright = location)

    def draw(self):
        self.surface.fill(self.bg)
        self.surface.blit(self.msgSurf, self.msgRect)
        data.screenSurf.blit(self.surface, self.rect)

# button class,  see 'code cited' section
class Button(Message):
    def __init__(self, msg, location, orientation, mode):
        super().__init__(msg, location, orientation, mode)
    def draw(self):
        self.mouseover()
        pygame.draw.rect(data.screenSurf, data.black, self.rect, 4)
        super().draw()
    def mouseover(self):
        self.bg = self.color
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.bg = data.grey
    def mouseClick(self):
        mousePos = pygame.mouse.get_pos()
        buttonPos = self.rect
        if (buttonPos.left < mousePos[0] < buttonPos.right) and \
            (buttonPos.top < mousePos[1] < buttonPos.bottom):
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
        pygame.draw.rect(data.screenSurf, data.black, self.rect, 2)

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
        

# helper functions to load images
def load_image(name):
    path = os.path.join(main_dir, 'images', name)
    return pygame.image.load(path).convert_alpha()
def load_images(*files):
    imgs = []
    for file in files:
        imgs.append(load_image(file))
    return imgs

# main game function
def main(petImg):
    pygame.init()
    
    # load images
    background = load_image('background.jpg')
    
    playerImg = pygame.transform.smoothscale(load_image(petImg), (150, 150))
    
    dessertImgs = [load_image('cake.png'), load_image('boba.png')]
    Dessert.images = dessertImgs
    
    forkImg = [load_image('fork.png')]
    Fork.images = forkImg

    # scale the background image so that it fills the window and
    # successfully overwrites the old sprite position.
    #background = pygame.transform.scale2x(background)
    data.screenSurf.blit(background, (0, 0))
    pygame.display.flip()
    
    # create clock to keep track of time
    clock = pygame.time.Clock()

    # group sprites
    desserts = set()
    forks = set()
    messages = set()
    
    # create player
    player = Player(playerImg)
     
    # create score
    if pygame.font:
        backButton = Button("back", (data.margin[0], data.margin[1]), "topleft", 4)
        dessertScore = TextBox("dessertScore", data.scorePos, "topleft", 4)
        bobaScore = TextBox("bobaScore", data.scorePos2, "topleft", 4)
        playerHitCount = TextBox("hit count", data.playerHitCountPos, "topleft", 4)
        messages.update([dessertScore, bobaScore, playerHitCount])
        # game over
        gameOverBox = MessageBox("game over", data.screenRect.center, "center", 4)
        collectPrizesButton = Button("prizes", data.buttonPos, "center", 4)
        # collect prizes
        collectPrizesBox = MessageBox("no message", data.screenRect.center, "center", 4)
        prizes = TextBox("prizes", data.screenRect.center, "center", 4)
        backToGameButton = Button("back", data.buttonPos2, "center", 4)
        
    # timer to create pastries every 3 sec
    pygame.time.set_timer(USEREVENT, 3000)
    bobaTime = 0
    
    ### Game Loop ###
    going = True
    while going:
        clock.tick(60)
        
        # event queue
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
                
            elif event.type == KEYDOWN:
                # move left or right
                if event.key == K_LEFT:
                    player.move(-1)
                elif event.key == K_RIGHT:
                    player.move(1)
                # shoot a fork
                elif event.key == K_SPACE:
                    fork = Fork(player.forkPos())
                    forks.add(fork)
                # force game over
                elif event.key == K_q:
                    data.values.hitCount = 6
                
            # create pastry, called every second
            elif event.type == USEREVENT:
                bobaTime += 1
                dessert = Dessert()
                desserts.add(dessert)
                if bobaTime % 3 == 0:
                    boba = Boba()
                    desserts.add(boba)
                    
            # mouse click for the buttons
            elif event.type == MOUSEBUTTONDOWN:
                if backButton.mouseClick():
                    return
                elif collectPrizesButton.mouseClick():
                    data.showCollectPrizes = True
                elif backToGameButton.mouseClick():
                    return (data.values["dessertScore"], data.values["bobaScore"])
        
        # detect collisions
        newDesserts, newForks = set(), set()
        for fork in forks:
            for dessert in desserts:
                if fork.collisionCheck(dessert):
                    dessert.hit = True
                    fork.hit = True
                    data.values["dessertScore"] += 1
                    if isinstance(dessert, Boba):
                        data.values["bobaScore"] += 1
        for dessert in desserts:
            if player.collisionCheck(dessert):
                dessert.hit = True
                data.values["hit count"] += 1
        for fork in forks:
            if (not fork.hit) and not (fork.rect.bottom < 0):
                newForks.add(fork)
        for dessert in desserts:
            if not dessert.hit:
                newDesserts.add(dessert)
        desserts = newDesserts
        forks = newForks
        
        # update all sprites
        for dessert in desserts:
            dessert.update()
        for fork in forks:
            fork.update()
        dessertScore.update()
        bobaScore.update()
        
        data.values["prizes"][0] = data.values["dessertScore"]
        data.values["prizes"][2] = data.values["bobaScore"]
        
        prizes.update()
        playerHitCount.update()
        
        # draw all sprites
        data.screenSurf.blit(background, (0, 0))
        for dessert in desserts:
            dessert.draw()
        for fork in forks:
            fork.draw()
        for message in messages:
            message.draw()
        if data.values["hit count"] > 0:
            gameOverBox.draw()
            collectPrizesButton.draw()
        if data.showCollectPrizes:
            collectPrizesBox.draw()
            prizes.draw()
            backToGameButton.draw()
        player.draw()
        pygame.display.flip()
        
    # end of loop
    
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
