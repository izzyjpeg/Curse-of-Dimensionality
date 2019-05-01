### Please see the bottom Bibliography section for code and image citations!

# import everything
import os, pygame, random, time, sys
from pygame.locals import *
import createPet, cakegame, simulateRarity

main_dir = os.path.split(os.path.abspath(__file__))[0]

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
        self.screenRect = Rect(0, 0, 1000, 750)
        self.screenSurf = pygame.display.set_mode((1000, 750))
        self.width = self.screenRect[2]
        self.height = self.screenRect[3]
        self.margin = [25, 25]

        # pre-defined coordinates
        self.centerX = self.width//2
        self.leftX = self.margin[0]
        self.rightX = self.width - self.margin[1]
        self.upperY = self.margin[1]
        self.midUpperY = self.upperY + self.height//5
        self.lowerY = self.height - self.margin[1]
        self.centerY = self.height//2
        self.foodStartPos = (self.leftX + 50, self.lowerY - 100)

        # 0: choosePet, 1: createPet, 2: showPet, 3: map, 4: cakegame,
        # 5: feed, # 6: edit
        self.mode = 0

        # bg image info
        self.bgWidth = 1074
        self.bgX = (self.bgWidth - self.screenRect.width) * (-1)

        # title and button info
        self.titles = {"choose pet" : "Which pet will you choose?", \
                       "create pet" : "Create a pet!", \
                       "show pet" : "Here's your pet!", \
                       "map" : "Map", "edit pet" : "Edit Pet", \
                       "feed pet" : "Feed your pet to evolve it!", \
                       "not enough foods" : "You don't have any of those!"}
        self.buttons = {"create pet" : "Create a new pet!", \
                        "get pet" : "See your new pet!", "go to map": "To the map!", \
                        "map" : ["Cake Game", "Feed Pet"], \
                        "back" : "Back", "no pets yet" : "No pets yet :(", \
                        "edit pet" : "Edit Pet", "update pet" : "Update Pet", \
                        "feed cake" : "Give pet cake!", "feed boba" : "Give pet boba!", \
                        "feed donut" : "Give pet a donut!"
                        }
        self.textboxes = {"name" : "Click and type to name pet!", \
                          "food" : "Snack Inventory"}
        self.tbDescs = {"Click and type to name pet!" : "Pet Name",
                        "Snack Inventory" : "Snack Inventory"}

        # pet creation info
        self.categories = ["strawberry", "angora", "axolotl", "seaCucumber", "gown", \
              "persianCat", "hoopskirt", "acorn", "siameseCat", "bathTowel",\
              "dough", "coffeepot", "screen"]
        self.attributeSliders = {0 : "How much does your pet like fruit?", \
                                 1 : "How soft and shy is your pet?", \
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
        self.rarities = simulateRarity.petOdds(1000)

        # images
        self.petImages = {}
        for i in range(52):
            self.petImages[i] = 'img' + str(i) + '.jpeg'
        self.iconImages = {"Cake Game" : 'cakegameicon.png', \
                           "Feed Pet" : 'feedpeticon.png'}
        self.petIcon = pygame.transform.scale(load_image(self.petImages[0]), (32, 32))
        self.foodImages = [pygame.transform.smoothscale(load_image('cake.png'), (150, 150)), \
                           pygame.transform.smoothscale(load_image('boba.png'), (77, 160)), \
                           pygame.transform.smoothscale(load_image('donut.png'), (200, 200))]

        # foods
        self.cakes = 1
        self.bobas = 1
        self.donuts = 1
        self.foodMessage = "You don't have any food yet! Play the Cake Game to get some."
        self.notEnoughFoods = False

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

### THIS CODE DRAWS A ROUNDED RECTANGLE AND WAS TAKEN FROM THE FOLLOWING SOURCE:
# code by josmiley on https://www.pygame.org/project-AAfilledRoundedRect-2349-.html
def roundedRect(surface,rect,color,radius=0.4):
    rect         = Rect(rect)
    color        = Color(*color)
    alpha        = color.a
    color.a      = 0
    pos          = rect.topleft
    rect.topleft = 0,0
    rectangle    = pygame.Surface(rect.size,SRCALPHA)

    circle       = pygame.Surface([min(rect.size)*3]*2,SRCALPHA)
    pygame.draw.ellipse(circle,(0,0,0),circle.get_rect(),0)
    circle       = pygame.transform.smoothscale(circle,[int(min(rect.size)*radius)]*2)

    radius              = rectangle.blit(circle,(0,0))
    radius.bottomright  = rect.bottomright
    rectangle.blit(circle,radius)
    radius.topright     = rect.topright
    rectangle.blit(circle,radius)
    radius.bottomleft   = rect.bottomleft
    rectangle.blit(circle,radius)

    rectangle.fill((0,0,0),rect.inflate(-radius.w,0))
    rectangle.fill((0,0,0),rect.inflate(0,-radius.h))

    rectangle.fill(color,special_flags=BLEND_RGBA_MAX)
    rectangle.fill((255,255,255,alpha),special_flags=BLEND_RGBA_MIN)

    return rectangle

### UI ELEMENTS ###

# message class: derived from button class, see 'code cited' section
class Message(object):
    def __init__(self, msg, location, orientation, mode, alwaysShown=True, bg=data.white, fg=data.black):
        self.color = data.white
        self.bg, self.fg = bg, fg
        self.margin = 10
        self.mode = mode
        self.font = pygame.font.Font(None, 36)
        self.msg = msg

        self.alwaysShown = alwaysShown

        self.size = self.font.size(self.msg)
        self.size = (self.size[0] + self.margin, self.size[1] + self.margin)
        self.msgSurf = self.font.render(self.msg, 1, self.fg)
        self.msgRect = self.msgSurf.get_rect(center = [s//2 for s in self.size])

        self.surface = pygame.surface.Surface(self.size)

        if orientation == "midtop":
            self.rect = self.surface.get_rect(midtop = location)
        elif orientation == "topleft":
            self.rect = self.surface.get_rect(topleft = location)
        elif orientation == "center":
            self.rect = self.surface.get_rect(center = location)
        elif orientation == "midbottom":
            self.rect = self.surface.get_rect(midbottom = location)
        elif orientation == "bottomleft":
            self.rect = self.surface.get_rect(bottomleft = location)
        elif orientation == "bottomright":
            self.rect = self.surface.get_rect(bottomright = location)

        self.roundRect = self.rect
        self.roundRect[2] += self.margin
        self.roundRect[3] += self.margin
        self.msgX = self.roundRect.width//2 - (self.size[0]//2) + (self.margin//2)
        self.msgY = self.roundRect.height//2 - (self.size[1]//2) + (self.margin//2)
        self.msgPos = self.msgX, self.msgY

    def draw(self):
        self.surface = roundedRect(self.surface, self.roundRect, data.white)
        self.surface.blit(self.msgSurf, self.msgPos)
        data.screenSurf.blit(self.surface, self.roundRect)

# button class,  see 'code cited' section
class Button(Message):
    def __init__(self, msg, location, orientation, mode):
        super().__init__(msg, location, orientation, mode)
    def draw(self):
        self.mouseover()
        super().draw()
    def mouseover(self):
        self.bg = self.color
        mousePos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mousePos):
            self.bg = data.grey
    def mouseClick(self):
        mousePos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mousePos):
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

        #debugging frames
        #pygame.draw.rect(data.screenSurf, data.pink, self.rect, 2)

    def mouseClick(self):
        mousePos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mousePos):
            return True
        elif self.imageRect.collidepoint(mousePos):
            return True
        else:
            return False

# text box class: updates based on user or game state. see 'code cited' section
class TextBox(Button):
    def __init__(self, msg, text, location, orientation, mode):
        super().__init__(msg, location, orientation, mode)
        self.text = text
        self.active = False
        self.textSurf = self.font.render(self.text, 1, data.black)
        self.desc = data.tbDescs[msg]
        self.descFont = pygame.font.Font(None, 20)
        self.descSurf = self.descFont.render(self.desc, 1, data.black)

    def update(self):
        self.width = max(self.descSurf.get_width() + 2*self.margin, \
                         self.textSurf.get_width() + 2*self.margin, \
                         self.msgSurf.get_width() + 2*self.margin)
        self.height = self.size[1] + self.margin
        self.roundRect.width = self.width
        self.surface = pygame.surface.Surface((self.width, self.height))

        self.textX = self.roundRect.x + self.margin
        self.textY = self.roundRect.y + self.height//2 - self.textSurf.get_height()//2

    def draw(self):
        self.surface = roundedRect(self.surface, self.roundRect, data.white)
        if self.text == "":
            self.surface.blit(self.msgSurf, self.msgPos)
        data.screenSurf.blit(self.surface, self.roundRect)
        self.textSurf = self.font.render(self.text, 1, data.black)
        data.screenSurf.blit(self.descSurf, (self.rect.x, self.rect.y - 20))
        data.screenSurf.blit(self.textSurf, (self.textX, self.textY))



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
        self.y = data.midUpperY + (self.ID % 10) * (self.height + self.margin[1])
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

    def __repr__(self):
        return "__sliderID__" + str(self.ID) + ":" +  str(self.val)

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

### FOOD for pet feeding feature ###
class Food(object):
    def __init__(self, type, startPos):
        # types: 0 = cake, 1 = boba, 2 = donut
        self.type = type
        self.image = data.foodImages[type]
        self.startPos = startPos
        self.rect = self.image.get_rect()
        self.rect.bottomleft = startPos
        self.active = False
    def mouseClick(self):
        mousePos = pygame.mouse.get_pos()
        petRect = self.rect
        if (petRect.left < mousePos[0] < petRect.right) and \
            (petRect.top < mousePos[1] < petRect.bottom):
                return True
        else:
            return False
    def move(self):
        mousePos = pygame.mouse.get_pos()
        self.rect.bottomleft = mousePos
    def draw(self):
        data.screenSurf.blit(self.image, self.rect)


### PETS ###

# pet class
class Pet(object):
    def __init__(self, name, ID, traits):
        self.images = data.petImages
        # individual pet characteristics
        self.name = name
        self.traits = traits

        # get image based on those traits
        self.speciesID = int(createPet.featureDistance(self.traits))
        self.image = load_image(self.images[self.speciesID])
        self.image = pygame.transform.smoothscale(self.image, (300, 300))
        self.medImage = pygame.transform.smoothscale(self.image, (200, 200))
        self.smImage = pygame.transform.smoothscale(self.image, (150, 150))
        self.ID = ID

        # get rarity
        self.rarity = data.rarities[self.speciesID]
        self.desc = "Pets like %s have a rarity index of %f." \
                     % (self.name, self.rarity)

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

        self.fg = data.white
        self.bg = data.white

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
            self.rect = self.smImage.get_rect(topleft = self.pos)
            data.screenSurf.blit(self.smImage, self.pos)

        elif (data.mode == 2) or (data.mode == 5):
            self.pos = (data.width//2 - self.width//2, data.height//2 - self.height//2)
            self.rect = self.image.get_rect(topleft = self.pos)
            data.screenSurf.blit(self.image, self.pos)

        elif data.mode == 3:
            self.pos = (data.leftX, data.lowerY - self.smHeight)
            self.rect = self.smImage.get_rect(topleft = self.pos)
            data.screenSurf.blit(self.smImage, self.pos)

        # display name or not, based on mode
        if (data.mode == 0) or (data.mode == 2) or (data.mode == 5):
            self.nameX = self.pos[0] + self.rect.width//2
            self.nameY = self.pos[1] + self.rect.height + self.margin[1]//4

            self.namePos = (self.nameX, self.nameY)
            self.nameSurf = self.nameFont.render(self.name, 1, self.fg)
            self.nameRect = self.nameSurf.get_rect(midtop = self.namePos)
            data.screenSurf.blit(self.nameSurf, self.nameRect)

        elif data.mode == 3:
            self.nameX = self.pos[0] + self.rect.width + self.margin[0]
            self.nameY = self.pos[1]

            self.namePos = (self.nameX, self.nameY)
            self.nameSurf = self.nameFont.render(self.name, 1, self.fg)
            self.nameRect = self.nameSurf.get_rect(topleft = self.namePos)
            data.screenSurf.blit(self.nameSurf, self.nameRect)

        # display desc or not, based on mode
        if (data.mode == 2) or (data.mode == 3):
            self.nameSize, self.descSize = 44, 30
            if data.mode == 2:
                self.descX = self.nameX
                self.descY = self.nameY + self.margin[1]

                self.descPos = (self.descX, self.descY)
                self.descSurf = self.descFont.render(self.desc, 1, self.fg)
                self.descRect = self.descSurf.get_rect(midtop = self.descPos)
                data.screenSurf.blit(self.descSurf, self.descRect)

            else:
                self.descX = self.nameX
                self.descY = self.nameY + self.margin[1]

                self.descPos = (self.descX, self.descY)
                self.descSurf = self.descFont.render(self.desc, 1, self.fg)
                self.descRect = self.descSurf.get_rect(topleft = self.descPos)
                data.screenSurf.blit(self.descSurf, self.descRect)

    def mouseClick(self):
        mousePos = pygame.mouse.get_pos()
        petRect = self.rect
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

    listContents = contents.split("__pet__")[1:]
    for pet in listContents:
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
    petInfo = repr(pet)
    contents = readFile(file)
    newContents = contents + "__pet__" + petInfo
    writeFile(file, newContents)

# edit an existing pet
def editPet(file, newPet):
    newPetInfo = "__pet__" + repr(newPet)
    contents = readFile(file)
    listContents = contents.split("__pet__")[1:]

    newContents = ""
    for i in range(len(listContents)):
        petInfo = "__pet__" + listContents[i]
        if i == newPet.ID:
            newContents += newPetInfo
        else:
            newContents += petInfo

    writeFile(file, newContents)

# read the petSlider file
def getSliders(file):
    contents = readFile(file)
    if len(contents) < 2:
        return {}
    result = {}
    listContents = contents.split("__petID__")[1:]
    petID = 0
    for sliderSet in listContents:
        sliders = {}
        for slider in sliderSet.split("__sliderID__")[1:]:
            i = slider.index(":")
            key, value = int(slider[:i]), float(slider[i + 1:])
            sliders[key] = value
        result[petID] = sliders
        petID += 1
    return result

# add a new pet's slider values to the petSlider file
def addSlider(file, currPetSliders):
    contents = readFile(file)
    newContents = contents + "__petID__" + currPetSliders
    writeFile(file, newContents)

# edit a pet's slider values in the petSlider file
def editSlider(file, newSliders, petID):
    newSliders = "__petID__" + newSliders
    contents = readFile(file)
    listContents = contents.split("__petID__")[1:]
    newContents = ""
    for i in range(len(listContents)):
        sliderInfo = "__petID__" + listContents[i]
        if i == petID:
            newContents += newSliders
        else:
            newContents += sliderInfo
    writeFile(file, newContents)

# keep track of pets
class AllPets(object):
    def __init__(self):
        self.petlist = getPets("pets.txt")
        self.currentPet = None
        self.petname = ""
        # sliders set to these values when editing pet
        self.sliderCache = getSliders("petSliders.txt")
allPets = AllPets()

# main game function
def main():
    pygame.init()

    # load BG images
    loadingBG = pygame.transform.smoothscale(load_image('loadingBG.png'), (1074, data.screenRect.height))
    defaultBG = pygame.transform.smoothscale(load_image('background.jpg'), (1074, data.screenRect.height))
    mapBG = pygame.transform.smoothscale(load_image('mapbackground.jpg'), (1074, data.screenRect.height))

    # make the game window fancy!
    pygame.display.set_icon(data.petIcon)
    pygame.display.set_caption('Curse of Dimensionality: A Virtual Pet Game for Sad GANbreeders')

    # LOADING SCREEN
    data.screenSurf.blit(loadingBG, (data.bgX, 0))
    pygame.display.flip()

    # create clock to keep track of time
    clock = pygame.time.Clock()

    # initialize groups
    messages, buttons, backButtons, icons, sliders, editSliders = [], [], [], [], [], []
    foods = set()

    # initialize titles, buttons, sliders
    if pygame.font:

        # all back buttons
        for i in range(1, 7):
            backButton = Button(data.buttons["back"], (data.leftX, data.upperY), "topleft", i)
            buttons += [backButton]
            backButtons += [backButton]

        # mode 0: choose pet
        choosePetTitle = Message(data.titles["choose pet"], (data.centerX, data.upperY), "midtop", 0)
        noPetsYet = Message(data.buttons["no pets yet"], (data.centerX, data.upperY + 100), "center", 0, False)
        createPetButton = Button(data.buttons["create pet"], (data.centerX, data.lowerY), "midbottom", 0)

        # mode 1: create pet
        createPetTitle = Message(data.titles["create pet"], (data.centerX, data.upperY), "midtop", 1)
        nameTextBox = TextBox(data.textboxes["name"], "", (data.leftX, data.midUpperY - 20), "bottomleft", 1)
        getPetButton = Button(data.buttons["get pet"], (data.centerX, data.lowerY), "midbottom", 1)
        for i in range(len(data.categories)):
            slider = Slider(i, data.attributeSliders[i], 50, 100, 0, data.leftX, 1)
            sliders += [slider]

        # mode 6: edit pet
        editPetTitle = Message(data.titles["edit pet"], (data.centerX, data.upperY), "midtop", 6)
        changeNameTextBox = TextBox(data.textboxes["name"], "", (data.leftX, data.midUpperY - 20), "bottomleft", 6)
        updatePetButton = Button(data.buttons["update pet"], (data.centerX, data.lowerY), "midbottom", 6)
        for i in range(len(data.categories)):
            slider = Slider(i, data.attributeSliders[i], 50, 100, 0, data.leftX, 6)
            editSliders += [slider]

        # mode 2: show pet
        showPetTitle = Message(data.titles["show pet"], (data.centerX, data.upperY), "midtop", 2)
        goToMapButton = Button(data.buttons["go to map"], (data.centerX + 100, data.lowerY), "bottomleft", 2)
        editPetButton = Button(data.buttons["edit pet"], (data.centerX - 100, data.lowerY), "bottomright", 2)

        # mode 3: map
        mapTitle = Message(data.titles["map"], (data.centerX, data.upperY), "midtop", 3)
        cakeGameIcon = Icon(data.buttons["map"][0], (data.centerX + 250, data.lowerY - 400), "center", 3)
        feedPetIcon = Icon(data.buttons["map"][1], (data.centerX, data.lowerY - 100), "center", 3)
        foodTextBox = TextBox(data.textboxes["food"], data.foodMessage, (data.leftX, data.centerY), "topleft", 3)

        # mode 5: feed pet
        feedPetTitle = Message(data.titles["feed pet"], (data.centerX, data.upperY), "midtop", 5)
        foodTextBox2 = TextBox(data.textboxes["food"], data.foodMessage, (data.leftX, data.upperY + 100), "topleft", 5)
        feedCakeButton = Button(data.buttons["feed cake"], (data.centerX - 200, data.lowerY), "bottomright", 5)
        feedBobaButton = Button(data.buttons["feed boba"], (data.centerX, data.lowerY), "midbottom", 5)
        feedDonutButton = Button(data.buttons["feed donut"], (data.centerX + 200, data.lowerY), "bottomleft", 5)
        notEnoughFoods = Message(data.titles["not enough foods"], (data.centerX, data.lowerY - 50), "midbottom", 5, False)

        messages += [choosePetTitle, createPetTitle, showPetTitle, mapTitle, \
                     noPetsYet, editPetTitle, feedPetTitle, notEnoughFoods]
        buttons += [createPetButton, getPetButton, goToMapButton, nameTextBox, \
                    foodTextBox, editPetButton, updatePetButton, \
                    changeNameTextBox, feedCakeButton, feedBobaButton, \
                    feedDonutButton, foodTextBox2]
        icons += [cakeGameIcon, feedPetIcon]
        for slider in sliders:
            slider.draw()
        for slider in editSliders:
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
                    elif data.mode == 5:
                        data.mode = 3
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
                        ID = len(allPets.petlist)
                        # read sliders
                        traits = {}
                        currPetSliders = ""
                        for slider in sliders:
                            currPetSliders += repr(slider)
                            traits[slider.ID] = slider.getDecimal()
                            # reset sliders
                            slider.val = slider.max//2
                        # add pet's sliders to slider cache
                        addSlider('petSliders.txt', currPetSliders)
                        allPets.sliderCache = getSliders('petSliders.txt')

                        # add pet (they are stored in a file)
                        if len(allPets.petname) == 0:
                            name = "no name"
                        else:
                            name = allPets.petname
                        pet = Pet(name, ID, traits)
                        addPet('pets.txt', pet)
                        allPets.petlist = getPets('pets.txt')
                        allPets.currentPet = pet

                        # reset name
                        allPets.petname = ""
                        nameTextBox.text = ""

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

            # 2. SHOW PET SCREEN
            elif data.mode == 2:
                if event.type == MOUSEBUTTONDOWN:
                    # go to map button
                    if goToMapButton.mouseClick():
                        data.mode = 3
                    # edit pet button
                    elif editPetButton.mouseClick():
                        data.mode = 6
                        changeNameTextBox.text = allPets.currentPet.name
                        allPets.petname = changeNameTextBox.text
                        sliderVals = allPets.sliderCache[allPets.currentPet.ID]
                        for slider in editSliders:
                            slider.val = sliderVals[slider.ID]

            # 3. MAP SCREEN
            elif data.mode == 3:
                if event.type == MOUSEBUTTONDOWN:
                    # show pet
                    if allPets.currentPet.mouseClick():
                        data.mode = 2
                    # cake game button
                    elif cakeGameIcon.mouseClick():
                        data.mode = 4
                        cakegame.data.__init__()
                        prizes = cakegame.main(data.petImages[allPets.currentPet.speciesID])
                        data.cakes += prizes[0]
                        data.bobas += prizes[1]
                        data.donuts += prizes[2]
                        foodTextBox.text = ("You have " + str(data.cakes) + \
                                           " cakes, " + str(data.bobas) + \
                                           " bobas, and " + str(data.donuts) + \
                                           " donuts.")
                        data.mode = 3
                    # feed pet button
                    elif feedPetIcon.mouseClick():
                        data.mode = 5

            # 5. FEED PET SCREEN
            elif data.mode == 5:
                if event.type == MOUSEBUTTONDOWN:
                    if (feedCakeButton.mouseClick() or
                        feedBobaButton.mouseClick() or feedDonutButton.mouseClick()):

                        # feed pet cake
                        if feedCakeButton.mouseClick():
                            if data.cakes < 1:
                                data.notEnoughFoods = True
                            else:
                                cake = Food(0, data.foodStartPos)
                                foods.add(cake)

                        # feed pet boba
                        elif feedBobaButton.mouseClick():
                            if data.bobas < 1:
                                data.notEnoughFoods = True
                            else:
                                boba = Food(1, data.foodStartPos)
                                foods.add(boba)

                        # feed pet donut
                        elif feedDonutButton.mouseClick():
                            if data.donuts < 1:
                                data.notEnoughFoods = True
                            else:
                                donut = Food(2, data.foodStartPos)
                                foods.add(donut)

                    for food in foods:
                        if food.mouseClick():
                            food.active = True

                elif event.type == MOUSEBUTTONUP:
                    for food in foods:
                        # the food item that is active
                        if food.mouseClick():
                            food.active = False

                            if food.type == 0:
                                # feeding your pet CAKE:
                                # increases (strawberry, angora, axolotl, sea cucumber)
                                # decreases (gown, persian cat, hoopskirt, acorn, siamese cat)
                                traits = allPets.currentPet.traits
                                addTraits = (0, 1, 2, 3)
                                subtractTraits = (4, 5, 6, 7, 8)
                                for trait in traits:
                                    if trait in addTraits:
                                        traits[trait] = min(traits[trait] * 1.1, 0.99)
                                    elif trait in subtractTraits:
                                        traits[trait] = max(traits[trait] * 0.9, 0.0)
                            elif food.type == 1:
                                # feeding your pet BOBA:
                                # increases (gown, persian cat, hoopskirt, acorn, siamese cat)
                                # decreases (bath towel, dough, coffeepot, screen)
                                traits = allPets.currentPet.traits
                                addTraits = (4, 5, 6, 7, 8)
                                subtractTraits = (9, 10, 11, 12)
                                for trait in traits:
                                    if trait in addTraits:
                                        traits[trait] = min(traits[trait] * 1.1, 0.99)
                                    elif trait in subtractTraits:
                                        traits[trait] = max(traits[trait] * 0.9, 0.0)
                            elif food.type == 2:
                                # feeding your pet DONUTS:
                                # increases (bath towel, dough, coffeepot, screen)
                                # decreases (strawberry, angora, axolotl, sea cucumber)
                                traits = allPets.currentPet.traits
                                addTraits = (9, 10, 11, 12)
                                subtractTraits = (0, 1, 2, 3)
                                for trait in traits:
                                    if trait in addTraits:
                                        traits[trait] = min(traits[trait] * 1.4, 0.99)
                                    elif trait in subtractTraits:
                                        traits[trait] = max(traits[trait] * 0.6, 0.0)

                            # update pet with new traits
                            newPet = Pet(allPets.currentPet.name, allPets.currentPet.ID, traits)
                            editPet('pets.txt', newPet)
                            allPets.petlist = getPets('pets.txt')
                            allPets.currentPet = newPet

                            # update pet's sliders
                            newPetSliders = ""
                            for trait in traits:
                                fauxSlider = "__sliderID__" + str(trait) + ":" +  str((traits[trait] * 100))
                                newPetSliders += fauxSlider
                            editSlider('petSliders.txt', newPetSliders, allPets.currentPet.ID)
                            allPets.sliderCache = getSliders('petSliders.txt')

            # 6. EDIT PET SCREEN
            elif data.mode == 6:
                if event.type == MOUSEBUTTONDOWN:
                    # update pet button
                    if updatePetButton.mouseClick():

                        traits = {}
                        newPetSliders = ""
                        for slider in editSliders:
                            traits[slider.ID] = slider.getDecimal()
                            newPetSliders += repr(slider)
                            # reset edit sliders
                            slider.val = slider.max//2
                        ID = allPets.currentPet.ID
                        # update slider cache
                        editSlider('petSliders.txt', newPetSliders, ID)
                        allPets.sliderCache = getSliders('petSliders.txt')

                        # edit pet
                        if len(allPets.petname) == 0:
                            name = "no name"
                        else:
                            name = allPets.petname
                        newPet = Pet(name, ID, traits)
                        editPet('pets.txt', newPet)

                        allPets.petlist = getPets('pets.txt')
                        allPets.currentPet = newPet

                        # reset name
                        allPets.petname = ""
                        nameTextBox.text = ""

                        data.mode = 2

                    # activate the change name textbox
                    elif changeNameTextBox.mouseClick():
                        changeNameTextBox.active = not changeNameTextBox.active

                    # activate sliders
                    pos = pygame.mouse.get_pos()
                    for slider in editSliders:
                        if slider.buttonRect.collidepoint(pos):
                            slider.hit = True

                elif event.type == KEYDOWN:
                    # fill the change name textbox
                    allPets.petname = changeNameTextBox.text
                    if event.key == K_BACKSPACE:
                        if len(nameTextBox.msg) > 0:
                            changeNameTextBox.text = changeNameTextBox.text[:-1]
                    else:
                        changeNameTextBox.text += event.unicode
                        allPets.petname = changeNameTextBox.text

                # deactivate edit sliders
                elif event.type == MOUSEBUTTONUP:
                    for slider in editSliders:
                        slider.hit = False

        # update all objects
        for slider in sliders:
            if slider.hit:
                slider.move()
        for slider in editSliders:
            if slider.hit:
                slider.move()
        for button in buttons:
            if isinstance(button, TextBox):
                button.update()
        newFoods = set()
        for food in foods:
            if food.active:
                food.move()
            if not allPets.currentPet.rect.contains(food.rect):
                newFoods.add(food)
        foods = newFoods


        # draw backgrounds
        if data.mode == 3:
            data.screenSurf.blit(mapBG, (data.bgX, 0))
        else:
            data.screenSurf.blit(defaultBG, (data.bgX, 0))

        # draw all objects
        for button in buttons:
            if button.mode == data.mode:
                button.draw()
        for message in messages:
            if message.mode == data.mode:
                if message.alwaysShown:
                    message.draw()
                elif (message.msg == "No pets yet :(") and (len(allPets.petlist) == 0):
                    message.draw()
                elif (message.msg == "You don't have any of those!") and (data.notEnoughFoods == True):
                    message.draw()
                    data.notEnoughFoods = False

        for slider in sliders:
            if slider.mode == data.mode:
                slider.draw()
        for slider in editSliders:
            if slider.mode == data.mode:
                slider.draw()
        for icon in icons:
            if data.mode == 3:
                icon.draw()
        for pet in allPets.petlist:
            if data.mode == 0:
                pet.draw()
            elif (pet == allPets.currentPet) and (data.mode != 1) and (data.mode != 6):
                pet.draw()
        for food in foods:
            food.draw()

        pygame.display.flip()
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()

### Bibliography ###
# Code cited/taken from other sources:
# Textboxes: https://stackoverflow.com/questions/46390231/how-to-create-a-text-input-box-with-pygame
# Buttons and sliders: https://www.dreamincode.net/forums/topic/401541-buttons-and-sliders-in-pygame
# Rounded Rectangles: https://www.pygame.org/project-AAfilledRoundedRect-2349-.html
# General Pygame: https://www.pygame.org/docs/

# Images:
# Backgrounds processed with DeepDreamGenerator: deepdreamgenerator.com
# Pet images collected from GANbreeder: ganbreeder.app