from .Individual import Individual


def getMaskValue(individual: Individual, mask):
    return tuple(individual.genes[g] for g in mask)


def setMaskValues(individual: Individual, mask, value):
    for valueIndex, geneIndex in enumerate(mask):
        individual.genes[geneIndex] = value[valueIndex]
