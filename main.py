# import everything
import os, pygame, random, time, sys
from pygame.locals import *

main_dir = os.path.split(os.path.abspath(__file__))[0]

import createPet
import cakegame

# set up screen and data
class Data(object):
    def __init__(self):
        self.screenRect = Rect(0, 0, 1000, 700)
        self.screenSurf = pygame.display.set_mode((1000, 700))
        self.width = self.screenRect[2]
        self.height = self.screenRect[3]
        self.margin = [25, 25]

        # pre-defined coordinates
        self.centerX = self.width//2
        self.leftX = self.margin[0]
        self.rightX = self.width - self.margin[1]
        self.upperY = self.margin[1]
        self.lowerY = self.height - self.height//3
        self.centerY = self.height//2

        # 0: choosePet, 1: createPet, 2: showPet, 3: map, 4: cakegame,
        # 5: flappygame, 6: feed
        self.mode = 0
        self.screen = pygame.display.set_mode((1000, 750))

        # title and button info
        self.titles = {"choose pet" : "Which pet will you choose?", \
                       "create pet" : "Create a pet!", \
                       "show pet" : "Here's your pet!", \
                       "map" : "Map"}
        self.buttons = {"create pet" : "Or, create a new one!", \
                        "get pet" : "Get pet!", "go to map": "To the map!", \
                        "map" : ["Cake Game", "Flappy Game", "Feed Pet"],
                        "back" : "Back"}

        self.categories = ["strawberry", "angora", "axolotl", "seaCucumber", "gown", \
              "persianCat", "hoopskirt", "acorn", "siameseCat", "bathTowel",\
              "dough", "coffeepot"]
        self.attributeSliders = ["How much does your pet like fruit?", \
                                 "How soft and fluffy is your pet?", \
                                 "How quirky is your pet?", \
                                 "How wet and slippery is your pet?", \
                                 "How fancy and pretty is your pet?", \
                                 "How floofy is your pet?", \
                                 "How old-fashioned is your pet?", \
                                 "How much does your pet like the forest?", \
                                 "How expensive and exotic is your pet?", \
                                 "How clean is your pet?", \
                                 "How chunky and round is your pet?", \
                                 "How much does your pet like coffee?"]
        self.petImages = {0 : 'img0.jpeg', 1 : 'img1.jpeg', 2 : 'img2.jpeg', 3: 'img3.jpeg', \
                          4 : 'img4.jpeg', 5 : 'img5.jpeg', 6 : 'img6.jpeg', 7 : 'img7.jpeg', \
                          8 : 'img8.jpeg', 9 : 'img9.jpeg', 10 : 'img10.jpeg'}

        # keep track of pets
        self.pets = set()
        self.currentPet = None

        # colors
        self.transparent = (0, 64, 64, 64)
        self.trans = (1, 1, 1)
        self.blue = (120, 169, 255)
        self.pink = (255, 129, 231)
        self.yellow = (255, 244, 81)
        self.orange = (255, 180, 81)
        self.black = (0, 0, 0)
        self.grey = (176, 169, 178)
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

# button class
class Button(object):
    def __init__(self, msg, location, orientation, mode):
        self.color = data.white
        self.bg, self.fg = data.white, data.black
        self.mode = mode
        self.font = pygame.font.Font(None, 36)
        self.msg = msg

        self.size = self.font.size(self.msg)
        self.msgSurf = self.font.render(self.msg, 1, self.fg)
        self.msgRect = self.msgSurf.get_rect(center = [s//2 for s in self.size])

        self.surface = pygame.surface.Surface(self.size)
        if orientation == "midtop":
            self.rect = self.surface.get_rect(midtop = location)
        elif orientation == "topleft":
            self.rect = self.surface.get_rect(topleft = location)
        elif orientation == "center":
            self.rect = self.surface.get_rect(center = location)

    def draw(self):
        self.mouseover()
        self.surface.fill(self.bg)
        self.surface.blit(self.msgSurf, self.msgRect)
        data.screenSurf.blit(self.surface, self.rect)

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

        self.margin = (12, 14)
        self.width, self.height = 300, self.size[1] + 2*self.margin[1]
        self.x = pos
        self.y = data.height//7 + (self.ID - 1)*(self.height + self.margin[0])
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.buttR = 10
        self.length = 200

        self.mode = mode
        self.surf = pygame.surface.Surface((self.width, self.height))
        self.hit = False

        self.msgSurf = self.font.render(name, 1, data.black)
        self.msgRect = self.msgSurf.get_rect(midleft = (self.margin[0], self.height//2 - self.margin[1]//2))
        self.sPos = (self.margin[0], self.height//2 + self.margin[1]//2)

        # static graphics: slider bg
        self.surf.fill((data.white))
        pygame.draw.rect(self.surf, data.grey, [self.sPos[0], self.sPos[1], self.length, 4], 0)
        self.surf.blit(self.msgSurf, self.msgRect)

        # dynamic graphics: slider button
        self.buttonSurf = pygame.surface.Surface((self.buttR*2, self.buttR*2))
        self.buttonSurf.fill(data.trans)
        self.buttonSurf.set_colorkey(data.trans)
        pygame.draw.circle(self.buttonSurf, data.grey, (self.buttR, self.buttR), self.buttR, 0)
        pygame.draw.circle(self.buttonSurf, data.pink, (self.buttR, self.buttR), self.buttR - 2, 0)

    def draw(self):
        surf = self.surf.copy()
        pos = (0 + int((self.val-self.min)/(self.max-self.min)*self.length), self.sPos[1] + 2)
        self.buttonRect = self.buttonSurf.get_rect(center=pos)
        surf.blit(self.buttonSurf, self.buttonRect)
        self.buttonRect.move_ip(self.x, self.y)

        data.screenSurf.blit(surf, (self.x, self.y))

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
    def __init__(self, name, strawberry, angora, axolotl, seaCucumber, gown, \
                 persianCat, hoopskirt, acorn, siameseCat, bathTowel, dough, \
                 coffeepot):

        # individual pet characteristics
        self.name = name
        self.traits = {0 : strawberry, 1 : angora, 2 : axolotl, \
                       3 : seaCucumber, 4 : gown, 5 : persianCat, 6: hoopskirt, \
                       7 : acorn, 8 : siameseCat, 9 : bathTowel, 10 : dough, \
                       11 : coffeepot}

        self.strongest = 0.0
        for trait in self.traits:
            if self.traits[trait] > self.strongest:
                self.strongest = trait
        self.desc = "%s is a pet whose strongest trait is %s" % (self.name, data.categories[self.strongest])

        # get image based on those traits
        self.imageID = int(createPet.featureDistance(self.traits))
        self.image = self.images[self.imageID]
        self.ID = len(data.pets) + 1

        # initial position and rect
        self.pos = (data.margin[0] + self.ID*200, data.height//2 - data.margin[1])
        self.rect = self.image.get_rect(midbottom = self.pos)
        #self.namePos = (self.pos[0] + self.rect.width//2, self.pos[1] + self.rect.height + 10)
        #self.descPos = (self.pos[0] + self.rect.width//2, self.pos[1] + self.rect.height + 10)

        self.fontSize = 36
        self.font = pygame.font.Font(None, self.fontSize)

    def draw(self):
        # update pos and rect based on mode, display whatever is necessary
        if data.mode == 0:
            self.pos = (data.margin[0] + self.ID*200, data.height//3 + data.margin[1])
        elif data.mode == 1:
            self.pos = (data.width//3 + self.ID*200, data.height//3)
        elif data.mode == 2:
            self.pos = (data.width//2 - self.rect.width, data.height//2 - self.rect.height)
            self.fontSize = 44
            # desc is only shown in mode 2
            self.descPos = (self.pos[0] + self.rect.width//2, self.pos[1] - 20)
            self.descSurf = self.font.render(self.desc, 1, data.black)
            self.descRect = self.descSurf.get_rect(midtop = self.descPos)
            data.screenSurf.blit(self.descSurf, self.descRect)
        elif data.mode == 3:
            self.pos == (data.margin[0], data.height - data.margin[1])

        self.rect = self.image.get_rect(midbottom = self.pos)
        data.screenSurf.blit(self.image, self.pos)
        # display name or not, based on mode
        if data.mode < 3:
            self.namePos = (self.pos[0] + self.rect.width//2, self.pos[1] + self.rect.height + 10)
            self.nameSurf = self.font.render(self.name, 1, data.black)
            self.nameRect = self.nameSurf.get_rect(midtop = self.namePos)
            data.screenSurf.blit(self.nameSurf, self.nameRect)

    def mouseClick(self):
        mousePos = pygame.mouse.get_pos()
        petPos = self.rect
        if (petPos.left < mousePos[0] < petPos.right) and \
            (petPos.top < mousePos[1] < petPos.bottom):
                return True
        else:
            return False

# main game function
def main():
    pygame.init()

    # load images
    background = load_image('background.jpg')
    Pet.images = load_images('img0.jpeg', 'img1.jpeg', 'img2.jpeg', \
                            'img3.jpeg', 'img4.jpeg', 'img5.jpeg', \
                            'img6.jpeg', 'img7.jpeg', 'img8.jpeg', \
                            'img9.jpeg', 'img10.jpeg')

    # display background
    data.screenSurf.blit(background, (0, 0))
    pygame.display.flip()

    # create clock to keep track of time
    clock = pygame.time.Clock()

    # initialize sprites
    titles, buttons, sliders, pets = [], [], [], []

    # initialize titles, buttons, sliders
    if pygame.font:
        # mode 0: choose pet
        choosePetTitle = Button(data.titles["choose pet"], (data.centerX, data.upperY), "midtop", 0)
        createPetButton = Button(data.buttons["create pet"], (data.centerX, data.lowerY), "center", 0)

        # mode 1: create pet
        createPetTitle = Button(data.titles["create pet"], (data.centerX, data.upperY), "midtop", 1)
        backButton1 = Button(data.buttons["back"], (data.leftX, data.upperY), "topleft", 1)
        getPetButton = Button(data.buttons["get pet"], (data.centerX, data.lowerY), "center", 1)
        strawberry = Slider(1, data.attributeSliders[0], 50, 100, 0, data.margin[0], 1)
        angora = Slider(2, data.attributeSliders[1], 50, 100, 0, data.margin[0], 1)
        axolotl = Slider(3, data.attributeSliders[2], 50, 100, 0, data.margin[0], 1)
        seaCucumber = Slider(4, data.attributeSliders[3], 50, 100, 0, data.margin[0], 1)
        gown = Slider(5, data.attributeSliders[4], 50, 100, 0, data.margin[0], 1)
        persianCat = Slider(6, data.attributeSliders[5], 50, 100, 0, data.margin[0], 1)
        hoopskirt = Slider(7, data.attributeSliders[6], 50, 100, 0, data.margin[0], 1)
        acorn = Slider(8, data.attributeSliders[7], 50, 100, 0, data.margin[0], 1)
        siameseCat = Slider(9, data.attributeSliders[8], 50, 100, 0, data.margin[0], 1)
        bathTowel = Slider(10, data.attributeSliders[9], 50, 100, 0, data.margin[0], 1)
        dough = Slider(11, data.attributeSliders[10], 50, 100, 0, data.margin[0], 1)
        coffeepot = Slider(12, data.attributeSliders[11], 50, 100, 0, data.margin[0], 1)

        # mode 2: show pet
        showPetTitle = Button(data.titles["show pet"], (data.centerX, data.upperY), "midtop", 2)
        backButton2 = Button(data.buttons["back"], (data.leftX, data.upperY), "topleft", 2)
        goToMapButton = Button(data.buttons["go to map"], (data.centerX, data.lowerY), "center", 2)

        # mode 3: map
        mapTitle = Button(data.titles["map"], (data.centerX, data.upperY), "midtop", 3)
        backButton3 = Button(data.buttons["back"], (data.leftX, data.upperY), "topleft", 3)
        cakeGameButton = Button(data.buttons["map"][0], (data.centerX, data.lowerY), "center", 3)
        flappyGameButton = Button(data.buttons["map"][1], (data.centerX + 200, data.lowerY + 200), "center", 3)
        feedPetButton = Button(data.buttons["map"][2], (data.centerX + 400, data.lowerY + 400), "center", 3)

        titles += [choosePetTitle, createPetTitle, showPetTitle, mapTitle]
        buttons += [createPetButton, getPetButton, cakeGameButton, \
                    flappyGameButton, feedPetButton, backButton1, backButton2, \
                    backButton3, goToMapButton]
        sliders += [strawberry, angora, axolotl, seaCucumber, gown, persianCat, \
                    hoopskirt, acorn, siameseCat, bathTowel, dough, coffeepot]
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
                    # user wants to create a new pet
                    if createPetButton.mouseClick():
                        data.mode = 1
                    # user selects an existing pet
                    for pet in pets:
                        if pet.mouseClick():
                            data.currentPet = pet
                            data.mode = 2
                            print("current pet", data.currentPet, data.currentPet.name)

            # CREATE PET SCREEN
            elif data.mode == 1:
                if event.type == MOUSEBUTTONDOWN:
                    # back button
                    if backButton1.mouseClick():
                        data.mode = 0
                    # get pet button
                    if getPetButton.mouseClick():
                        print("adding pet")
                        traits = []
                        for slider in sliders:
                            traits += [slider.getDecimal()]
                        print("traits", traits)
                        pet = Pet("Boompus", traits[0], traits[1], traits[2], \
                                  traits[3], traits[4], traits[5], traits[6], \
                                  traits[7], traits[8], traits[9], traits[10], \
                                  traits[11])
                        pets += [pet]
                        data.pets.add(pet)
                        data.currentPet = pet
                        data.mode = 2
                    # sliders
                    pos = pygame.mouse.get_pos()
                    for slider in sliders:
                        if slider.buttonRect.collidepoint(pos):
                            slider.hit = True
                elif event.type == MOUSEBUTTONUP:
                    for slider in sliders:
                        slider.hit = False

            # SHOW PET SCREEN
            elif data.mode == 2:
                if event.type == MOUSEBUTTONDOWN:
                    # back button
                    if backButton2.mouseClick():
                        data.mode = 0
                    # go to map button
                    if goToMapButton.mouseClick():
                        data.mode = 3

            # MAP SCREEN
            elif data.mode == 3:
                if event.type == MOUSEBUTTONDOWN:
                    # back button
                    if backButton3.mouseClick():
                        data.mode = 0
                    # cake game button
                    elif cakeGameButton.mouseClick:
                        data.mode = 4
                        cakegame.main(data.petImages[data.currentPet.imageID])

        # update sliders
        for slider in sliders:
            if slider.hit:
                slider.move()

        # draw all sprites
        data.screenSurf.blit(background, (0, 0))
        for pet in pets:
            if (data.mode >= 2) or (pet == data.currentPet):
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

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()