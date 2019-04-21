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

        # 0: choosePet, 1: createPet, 2: showPet, 3: map, 4: cakegame,
        # 5: flappygame, 6: feed
        self.mode = 0
        self.screen = pygame.display.set_mode((1000, 750))

        # title and button info
        self.titles = ["0 Which pet will you choose?", "1 Create a pet!", \
                        "2 Map", "Cake Game", "Flappy Game", "Feed", "Clothe"]
        self.titleX = self.width//2
        self.titleY = self.height//12
        self.buttons = ["Or, create a new one!", "Get pet!", "To the map!", \
                        ["Cake Game", "Flappy Game", "Feed Pet"]]
        self.lowerButtonX = self.width//2
        self.lowerButtonY = self.height - self.height//3
        self.attributeSliders = ["How much does your pet like fruit?", \
                                 "How soft and fluffy is your pet?", \
                                 "How quirky is your pet?", \
                                 "How wet and slippery is your pet?", \
                                 "How fancy and pretty is your pet?"]
        # keep track of pets
        self.pets = set()
        self.currentPet = None

        # colors
        self.transparent = (0, 64, 64, 64)
        self.trans = (1, 1, 1)
        self.blue = (50, 30, 250)
        self.pink = (170, 0, 20)
        self.yellow = (100, 100, 0)
        self.orange = (200, 100, 0)
        self.black = (0, 0, 0)
        self.white = (250, 250, 250)

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

# button class
class Button(object):
    def __init__(self, msg, location, mode, bg=Color("White"), fg=Color("Black")):
        self.color = bg
        self.bg = bg
        self.fg = fg
        self.mode = mode
        self.font = pygame.font.Font(None, 36)
        self.msg = msg

        self.size = self.font.size(self.msg)
        self.msgSurf = self.font.render(self.msg, 1, self.fg)
        self.msgRect = self.msgSurf.get_rect(center = [s//2 for s in self.size])

        self.surface = pygame.surface.Surface(self.size)
        self.rect = self.surface.get_rect(center = location)

    def draw(self):
        self.mouseover()
        self.surface.fill(self.bg)
        self.surface.blit(self.msgSurf, self.msgRect)
        data.screen.blit(self.surface, self.rect)

    def mouseover(self):
        self.bg = self.color
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.bg = Color("grey")

    def mouseClick(self):
        mousePos = pygame.mouse.get_pos()
        buttonPos = self.rect
        if (buttonPos.left < mousePos[0] < buttonPos.right) and \
            (buttonPos.top < mousePos[1] < buttonPos.bottom):
                return True
        else:
            return False

# slider class
class Slider(object):
    def __init__(self, ID, name, val, max, min, pos, mode):
        self.val = val
        self.max = max
        self.min = min
        self.ID = ID

        self.font = pygame.font.Font(None, 20)
        self.size = self.font.size(name)

        self.margin = (15, 15)
        self.width, self.height = 300, self.size[1] + 2*self.margin[1]
        self.x = pos
        self.y = data.height//4 + (self.ID - 1)*(self.height + self.margin[0])
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.buttR = 10
        self.length = 200

        self.mode = mode
        self.surf = pygame.surface.Surface((self.width, self.height))
        self.hit = False

        self.msgSurf = self.font.render(name, 1, data.black)
        self.msgRect = self.msgSurf.get_rect(midleft = (self.margin[0], self.height//2 - 10))
        self.sPos = (self.margin[0], self.height//2 + 10)

        print(type(self.val), self.val)

        # static graphics: slider bg
        self.surf.fill((data.white))
        pygame.draw.rect(self.surf, data.yellow, [self.sPos[0], self.sPos[1], self.length, 6], 0)
        self.surf.blit(self.msgSurf, self.msgRect)

        # dynamic graphics: slider button
        self.buttonSurf = pygame.surface.Surface((self.buttR*2, self.buttR*2))
        self.buttonSurf.fill(data.trans)
        self.buttonSurf.set_colorkey(data.trans)
        pygame.draw.circle(self.buttonSurf, data.black, (self.buttR, self.buttR), self.buttR, 0)
        pygame.draw.circle(self.buttonSurf, data.orange, (self.buttR, self.buttR), self.buttR - 2, 0)

    def draw(self):
        surf = self.surf.copy()
        pos = (0 + int((self.val-self.min)/(self.max-self.min)*self.length), self.sPos[1] + 3)
        self.buttonRect = self.buttonSurf.get_rect(center=pos)
        surf.blit(self.buttonSurf, self.buttonRect)
        self.buttonRect.move_ip(self.x, self.y)

        data.screen.blit(surf, (self.x, self.y))

    # move the slider button using the mouse
    def move(self):
        self.val = (pygame.mouse.get_pos()[0] - self.x) / self.length * (self.max - self.min) + self.min
        if self.val < self.min:
            self.val = self.min
        if self.val > self.max:
            self.val = self.max

    # return the chosen value
    def getDecimal(self):
        return self.val/100

# pet class
class Pet(object):
    images = []
    def __init__(self, name, strawberry, angora, axolotl, seaCucumber, gown):

        # individual pet characteristics
        self.name = name
        self.traits = {"strawberry" : strawberry, "angora" : angora, \
                        "axolotl" : axolotl, "seaCucumber" : seaCucumber, \
                        "gown" : gown}

        # get image based on those traits

        imageID = createPet.featureDistance(self.traits)

        self.image = self.images[int(imageID)]
        self.ID = len(data.pets) + 1
        self.pos = (data.margin[0] + self.ID*200, data.height//2 - data.margin[1])
        self.rect = self.image.get_rect(midbottom = self.pos)
        self.msgPos = (self.pos[0] + self.rect.width//2, self.pos[1] + self.rect.height + 10)

        self.font = pygame.font.Font(None, 30)

    def draw(self):
        data.screen.blit(self.image, self.pos)
        if data.mode < 3:
            self.msgSurf = self.font.render(self.name, 1, data.black)
            self.msgRect = self.msgSurf.get_rect(midtop = self.msgPos)
            data.screen.blit(self.msgSurf, self.msgRect)


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
    titles, buttons, sliders = [], [], []
    pets = []
    Pet.containers = pets

    # initialize titles, buttons, sliders
    if pygame.font:
        # mode 0: choose pet
        createPetButton = Button(data.buttons[0], (data.lowerButtonX, data.lowerButtonY), 0)
        choosePetTitle = Button(data.titles[0], (data.titleX, data.titleY), 0)
        # mode 1: create pet
        getPetButton = Button(data.buttons[1], (data.lowerButtonX, data.lowerButtonY), 1)
        slider1 = Slider(1, data.attributeSliders[0], 50, 100, 0, 50, 1)
        slider2 = Slider(2, data.attributeSliders[1], 50, 100, 0, 50, 1)
        slider3 = Slider(3, data.attributeSliders[2], 50, 100, 0, 50, 1)
        slider4 = Slider(4, data.attributeSliders[3], 50, 100, 0, 50, 1)
        slider5 = Slider(5, data.attributeSliders[4], 50, 100, 0, 50, 1)
        # mode 2: show pet
        goToMapButton = Button(data.buttons[2], (data.lowerButtonX, data.lowerButtonY), 2)
        # mode 3: map
        cakeGameButton = Button(data.buttons[3][0], (data.lowerButtonX, data.lowerButtonY), 3)
        flappyGameButton = Button(data.buttons[3][1], (data.lowerButtonX + 200, data.lowerButtonY + 200), 3)
        feedPetButton = Button(data.buttons[3][2], (data.lowerButtonX + 400, data.lowerButtonY + 400), 3)

        titles += [choosePetTitle]
        buttons += [createPetButton, getPetButton, cakeGameButton, flappyGameButton, feedPetButton]
        sliders += [slider1, slider2, slider3, slider4, slider5]
        for slider in sliders:
            slider.draw()

### Game Loop ###

    going = True
    while going:

        clock.tick(60)

        # event queue
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False

            # CHOOSE PET SCREEN
            if data.mode == 0:
                if event.type == MOUSEBUTTONDOWN:
                    if createPetButton.mouseClick():
                        data.mode = 1

            # CREATE PET SCREEN
            if data.mode == 1:
                if event.type == MOUSEBUTTONDOWN:
                    if getPetButton.mouseClick():
                        print("adding pet")
                        traits = []
                        for slider in sliders:
                            traits += [slider.getDecimal()]
                        pet = Pet("Boompus", traits[0], traits[1], traits[2], traits[3], traits[4])
                        pets += [pet]
                        data.pets.add(pet)

                    pos = pygame.mouse.get_pos()
                    for slider in sliders:
                        if slider.buttonRect.collidepoint(pos):
                            slider.hit = True
                elif event.type == MOUSEBUTTONUP:
                    for slider in sliders:
                        slider.hit = False

            # MAP SCREEN
            if data.mode == 3:
                if event.type == MOUSEBUTTONDOWN and cakeGameButton.mouseClick:
                    data.mode = 4
                    cakegame.main()

        # update all sprites
        allsprites.update()
        for slider in sliders:
            if slider.hit:
                slider.move()

        # draw all sprites
        data.screen.blit(background, (0, 0))

        allsprites.draw(data.screen)
        for pet in pets:
            pet.draw()
        for button in buttons:
            if button.mode == data.mode:
                button.draw()
        for title in titles:
            if title.mode == data.mode:
                title.draw()
        for slider in sliders:
            if slider.mode == data.mode:
                slider.draw()

        #pets.draw(data.screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()