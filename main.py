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
        self.margin = [25, 25]

data = Data()

# helper functions to load images
def load_image(name):
    path = os.path.join(main_dir, 'images', name)
    return pygame.image.load(path).convert_alpha()
def load_images(*files):
    imgs = []
    for file in files:
        imgs.append(load_image(file))
    return imgs

# pet class
class Pet(pygame.sprite.Sprite):
    images = []
    def __init__(self, name, color, numEyes, numLegs, faveFood):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom = screen.midbottom)

        # individual pet characteristics
        self.name = name
        self.color = color
        self.numEyes = numEyes
        self.numLegs = numLegs
        self.faveFood = faveFood

    def __eq__(self, other):
        return (isinstance(other, Pet) and (self.color == other.color) \
                and (self.name == other.name) \
                and (self.numEyes == other.numEyes) \
                and (self.numLegs == other.numLegs) \
                and (self.faveFood == other.faveFood))

    def __repr__(self):
        print("%s is a %s creature with %d eyes and %d legs. It likes to eat %s." % self.name, \
                self.color, self.numEyes, self.numLegs, self.faveFood)

    def getHashables():
        return (self.name, self.color, self.numEyes, self.numLegs, self.faveFood)

    def __hash__(self):
        return hash(getHashables())


# main game function
def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 750))
    start = time.time()

    # load images
    background = load_image('background.jpg')
    petImages = load_images('cat.png', 'bunny.png')
    Pet.images = petImages

    # display background
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # create clock to keep track of time
    clock = pygame.time.Clock()

    # initialize sprites
    allsprites = pygame.sprite.OrderedUpdates(())
    Pet.containers = allsprites

    # game loop
    going = True
    while going:
        # update all sprites
        allsprites.update()

        # draw all sprites
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()