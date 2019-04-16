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

        self.modes = ["choosePet", "createPet", "map", "cakegame", "flappygame", "feed", "clothe"]
        self.mode = self.modes[0]

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

# title class
class Title(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 36)
        self.color = Color('white')
        self.size = self.font.size("Which pet will you choose?")
        self.x = data.width//2 - self.size[0]//2
        self.y = data.width//16

        self.update()
        self.rect = self.image.get_rect().move(self.x, self.y)

    def update(self):
        if data.mode == "choosePet":
            msg = "Which pet will you choose?"
            self.image = self.font.render(msg, 1, self.color)


# pet class
class Pet(pygame.sprite.Sprite):
    images = []
    def __init__(self, ID, name, color, numEyes, numLegs, faveFood):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[ID]
        self.ID = ID
        self.rect = self.image.get_rect(midbottom = (data.width//2 - ID*300, data.height - 100))

        # individual pet characteristics
        self.name = name
        self.color = color
        self.numEyes = numEyes
        self.numLegs = numLegs
        self.faveFood = faveFood

    #def update(self):
      #  self.rect.move_ip(25 + self.ID, 25 + self.ID)

# main game function
def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 750))

    # load images
    background = load_image('background.jpg')
    petImages = load_images('cat.jpeg', 'bunny.jpeg')
    Pet.images = petImages

    # display background
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # create clock to keep track of time
    clock = pygame.time.Clock()

    # initialize sprites
    allsprites = pygame.sprite.OrderedUpdates(())
    Pet.containers = allsprites
    Title.containers = allsprites

    # create score
    if pygame.font:
        allsprites.add(Title())

    pet1 = Pet(0, "Herbert", "grey", 3, 4, "kimchi")
    pet2 = Pet(1, "Jimothy", "pink", 2, 3, "ice cream")
    allsprites.add(pet1)
    allsprites.add(pet2)


    # game loop
    going = True
    while going:

        clock.tick(60)

        # event queue
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False

        # update all sprites
        allsprites.update()

        # draw all sprites
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()