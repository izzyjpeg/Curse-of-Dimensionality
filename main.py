# import everything
import os, pygame, random, time
from pygame.locals import *

main_dir = os.path.split(os.path.abspath(__file__))[0]

import createPet
import cakegame

# set up screen and data
class Data(object):
    def __init__(self):
        self.screenRect = Rect(0, 0, 1000, 750)
        self.width = self.screenRect[2]
        self.height = self.screenRect[3]
        self.margin = [25, 25]

        # 0: choosePet, 1: createPet, 2: map, 3: cakegame, 4: flappygame,
        # 5: feed, 6: clothe
        self.mode = 0
        self.screen = pygame.display.set_mode((1000, 750))

        # title and button info
        self.titles = ["0 Which pet will you choose?", "1 Create a pet!", \
                        "2 Map", "Cake Game", "Flappy Game", "Feed", "Clothe"]
        self.titleX = self.width//2
        self.titleY = self.height//12
        self.buttons = ["Or, create a new one!", "Get pet!"]
        self.lowerButtonX = self.width//2
        self.lowerButtonY = self.height - self.height//3

        # keep track of pets
        self.pets = set()
        self.currentPet = None

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

# determine if a button has been clicked
def mouseClick(button):
    mousePos = pygame.mouse.get_pos()
    buttonPos = button.rect
    if (buttonPos.left < mousePos[0] < buttonPos.right) and \
        (buttonPos.top < mousePos[1] < buttonPos.bottom):
            return True
    else:
        return False

# title class
class Title(pygame.sprite.Sprite):
    def __init__(self, msg, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 40)
        self.color = Color('white')

        self.msg = msg
        self.size = self.font.size(self.msg)
        self.x = x
        self.y = y

        self.update()
        self.rect = self.image.get_rect().move(self.x, self.y)

    def update(self):
        self.msg = data.titles[data.mode]
        self.image = self.font.render(self.msg, 1, self.color)

# button class
class Button(pygame.sprite.Sprite):
    def __init__(self, msg, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 36)
        self.color = Color('white')

        self.msg = msg
        self.size = self.font.size(self.msg)
        self.x = x
        self.y = y

        self.update()
        self.rect = self.image.get_rect().move(self.x, self.y)

    def update(self):
        self.msg = data.buttons[data.mode]
        typeRect = pygame.Rect(self.x, self.y, 100, 100)
        pygame.draw.rect(data.screen, Color('white'), typeRect, 0)
        self.image = self.font.render(self.msg, 1, self.color)


# pet class
class Pet(pygame.sprite.Sprite):
    images = []
    def __init__(self, name, strawberry, angora, axolotl, seaCucumber, gown):
        pygame.sprite.Sprite.__init__(self, self.containers)

        # individual pet characteristics
        self.name = name
        self.traits = {"strawberry" : strawberry, "angora" : angora, \
                        "axolotl" : axolotl, "seaCucumber" : seaCucumber, \
                        "gown" : gown}

        # get image based on those traits

        imageID = createPet.featureDistance(self.traits)

        self.image = self.images[int(imageID)]
        self.ID = len(data.pets) + 1
        self.pos = (data.width//2 - self.ID*300, data.height//2 - data.margin[1])
        self.rect = self.image.get_rect(midbottom = self.pos)


# main game function
def main():
    pygame.init()

    # load images
    background = load_image('background.jpg')
    petImages = load_images('img1.jpeg', 'img2.jpeg', 'img3.jpeg', \
                            'img4.jpeg', 'img5.jpeg', 'img6.jpeg')
    Pet.images = petImages

    # display background
    data.screen.blit(background, (0, 0))
    pygame.display.flip()

    # create clock to keep track of time
    clock = pygame.time.Clock()

    # initialize sprites
    allsprites = pygame.sprite.OrderedUpdates(())
    titles = pygame.sprite.Group()
    buttons = pygame.sprite.Group()
    pets = pygame.sprite.Group()
    Pet.containers = pets
    Title.containers = titles
    Button.containers = buttons

    # initialize title and create pet button
    if pygame.font:
        if data.mode == 0:
            createPetButton = Button(data.buttons[0], data.lowerButtonX, data.lowerButtonY)
            title = Title(data.titles[0], data.titleX, data.titleY)
        titles.add(title)
        buttons.add(createPetButton)

    # game loop
    going = True
    while going:

        clock.tick(60)

        # event queue
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            # while on choose pet screen
            if data.mode == 0:
                if event.type == MOUSEBUTTONDOWN and mouseClick(createPetButton):
                    data.mode = 1
            # while on create pet screen
            if data.mode == 1:
                if event.type == MOUSEBUTTONDOWN and mouseClick(createPetButton):
                    print("adding pet")
                    pets.add(Pet("Bobby", 0.7, 0.3, 0.1, 0.3, 0.4))
                    buttons.remove(createPetButton)
            # while on map screen
            if data.mode == 2:
                if event.type == MOUSEBUTTONDOWN and mouseClick(cakeGameButton):
                    data.mode = 3
                    cakegame.main()

        # update all sprites
        allsprites.update()
        titles.update()
        buttons.update()

        # draw all sprites
        data.screen.blit(background, (0, 0))

        allsprites.draw(data.screen)
        titles.draw(data.screen)
        buttons.draw(data.screen)
        pets.draw(data.screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()