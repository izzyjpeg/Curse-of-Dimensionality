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
        self.score = 0
        self.scoreMsg = "Treats Consumed: "
        self.playerHitCount = 0
        self.playerHitCountMsg = "Hits taken: "

        self.playerPos = (self.width // 2, self.height // 8 - self.margin[1])
        self.scorePos = (self.width - self.margin[0], self.height // 8)        
        self.playerHitCountPos = (self.width - self.margin[0], self.height // 8 + 20)
        
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
        self.pos = (data.width//2 - self.size[0]//2, data.height - self.size[1]//2 - data.margin[1])
        self.rect = self.image.get_rect(center = self.pos)
        
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
            
#obstacle class
class Pastry(object):
    images = []
    def __init__(self):
        self.image = random.choice(self.images)
        self.rect = self.image.get_rect(topright = (0,0))
        self.speed = [random.randint(1, 25), random.randint(1,25)]
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
        if self.rect.bottom <= data.screenRect.top:
            self.kill()
    
    def draw(self):
        data.screenSurf.blit(self.image, self.rect.midbottom)
        
    def collisionCheck(self, other):
        return self.rect.colliderect(other.rect)

# message class
class Message():
    def __init__(self, msg, location, orientation, mode):
        self.bg, self.fg = data.white, data.black
        self.mode = mode
        self.font = pygame.font.Font(None, 36)
        self.msg = msg

        self.size = self.font.size(self.msg)
        self.msgSurf = self.font.render(self.msg, 1, self.fg)
        self.msgRect = self.msgSurf.get_rect(center = [s//2 for s in self.size])

        self.surface = pygame.surface.Surface(self.size)
        if orientation == "center":
            self.rect = self.surface.get_rect(center = location)
        elif orientation == "topleft":
            self.rect = self.surface.get_rect(topleft = location)
        elif orientation == "topright":
            self.rect = self.surface.get_rect(topright = location)
            
    def update(self, newMsg):
        self.msg = newMsg

    def draw(self):
        self.surface.fill(self.bg)
        self.surface.blit(self.msgSurf, self.msgRect)
        data.screenSurf.blit(self.surface, self.rect)

# draw game over screen
class GameOverBox():
    def __init__(self):
        self.width, self.height = 300, 100
        self.x = data.width//2
        self.y = data.height//2
        self.text = "Oh no, you ate too much! Game Over!"
        self.textColor = data.black
        self.bgColor = data.white
        self.font = pygame.font.Font(None, 30)
        
    def draw(self):
        self.size = self.font.size(self.text)
        self.textSurf = self.font.render(self.text, 1, self.textColor)
        self.textRect = self.textSurf.get_rect(center = (self.x, self.y))
        
        self.surface = pygame.surface.Surface((self.size[0] + data.margin[0], self.size[1] + data.margin[1]))
        self.rect = self.surface.get_rect(center = (self.x, self.y))
        
        self.surface.fill(self.bgColor)
        self.surface.blit(self.textSurf, self.textRect)
        data.screenSurf.blit(self.surface, self.rect)

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
    
    playerImg = load_image(petImg)
    
    pastryImgs = [load_image('cake.png'), load_image('boba.png')]
    Pastry.images = pastryImgs
    
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
    pastries = set()
    forks = set()
    messages = []
    
    # create player
    player = Player(playerImg)
    
    # create score
    if pygame.font:
        score = Message(data.scoreMsg, data.scorePos, "topright", 0)
        playerHitCount = Message(data.playerHitCountMsg, data.playerHitCountPos, "topright", 0)
        messages += [score, playerHitCount]
        gameOverBox = GameOverBox()
        
    # timer to create pastries every 600 ms
    pygame.time.set_timer(USEREVENT, 2000)
    
    # game loop
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
                # back to main game
                elif event.key == K_q:
                    print("quitting")
                    going = False
                    pygame.quit()
                
            # create pastry, called every second
            elif event.type == USEREVENT:
                pastry = Pastry()
                pastries.add(pastry)
        
        # detect collisions
        newPastries, newForks = set(), set()
        for fork in forks:
            for pastry in pastries:
                if fork.collisionCheck(pastry):
                    pastry.hit = True
                    fork.hit = True
                    data.score += 1
        for pastry in pastries:
            if player.collisionCheck(pastry):
                pastry.hit = True
                data.playerHitCount += 1
        for fork in forks:
            if not fork.hit:
                newForks.add(fork)
        for pastry in pastries:
            if not pastry.hit:
                newPastries.add(pastry)
        pastries = newPastries
        forks = newForks
        
        # update all sprites
        for pastry in pastries:
            pastry.update()
        for fork in forks:
            fork.update()
        #score.update(str(data.scoreMsg + str(data.score)))
        #playerHitCount.update(str(data.playerHitCountMsg + str(data.playerHitCount)))
        
        # draw all sprites
        data.screenSurf.blit(background, (0, 0))
        for pastry in pastries:
            pastry.draw()
        for fork in forks:
            fork.draw()
        for message in messages:
            message.draw()
        if data.playerHitCount > 5:
            gameOverBox.draw()
        player.draw()
        pygame.display.flip()
        
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
