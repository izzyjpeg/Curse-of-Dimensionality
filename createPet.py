import math

categories = ["strawberry", "angora", "axolotl", "seaCucumber", "gown", \
              "persianCat", "hoopskirt", "acorn", "siameseCat", "bathTowel",\
              "dough", "coffeepot"]
# add "screen"
catNums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

img0 = {0 : 0.0, 1 : 0.4168, 2 : 0.0, 3 : 0.0, 4 : 0.0, 5 : 0.0, 6 : 0.0, \
        7 : 0.3627, 8 : 0.0, 9 : 0.0, 10 : 0.0, 11 : 0.2204}
img1 = {0 : 0.0, 1 : 0.0, 2 : 0.0, 3 : 0.0, 4 : 0.0, 5 : 0.0, 6 : 0.0, \
        7 : 0.0, 8 : 0.4653, 9 : 0.1126, 10 : 0.4220, 11 : 0.0}
img2 = {0 : 0.2211, 1 : 0.5834, 2 : 0.2210, 3 : 0.3520, 4 : 0.6617, 5 : 0.0, \
        6 : 0.0, 7 : 0.0, 8 : 0.0, 9 : 0.0, 10 : 0.0, 11 : 0.0}
img3 = {0 : 0.6232, 1 : 0.3228, 2 : 0.2781, 3 : 0.3463, 4 : 0.5567, 5 : 0.0, \
        6 : 0.0, 7 : 0.0, 8 : 0.0, 9 : 0.0, 10 : 0.0, 11 : 0.0}
img4 = {0 : 0.4078, 1 : 0.6695, 2 : 0.3525, 3 : 0.2996, 4 : 0.4139, 5 : 0.0, \
        6 : 0.0, 7 : 0.0, 8 : 0.0, 9 : 0.0, 10 : 0.0, 11 : 0.0}
img5 = {0 : 0.2668, 1 : 0.0, 2 : 0.6489, 3 : 0.5217, 4 : 0.0, 5 : 0.0, \
        6 : 0.0, 7 : 0.0, 8 : 0.0, 9 : 0.0, 10 : 0.0, 11 : 0.0}
img6 = {0 : 0.2745, 1 : 0.0, 2 : 0.4341, 3 : 0.0, 4 : 0.0, 5 : 0.0, 6 : 0.0, \
        7 : 0.0, 8 : 0.0, 9 : 0.0, 10 : 0.0, 11 : 0.0}
img7 = {0 : 0.0, 1 : 0.0, 2 : 0.0, 3 : 0.0, 4 : 0.0, 5 : 0.6472, 6 : 0.1226, \
        7 : 0.2300, 8 : 0.0, 9 : 0.0, 10 : 0.0, 11 : 0.0}
img8 = {0 : 0.6040, 1 : 0.0, 2 : 0.0, 3 : 0.0, 4 : 0.0, 5 : 0.0, \
        6 : 0.0, 7 : 0.0, 8 : 0.6163, 9 : 0.4649, 10 : 0.0, 11 : 0.0}
img9 = {0 : 0.02526, 1 : 0.0412, 2 : 0.8562, 3 : 0.0, 4 : 0.0, 5 : 0.0, \
        6 : 0.0, 7 : 0.0, 8 : 0.0, 9 : 0.1299, 10 : 0.4909, 11 : 0.0}
img10 = {0 : 0.2826, 1 : 0.2826, 2 : 0.2826, 3 : 0.2826, 4 : 0.2826, 5 : 0.2826, \
        6 : 0.2826, 7 : 0.2826, 8 : 0.2826, 9 : 0.2826, 10 : 0.2826, 11 : 0.2826}

# Categories
# 0: strawberry
# 1: angora
# 2: axolotl
# 3: sea cucumber
# 4: gown
# 5: persian cat
# 6: hoopskirt
# 7: acorn
# 8: siamese cat
# 9: bath towel
# 10: dough
# 11: coffeepot


images = {"img0" : img0, "img1" : img1, "img2" : img2, "img3" : img3, "img4" : img4, \
          "img5" : img5, "img6" : img6, "img7": img7, "img8" : img8, \
          "img9" : img9}#, "img10" : img10}

examplePet = {0 : 0.8, 1 : 0.8, 2 : 0.2, 3 : 0.1, 4 : 0.4, 5: 0.6, 6: 0.3, \
              7: 0.8, 8 : 0.4653, 9 : 0.1126, 10 : 0.4220, 11 : 0.0}

def featureDistance(userInput):

    bestImg = None
    bestDistance = None

    for key in images:
        sums = 0
        img = images[key]
        for i in range(len(categories)):
            category = catNums[i]

            userFeature = userInput[category]
            imgFeature = img[category]
            sums += (userFeature - imgFeature)**2
        distance = math.sqrt(sums)
        if (bestDistance == None) or (distance < bestDistance):
            bestDistance = distance
            bestImg = key

    imageID = (str(bestImg).split("img"))[1]
    return imageID

#print(featureDistance(examplePet))