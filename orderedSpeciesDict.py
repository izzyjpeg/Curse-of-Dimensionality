# This file shows how I spaced out the features.

### Functions to Space Out the Features
# This data had too many clusters, so I spread them out.
from speciesDict import speciesDict
numSpecies = len(speciesDict)
# initialize category dict
orderedCats = {}
for i in range(12 + 1):
    orderedCats[i] = []
# first, sort the data by category (feature) instead of by species (data point)
for species in speciesDict:
    for category in speciesDict[species]:
        orderedCats[category] += [  [species, speciesDict[species][category]]  ]
# within each category, sort from smallest to largest value
for category in orderedCats:
    unordered = orderedCats[category]
    unordered.sort(key=lambda x: x[1])
    orderedCats[category] = unordered

# Now, for each category, assign each species a more 'spaced out' value
# i.e. if there were 5 species, cat 0 would be 0.1, 0.3, 0.5, 0.7, and 0.9
for category in orderedCats:
    for i in range(numSpecies):
        newVal = (1.0/numSpecies)*i - (1.0/numSpecies)//2
        orderedCats[category][i][1] = newVal

# make a new speciesDict where things are all nice and spaced out
orderedSpeciesDict = {}
for i in range(numSpecies):
    key = "sp" + str(i)
    orderedSpeciesDict[key] = {}
for category in orderedCats:
    for speciesVal in orderedCats[category]:
        species = speciesVal[0]
        val = speciesVal[1]
        orderedSpeciesDict[species][category] = val