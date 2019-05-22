###  This is the algorithm to choose a pet.

import math
### switch these two to go back to cluster-y data
#from speciesDict import speciesDict
from cachedOrderedSpeciesDict import orderedSpeciesDict as speciesDict

categories = ["strawberry", "angora", "axolotl", "seaCucumber", "gown", \
              "persianCat", "hoopskirt", "acorn", "siameseCat", "bathTowel",\
              "dough", "coffeepot", "screen"]
catNums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

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
# 12: screen

examplePet = {0 : 0.8, 1 : 0.8, 2 : 0.2, 3 : 0.1, 4 : 0.4, 5: 0.6, 6: 0.3, \
              7: 0.8, 8 : 0.4653, 9 : 0.1126, 10 : 0.4220, 11 : 0.0, 12 : 0.0}

# The normalization dict calculates a min and max for each individual category,
# based on the data we actually have. This ensures that choices the user makes,
# via the sliders, are properly reflected with a change in species.
normalization = {}
for i in range(len(catNums)):
    category = catNums[i]
    catMax = None
    catMin = None

    for key in speciesDict:
        species = speciesDict[key]
        speciesFeature = species[category]
        if (catMin == None) or (speciesFeature < catMin):
            catMin = speciesFeature

    for key in speciesDict:
        species = speciesDict[key]
        speciesFeature = species[category]
        if (catMax == None) or (speciesFeature > catMax):
            catMax = speciesFeature

    normalization[i] = [catMin, catMax]


def featureDistance(userInput):
    bestSpecies = None
    bestDistance = None

    for key in speciesDict:
        sums = 0
        species = speciesDict[key]

        for i in range(len(catNums)):

            category = catNums[i]
            catMin = normalization[i][0]
            catMax = normalization[i][1]

            # weights are no longer necessary
            # angora, persian cat, and siamese cat are less heavily weighted
            #if (i == 1) or (i == 5) or (i == 8):
             #   weight = 0.5
            #elif (i == 0):
             #   weight = 0.7
            #else:
             #   weight = 1.0
            weight = 1.0

            userFeature = userInput[category]
            userFeature = weight*((userFeature - catMin)/catMax)

            speciesFeature = species[category]
            speciesFeature = weight*((speciesFeature - catMin)/catMax)

            sums += (userFeature - speciesFeature)**2

        distance = math.sqrt(sums)
        if (bestDistance == None) or (distance < bestDistance):
            bestDistance = distance
            bestSpecies = key

    speciesID = (str(bestSpecies).split("sp"))[1]
    return speciesID