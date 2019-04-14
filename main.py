# import everything
import os, pygame, random, time
from pygame.locals import *

main_dir = os.path.split(os.path.abspath(__file__))[0]

# set up screen and data
screen = Rect(0, 0, 1000, 750)
class Data(object):
    def __init__(self):
        self.width = screen[2]
        self.height = screen[3]
        self.score = 0
        
        # game over info
        self.gameOver = False
        self.boxWidth, self.boxHeight = 200, 100
        self.x1, self.y1 = self.width//2 - self.boxWidth, self.height//2 + self.boxHeight
data = Data()

# draw game over screen
def drawGameOver(screen):
    boxRect = pygame.Rect(data.x1, data.y1, data.boxWidth, data.boxHeight)
    pygame.draw.rect(screen, (0, 0, 0), boxRect)

# player class
class Kewpie(pygame.sprite.Sprite):
    speed = [25, 5]
    bounce = 10
    images = []
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom = screen.midbottom)
        self.origtop = self.rect.top
        self.facing = -1
    
    # move Kewpie based on input direction (left or right)
    def move(self, direction):
        if direction:
            self.facing = direction
        self.rect.move_ip(direction*self.speed[0], 0)
        self.rect = self.rect.clamp(screen)
        # use left or right-facing image
        if direction < 0:
            self.image = self.images[0]
        elif direction > 0:
            self.image = self.images[1]
        self.rect.top = self.origtop - (self.rect.left//self.bounce%2)
            
#obstacle class
class Pastry(pygame.sprite.Sprite):
    speed = [5, 5]
    images = []
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = random.choice(self.images)
        self.rect = self.image.get_rect(midbottom = screen.midbottom)
        self.facing = random.choice((-1,1)) * self.speed[0]
        if self.facing < 0:
            self.rect.right = screen.right
        
    def update(self):
        self.rect.move_ip(self.speed[0], self.speed[1])
        # check if pastries have gone offscreen
        if not screen.contains(self.rect):
            #self.facing = -self.facing;
            if (self.rect.right > screen.right) or (self.rect.left < 0):
                self.speed[0] *= (-1)
            if (self.rect.bottom > screen.bottom) or (self.rect.top < 0):
                self.speed[1] *= (-1)
            #self.rect.top = self.rect.bottom + 1
            #self.rect = self.rect.clamp(screen)
            
# bullet class
class Fork(pygame.sprite.Sprite):
    speed = [0, -15]
    images = []
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom = screen.midbottom)

    def update(self):
        self.rect.move_ip(self.speed[0], self.speed[1])
        if self.rect.bottom <= 0:
            self.kill()

# helper functions to load images
def load_image(name):
    path = os.path.join(main_dir, 'images', name)
    return pygame.image.load(path).convert_alpha()
def load_images(*files):
    imgs = []
    for file in files:
        imgs.append(load_image(file))
    return imgs

def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 750))
    start = time.time()
    
    # load images
    background = load_image('background.jpg')
    
    kewpieImgs = load_image('kewpieleft.png')
    Kewpie.images = [kewpieImgs, pygame.transform.flip(kewpieImgs, 1, 0)]
    
    pastryImgs = [load_image('cake.png'), load_image('boba.png')]
    Pastry.images = pastryImgs
    
    forkImg = [load_image('fork.png')]
    Fork.images = forkImg

    # scale the background image so that it fills the window and
    # successfully overwrites the old sprite position.
    #background = pygame.transform.scale2x(background)
    screen.blit(background, (0, 0))
    pygame.display.flip()
    
    # create clock to keep track of time
    clock = pygame.time.Clock()

    # initialize sprites
    pastries = pygame.sprite.Group()
    
    forks = pygame.sprite.Group()
    players = pygame.sprite.GroupSingle()
    allsprites = pygame.sprite.OrderedUpdates(())
    Kewpie.containers = allsprites, players
    Pastry.containers = allsprites, pastries
    Fork.containers = allsprites, forks
    
    # create player
    player = Kewpie()
    
    # timer to create pastries every 200 ms
    pygame.time.set_timer(USEREVENT, 1000)
    
    # game loop
    going = True
    while going:
        clock.tick(60)
        
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
                fork = Fork(player.rect.top)
                allsprites.add(fork)
                
            # create pastry, called every second
            elif event.type == USEREVENT:
                pastry = Pastry()
                allsprites.add(pastry)
                screen.blit(pastry.image, (pastry.rect[0],pastry.rect[1]))
        
        # detect collisions
        # pastry / player collisions
        for pastry in pygame.sprite.spritecollide(player, pastries, 1):
            #data.score += 1
            #player.kill()
            data.gameOver = True
        # pastry / fork collisions
        for pastry in pygame.sprite.groupcollide(forks, pastries, 1, 1).keys():
            #boom_sound.play()
            #Explosion(alien)
            data.score += 1
            print(data.score)
        
        
        # update all sprites
        allsprites.update()
        
        # draw all sprites
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pygame.display.flip()
        
        # if game over
        if data.gameOver:
            drawGameOver(screen)
        
    pygame.quit()

if __name__ == '__main__':
    main()
