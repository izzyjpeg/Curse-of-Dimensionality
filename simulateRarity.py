# This is the file that calculates pet rarity.


# Monte Carlo process template came from the 112 website.
# https://www.cs.cmu.edu/~112/notes/notes-monte-carlo.html
import random, math
from speciesDict import speciesDict

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

# generates a random position for each slider
def randomPet():
    pet = {}
    for i in range(len(catNums)):
        pet[i] = random.random()
    return pet

# runs featureDistance (trials) # of times
def petSim(trials):
    counts = {}
    for i in range(len(speciesDict)):
        counts[i] = 0
    for trial in range(trials):
        pet = randomPet()
        petID = int(featureDistance(pet))
        counts[petID] += 1
    return counts

# formats counts as odds
def petOdds(trials):
    counts = petSim(trials)
    odds = {}
    for petID in counts:
        odds[petID] = counts[petID] / trials
    return odds

# alternatively, formats counts for printing
def showPetSim(trials):
    counts = petSim(trials)
    strCounts = ""

    mostCommonPet = None
    highest = None

    for petID in counts:
        strCounts += str(petID) + " : " + str(counts[petID]) + "\n"
        if (highest == None) or (counts[petID] > highest):
            highest = counts[petID]
            mostCommonPet = petID

    result =  ("Counts: " + strCounts + "\nMost Common Pet: " \
                + str(mostCommonPet) + " with " + str(highest) + " hits.")
    return result