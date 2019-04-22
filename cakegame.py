# import everything
import os, pygame, random, time, sys
from pygame.locals import *

main_dir = os.path.split(os.path.abspath(__file__))[0]
print(__file__)

# set up screen and data
class Data(object):
    def __init__(self):
        self.screen = Rect(0, 0, 1000, 750)
        self.screenSurf = pygame.display.set_mode((1000, 750))
        
        self.width = self.screen[2]
        self.height = self.screen[3]
        self.margin = [25, 25]
        
        # game state info
        self.gameOver = False
        self.score = 0
        
data = Data()

# player class
class Player(object):
    def __init__(self, image):
        speed = [50, 5]
        self.image = image
        self.flipImage = pygame.transform.flip(self.image, 1, 0)
        self.rect = self.image.get_rect(midbottom = data.screen.midbottom)
        self.origtop = self.rect.top
        self.facing = -1
        self.forkOffset = -5
        
    # move Kewpie based on input direction (left or right)
    def move(self, direction):
        if direction:
            self.facing = direction
        self.rect.move_ip(direction*self.speed[0], 0)
        self.rect = self.rect.clamp(data.screen)
        # use left or right-facing image
        if direction < 0:
            self.image = self.image
        elif direction > 0:
            self.image = self.flipImage
        
    def draw(self):
        self.pos = (data.width//2, data.height - data.margin[0])
        self.rect = self.image.get_rect(midbottom = self.pos)
        data.screenSurf.blit(self.image, self.pos)
    
    # controls where the fork originates
    def forkPos(self):
        pos = (self.facing * self.forkOffset) + self.rect.centerx
        return pos, self.rect.centery
            
#obstacle class
class Pastry(object):
    speed = [25, 25]
    images = []
    def __init__(self):
        self.image = random.choice(self.images)
        self.rect = self.image.get_rect(midbottom = data.screen.midbottom)
        self.facing = random.choice((-1,1)) * self.speed[0]
        if self.facing < 0:
            self.rect.right = data.screen.right
        
    def update(self):
        self.rect.move_ip(self.speed[0], self.speed[1])
        # check if pastries have gone offscreen
        if not data.screen.contains(self.rect):
            self.facing = -self.facing;
            if (self.rect.right > data.screen.right) or (self.rect.left < 0):
                self.speed[0] *= (-1)
            if (self.rect.bottom > data.screen.bottom) or (self.rect.top < 0):
                self.speed[1] *= (-1)
    
    def draw(self):
        data.screenSurf.blit(self.image, self.rect.midbottom)
            
# bullet class
class Fork(pygame.sprite.Sprite):
    speed = [0, -15]
    images = []
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom = pos)

    def update(self):
        self.rect.move_ip(self.speed[0], self.speed[1])
        if self.rect.bottom <= 0:
            self.kill()

# score class
class Score(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 36)
        #self.font = pygame.font.SysFont("maagkrampttf", 36)
        self.color = Color('white')
        self.lastscore = -1
        self.size = self.font.size("Treats Consumed: 100")
        self.x = data.width - self.size[0] - data.margin[0]
        self.y = data.width//20
        
        self.update()
        self.rect = self.image.get_rect().move(self.x, self.y)

    def update(self):
        if data.score != self.lastscore:
            self.lastscore = data.score
            msg = "Treats Consumed: %d" % data.score
            self.image = self.font.render(msg, 1, self.color)

# draw game over screen
class GameOver():
    def __init__(self):
        self.width, self.height = 300, 100
        self.x = data.width//2 - self.width
        self.y = data.height//2 - self.height
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.color = Color(white)
    def update(self):
        if data.gameOver:
            print("game is over")
            pygame.draw.rect(data.screen, self.color, self.rect, width=0)

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
    pastries = []
    forks = pygame.sprite.LayeredUpdates()
    
    # initialize sprites
    allsprites = pygame.sprite.OrderedUpdates(())
    Fork.containers = allsprites, forks
    Score.containers = allsprites
    GameOver.containers = allsprites
    
    # create player
    player = Player(playerImg)
    
    # create score
    if pygame.font:
        allsprites.add(Score())
        
    # timer to create pastries every 200 ms
    pygame.time.set_timer(USEREVENT, 200)
    
    # game loop
    going = True
    while going:
        clock.tick(20)
        
        # event queue
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            
            # move left or right
            elif event.type == KEYDOWN and event.key == K_LEFT:
                print("left")
                player.move(-1)
            elif event.type == KEYDOWN and event.key == K_RIGHT:
                print("right")
                player.move(1)
                
            # create bullets
            elif event.type == KEYDOWN and event.key == K_SPACE:
                print("space")
                fork = Fork(player.forkPos())
                allsprites.add(fork)
                
            # create pastry, called every second
            elif event.type == USEREVENT:
                pastry = Pastry()
                pastries += [pastry]
                data.screenSurf.blit(pastry.image, (pastry.rect[0],pastry.rect[1]))
        
        # detect pastry / player collisions
        #for pastry in pygame.sprite.spritecollide(player, pastries, 1):
         #   #player.kill()
          #  data.gameOver = True
            
        # detect pastry / fork collisions
        #for pastry in pygame.sprite.groupcollide(forks, pastries, 1, 1).keys():
         #   data.score += 1
        
        # update all sprites
        allsprites.update()
        for pastry in pastries:
            pastry.update()
        
        # draw all sprites
        data.screenSurf.blit(background, (0, 0))
        allsprites.draw(data.screenSurf)
        for pastry in pastries:
            pastry.draw()
        player.draw()
        pygame.display.flip()
        
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
