import math

categories = ["strawberry", "angora", "axolotl", "seaCucumber", "gown"]
numCats = len(categories)

img1 = {"strawberry" : 0.9, "angora" : 0.9, "axolotl" : 0.1, "seaCucumber" : 0.2, "gown" : 0.3}
img2 = {"strawberry" : 0.1, "angora" : 0.1, "axolotl" : 0.8, "seaCucumber" : 0.9, "gown" : 0.7}
img3 = {"strawberry" : 0.2211, "angora" : 0.5834, "axolotl" : 0.2210, "seaCucumber" : 0.3520, "gown" : 0.6617}
img4 = {"strawberry" : 0.6232, "angora" : 0.3238, "axolotl" : 0.2781, "seaCucumber" : 0.3463, "gown" : 0.5567}
img5 = {"strawberry" : 0.4078, "angora" : 0.6695, "axolotl" : 0.3525, "seaCucumber" : 0.2996, "gown" : 0.4139}
img6 = {"strawberry" : 0.2668, "angora" : 0.0, "axolotl" : 0.6489, "seaCucumber" : 0.5217, "gown" : 0.0}

images = {"img1" : img1, "img2" : img2, "img3" : img3, "img4" : img4, "img5" : img5, "img6" : img6}

examplePet = {"strawberry" : 0.8, "angora" : 0.8, "axolotl" : 0.2, "seaCucumber" : 0.1, "gown" : 0.4}

def featureDistance(userInput):

    bestImg = None
    bestDistance = None

    for key in images:
        sums = 0
        img = images[key]
        for category in categories:
            userFeature = userInput[category]
            imgFeature = img[category]
            sums += (userFeature - imgFeature)**2
        distance = math.sqrt(sums)
        if (bestDistance == None) or (distance < bestDistance):
            bestDistance = distance
            bestImg = key

    imageID = str(bestImg)[-1]
    return imageID
