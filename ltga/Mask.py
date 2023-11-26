from .Individual import Individual


def getMaskValue(individual: Individual, mask):
    '''
    Gets the individual's gene values for the given mask

    Parameters:

    - ``individual``: The individual to get gene information from
    - ``mask``: The list of indices to get information from
    '''
    return tuple(individual.genes[g] for g in mask)


def setMaskValues(individual: Individual, mask, value):
    '''
    Sets the individual's gene values for the given mask

    Parameters:

    - ``individual``: The individual who's genes are changing.
    - ``mask``: The list of indices to change.
    - ``value``: The list of values to change to.
    '''
    for valueIndex, geneIndex in enumerate(mask):
        individual.genes[geneIndex] = value[valueIndex]
