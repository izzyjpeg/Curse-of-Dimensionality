### Please see the bottom Bibliography section for code and image citations!

# import everything
import os, pygame, random, time, sys
from pygame.locals import *

main_dir = os.path.split(os.path.abspath(__file__))[0]

import createPet
import cakegame

# helper functions to read and write files
def readFile(path):
    with open(path, "rt") as f:
        return f.read()
def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

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
        self.lowerY = self.height - self.margin[1]
        self.centerY = self.height//2

        # 0: choosePet, 1: createPet, 2: showPet, 3: map, 4: cakegame,
        # 5: feed
        self.mode = 0

        # title and button info
        self.titles = {"choose pet" : "Which pet will you choose?", \
                       "create pet" : "Create a pet!", \
                       "show pet" : "Here's your pet!", \
                       "map" : "Map"}
        self.buttons = {"create pet" : "Create a new pet!", \
                        "get pet" : "See your new pet!", "go to map": "To the map!", \
                        "map" : ["Cake Game", "Feed Pet"],
                        "back" : "Back", "no pets yet" : "No pets yet :(", \
                        "food" : ["You have", 0, "cakes, and", 0, "bobas."]}
        self.textboxes = {"name" : "Click and type to name pet!"}

        self.categories = ["strawberry", "angora", "axolotl", "seaCucumber", "gown", \
              "persianCat", "hoopskirt", "acorn", "siameseCat", "bathTowel",\
              "dough", "coffeepot", "screen"]
        self.attributeSliders = {0 : "How much does your pet like fruit?", \
                                 1 : "How soft and fluffy is your pet?", \
                                 2 : "How quirky is your pet?", \
                                 3 : "How wet and slippery is your pet?", \
                                 4 : "How fancy and pretty is your pet?", \
                                 5 : "How floofy is your pet?", \
                                 6 : "How old-fashioned is your pet?", \
                                 7 : "How much does your pet like the forest?", \
                                 8 : "How expensive and exotic is your pet?", \
                                 9 : "How clean is your pet?", \
                                 10 : "How chunky and round is your pet?", \
                                 11 : "How much does your pet like coffee?", \
                                 12 : "How digitally literate is your pet?"}

        self.petImages = {0 : 'img0.jpeg', 1 : 'img1.jpeg', 2 : 'img2.jpeg', 3: 'img3.jpeg', \
                          4 : 'img4.jpeg', 5 : 'img5.jpeg', 6 : 'img6.jpeg', 7 : 'img7.jpeg', \
                          8 : 'img8.jpeg', 9 : 'img9.jpeg', 10 : 'img10.jpeg', \
                          11 : 'img11.jpeg', 12 : 'img12.jpeg', 13 : 'img13.jpeg', \
                          14 : 'img14.jpeg', 15 : 'img15.jpeg', 16 : 'img16.jpeg', \
                          17 : 'img17.jpeg', 18 : 'img18.jpeg', 19 : 'img19.jpeg', \
                          20 : 'img20.jpeg', 21 : 'img21.jpeg', 22 : 'img22.jpeg'
                          }
        self.petImages = {}
        for i in range(52):
            self.petImages[i] = 'img' + str(i) + '.jpeg'

        self.iconImages = {"Cake Game" : 'cakegameicon.png', \
                           "Feed Pet" : 'feedpeticon.png'}

        # foods
        self.cakes = 0
        self.bobas = 0

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

### UI ELEMENTS ###

# message class: derived from button class, see 'code cited' section
class Message(object):
    def __init__(self, msg, location, orientation, mode, alwaysShown=True):
        self.color = data.white
        self.bg, self.fg = data.white, data.black
        self.mode = mode
        self.font = pygame.font.Font(None, 36)
        self.msg = msg

        self.alwaysShown = alwaysShown

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
        self.surface.fill(self.bg)
        self.surface.blit(self.msgSurf, self.msgRect)
        data.screenSurf.blit(self.surface, self.rect)

# button class,  see 'code cited' section
class Button(Message):
    def __init__(self, msg, location, orientation, mode):
        super().__init__(msg, location, orientation, mode)
    def draw(self):
        self.mouseover()
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

# icon class : like a button but with an image
class Icon(Button):
    def __init__(self, msg, location, orientation, mode):
        super().__init__(msg, location, orientation, mode)
        self.image = load_image(data.iconImages[self.msg])
        self.image = pygame.transform.scale(self.image, (200, 200))

    def draw(self):
        super().draw()
        self.imagePos = self.rect.midtop
        self.imageRect = (self.image.get_rect(midbottom = self.imagePos))
        data.screenSurf.blit(self.image, (self.imageRect.x, self.imageRect.y))

# text box class: updates based on user or game state. see 'code cited' section
class TextBox(Button):
    def __init__(self, msg, location, orientation, mode):
        super().__init__(msg, location, orientation, mode)
        self.text = ""
        self.active = False
        self.textSurf = self.font.render(self.text, 1, data.black)
        self.desc = "Click the box and type to name your pet!"
        self.descFont = pygame.font.Font(None, 20)
        self.descSurf = self.descFont.render(self.desc, 1, data.black)

    def update(self):
        self.width = max(self.descSurf.get_width() + 10, self.textSurf.get_width() + 10)
        self.height = self.textSurf.get_height()
        self.rect.width = self.width

    def draw(self):
        self.surface = pygame.surface.Surface((self.width, self.height))
        self.surface.fill(self.bg)
        self.textSurf = self.font.render(self.text, 1, data.black)
        data.screenSurf.blit(self.surface, self.rect)
        data.screenSurf.blit(self.descSurf, (self.rect.x, self.rect.y - 20))
        data.screenSurf.blit(self.textSurf, (self.rect.x, self.rect.y))
        pygame.draw.rect(data.screenSurf, data.black, self.rect, 2)

# slider class: see 'code cited' section
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
        self.x = data.leftX + (self.width * (self.ID // 10)) + (self.margin[0] * (self.ID // 10))
        self.y = (data.upperY + 90) + (self.ID % 10) * (self.height + self.margin[1])
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.buttR = int(self.height / 4)
        self.length = self.width - (2 * self.margin[0])

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

### PETS ###

# pet class
class Pet(object):
    def __init__(self, name, ID, traits):
        self.images = data.petImages
        # individual pet characteristics
        self.name = name
        self.traits = traits
        self.strongest = 0.0
        for trait in self.traits:
            if self.traits[trait] > self.strongest:
                self.strongest = trait
        self.desc = "%s 's strongest trait is %s." \
                     % (self.name, data.categories[self.strongest])

        # get image based on those traits
        self.speciesID = int(createPet.featureDistance(self.traits))
        self.image = load_image(self.images[self.speciesID])
        self.image = pygame.transform.smoothscale(self.image, (300, 300))
        self.medImage = pygame.transform.smoothscale(self.image, (200, 200))
        self.smImage = pygame.transform.smoothscale(self.image, (150, 150))
        self.ID = ID

        # initial position and rect
        self.x = data.centerX
        self.y = data.centerY
        self.pos = (self.x, self.y)
        self.margin = [25, 25]

        self.rect = self.image.get_rect(center = self.pos)
        self.smRect = self.smImage.get_rect(center = self.pos)
        self.medRect = self.medImage.get_rect(center = self.pos)

        self.width, self.height = self.rect.width, self.rect.height
        self.smWidth, self.smHeight = self.smRect.width, self.smRect.height
        self.medWidth, self.medHeight = self.medRect.width, self.medRect.height

    def __repr__(self):
        traitlist = []
        for trait in self.traits:
            value = self.traits[trait]
            traitlist += [str(trait) + ":" + str(value)]
        traits = "__trait__".join(traitlist)
        return "__name__" + str(self.name)+ "__ID__" + str(self.ID) + "__traits__" + traits

    def __hash__(self):
        return hash(self.ID)

    def __eq__(self, other):
        return isinstance(other, Pet) and (self.ID == other.ID)

    def draw(self):
        self.nameSize, self.descSize = 36, 18
        self.nameFont = pygame.font.Font(None, self.nameSize)
        self.descFont = pygame.font.Font(None, self.descSize)

        # update pos, text, image based on mode. pet not shown when mode == 1
        if data.mode == 0:
            xOffset = int((self.smWidth * 2) + (self.margin[0] * 1.5))
            yOffset = int((self.smHeight * 2) + (self.margin[1] * 0.5))

            self.x = (data.width//2 - xOffset + (self.smWidth * (self.ID % 4))
                        + (self.margin[0] * (self.ID % 4)))
            self.y = (data.height//2 - yOffset + self.margin[1]
                        + (self.ID // 4) * (self.medHeight))

            self.pos = (self.x, self.y)
            self.rect = self.smImage.get_rect(center = self.pos)
            data.screenSurf.blit(self.smImage, self.pos)

        elif data.mode == 2:
            self.pos = (data.width//2 - self.width//2, data.height//2 - self.height//2)
            self.rect = self.image.get_rect(center = self.pos)
            data.screenSurf.blit(self.image, self.pos)

        elif data.mode == 3:
            self.pos = (data.leftX, data.lowerY)
            self.rect = self.smImage.get_rect(bottomleft = self.pos)
            data.screenSurf.blit(self.smImage, self.pos)

        # display name or not, based on mode
        if data.mode <= 3:
            if (data.mode == 0) or (data.mode == 2):
                self.nameX = self.pos[0] + self.rect.width//2
                self.nameY = self.pos[1] + self.rect.height + self.margin[1]//4

                self.namePos = (self.nameX, self.nameY)
                self.nameSurf = self.nameFont.render(self.name, 1, data.black)
                self.nameRect = self.nameSurf.get_rect(midtop = self.namePos)
                data.screenSurf.blit(self.nameSurf, self.nameRect)

            elif data.mode == 3:
                self.nameX = self.pos[0] + self.rect.width + self.margin[0]
                self.nameY = self.pos[1]

                self.namePos = (self.nameX, self.nameY)
                self.nameSurf = self.nameFont.render(self.name, 1, data.black)
                self.nameRect = self.nameSurf.get_rect(topleft = self.namePos)
                data.screenSurf.blit(self.nameSurf, self.nameRect)

        # display desc or not, based on mode
        if (data.mode == 2) or (data.mode == 3):
            self.nameSize, self.descSize = 44, 30
            if data.mode == 2:
                self.descX = self.nameX
                self.descY = self.nameY + self.margin[1]

                self.descPos = (self.descX, self.descY)
                self.descSurf = self.descFont.render(self.desc, 1, data.black)
                self.descRect = self.descSurf.get_rect(midtop = self.descPos)
                data.screenSurf.blit(self.descSurf, self.descRect)

            else:
                self.descX = self.nameX
                self.descY = self.nameY + self.margin[1]

                self.descPos = (self.descX, self.descY)
                self.descSurf = self.descFont.render(self.desc, 1, data.black)
                self.descRect = self.descSurf.get_rect(topleft = self.descPos)
                data.screenSurf.blit(self.descSurf, self.descRect)

    def mouseClick(self):

        self.clickRect= self.smImage.get_rect(topleft = self.pos)

        mousePos = pygame.mouse.get_pos()
        petRect = self.clickRect
        if (petRect.left < mousePos[0] < petRect.right) and \
            (petRect.top < mousePos[1] < petRect.bottom):
                return True
        else:
            return False

# helper function to read pets.txt
def getPets(file):
    contents = readFile(file)
    if len(contents) == 0:
        return set()
    pets = set()

    for pet in contents.split("__pet__")[1:]:
        name = pet[pet.index("__name__")+8:pet.index("__ID__")]
        ID = int(pet[pet.index("__ID__")+6:pet.index("__traits__")])
        traitlist = pet[pet.index("__traits__")+10:]
        traits = {}
        for trait in traitlist.split("__trait__"):
            i = trait.index(":")
            key, value = int(trait[:i]), float(trait[i + 1:])
            traits[key] = value
        pets.add(Pet(name, ID, traits))
    return pets

# and to write it
def addPet(file, pet):
    contents = readFile(file)
    petInfo = repr(pet)
    newContents = contents + "__pet__" + petInfo
    writeFile(file, newContents)

# keep track of pets
class AllPets(object):
    def __init__(self):
        self.petlist = getPets("pets.txt")
        self.currentPet = None
        self.petname = ""
allPets = AllPets()

# main game function
def main():
    pygame.init()

    # load images
    defaultBG = pygame.transform.scale(load_image('background.jpg'), (1000, 700))
    mapBG = pygame.transform.scale(load_image('mapbackground.jpg'), (1000, 700))

    # display background
    #data.screenSurf.blit(background, (0, 0))
    pygame.display.flip()

    # create clock to keep track of time
    clock = pygame.time.Clock()

    # initialize sprites
    messages, buttons, backButtons, icons, sliders = [], [], [], [], []

    # initialize titles, buttons, sliders
    if pygame.font:

        # all back buttons
        for i in range(1, 6):
            backButton = Button(data.buttons["back"], (data.leftX, data.upperY), "topleft", i)
            buttons += [backButton]
            backButtons += [backButton]

        # mode 0: choose pet
        choosePetTitle = Message(data.titles["choose pet"], (data.centerX, data.upperY), "midtop", 0)
        noPetsYet = Message(data.buttons["no pets yet"], (data.centerX, data.upperY + 100), "center", 0, False)
        createPetButton = Button(data.buttons["create pet"], (data.centerX, data.lowerY), "center", 0)

        # mode 1: create pet
        createPetTitle = Message(data.titles["create pet"], (data.centerX, data.upperY), "midtop", 1)
        nameTextBox = TextBox(data.textboxes["name"], (data.leftX, data.upperY + 50), "topleft", 1)
        getPetButton = Button(data.buttons["get pet"], (data.centerX, data.lowerY), "center", 1)
        for i in range(len(data.categories)):
            slider = Slider(i, data.attributeSliders[i], 50, 100, 0, data.leftX, 1)
            sliders += [slider]

        # mode 2: show pet
        showPetTitle = Message(data.titles["show pet"], (data.centerX, data.upperY), "midtop", 2)
        goToMapButton = Button(data.buttons["go to map"], (data.centerX, data.lowerY), "center", 2)

        # mode 3: map
        mapTitle = Message(data.titles["map"], (data.centerX, data.upperY), "midtop", 3)
        cakeGameIcon = Icon(data.buttons["map"][0], (data.centerX + 250, data.lowerY - 400), "center", 3)
        feedPetIcon = Icon(data.buttons["map"][1], (data.centerX, data.lowerY - 100), "center", 3)
        #foodMessage = Message(data.buttons["food"], (data.leftX, data.centerY), "topleft", 3)

        messages += [choosePetTitle, createPetTitle, showPetTitle, mapTitle, \
                     noPetsYet]
        buttons += [createPetButton, getPetButton, goToMapButton, nameTextBox]
        icons += [cakeGameIcon, feedPetIcon]
        for slider in sliders:
            slider.draw()

### Game Loop ###

    going = True
    while going:

        #clock.tick_busy_loop()

        # event queue
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False

            # ALL BACK BUTTONS
            for backButton in backButtons:
                if event.type == MOUSEBUTTONDOWN and backButton.mouseClick():
                    if data.mode <= 2:
                        data.mode = 0
                    else:
                        data.mode = 2

            # CHOOSE PET SCREEN
            if data.mode == 0:
                if event.type == MOUSEBUTTONDOWN:
                    # user wants to create a new pet
                    if createPetButton.mouseClick():
                        data.mode = 1
                    # user selects an existing pet
                    else:
                        for pet in allPets.petlist:
                            if pet.mouseClick():
                                allPets.currentPet = pet
                                data.mode = 2

            # CREATE PET SCREEN
            elif data.mode == 1:
                if event.type == MOUSEBUTTONDOWN:
                    # get pet button
                    if getPetButton.mouseClick():
                        traits = {}
                        for slider in sliders:
                            traits[slider.ID] = slider.getDecimal()

                        # add pet (they are stored in a file)
                        ID = len(allPets.petlist)
                        if len(allPets.petname) == 0:
                            name = "no name"
                        else:
                            name = allPets.petname
                        pet = Pet(name, ID, traits)
                        addPet('pets.txt', pet)
                        allPets.petlist = getPets('pets.txt')
                        allPets.currentPet = pet

                        data.mode = 2

                    # activate name textbox
                    elif nameTextBox.mouseClick():
                        nameTextBox.active = not nameTextBox.active

                    # activate sliders
                    pos = pygame.mouse.get_pos()
                    for slider in sliders:
                        if slider.buttonRect.collidepoint(pos):
                            slider.hit = True

                elif event.type == KEYDOWN:
                    # fill name textbox
                    if event.key == K_BACKSPACE:
                        if len(nameTextBox.msg) > 0:
                            nameTextBox.text = nameTextBox.text[:-1]
                    else:
                        nameTextBox.text += event.unicode
                        allPets.petname = nameTextBox.text

                # deactivate sliders
                elif event.type == MOUSEBUTTONUP:
                    for slider in sliders:
                        slider.hit = False

            # SHOW PET SCREEN
            elif data.mode == 2:
                if event.type == MOUSEBUTTONDOWN:
                    # go to map button
                    if goToMapButton.mouseClick():
                        data.mode = 3

            # MAP SCREEN
            elif data.mode == 3:
                if event.type == MOUSEBUTTONDOWN:
                    # cake game button
                    if cakeGameIcon.mouseClick:
                        data.mode = 4
                        prizes = cakegame.main(data.petImages[allPets.currentPet.speciesID])
                        data.cakes += prizes[0]
                        data.bobas += prizes[1]
                        data.mode = 3

        # update sliders
        for slider in sliders:
            if slider.hit:
                slider.move()
        for button in buttons:
            if isinstance(button, TextBox):
                button.update()

        # draw all sprites
        if data.mode == 3:
            data.screenSurf.blit(mapBG, (0,0))
        else:
            data.screenSurf.blit(defaultBG, (0, 0))

        for button in buttons:
            if button.mode == data.mode:
                button.draw()
        for message in messages:
            if message.mode == data.mode:
                if message.alwaysShown:
                    message.draw()
                elif len(allPets.petlist) == 0:
                    message.draw()
        for slider in sliders:
            if slider.mode == data.mode:
                slider.draw()
        for icon in icons:
            if data.mode == 3:
                icon.draw()
        for pet in allPets.petlist:
            if data.mode == 0:
                pet.draw()
            elif (pet == allPets.currentPet) and (data.mode != 1):
                pet.draw()

        pygame.display.flip()

    pygame.quit()
    # TEMPORARY clear pet list upon closing pygame window
    writeFile("pets.txt", "")
    sys.exit()

if __name__ == '__main__':
    main()

### Bibliography ###
# Code cited/taken from other sources:
# Textboxes: https://stackoverflow.com/questions/46390231/how-to-create-a-text-input-box-with-pygame
# Buttons and sliders: https://www.dreamincode.net/forums/topic/401541-buttons-and-sliders-in-pygame
# General Pygame: https://www.pygame.org/docs/

# Images:
# Backgrounds processed with DeepDreamGenerator: deepdreamgenerator.com
# Pet images collected from GANbreeder: ganbreeder.app