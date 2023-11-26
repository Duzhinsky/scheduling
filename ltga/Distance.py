from .Mask import getMaskValue
import math

def entropy(individuals, mask, lookup):
    '''
    Calculates the current populations entropy for a given mask.

    Parameters:

    - ``mask``: The list of indices to examine
    - ``lookup``: A dictionary containing entropy values already found for
      this population.  Should be reset if the population changes.
    '''
    try:
        return lookup[mask]
    except KeyError:
        occurances = {}
        for individual in individuals:
            # extract the gene values for the cluster
            value = getMaskValue(individual, mask)
            try:
                occurances[value] += 1
            except KeyError:
                occurances[value] = 1
        total = float(len(individuals))
        result = -sum(x / total * math.log(x / total, 2)
                      for x in iter(occurances.values()))
        lookup[mask] = result
        return result

def clusterDistance(individuals, c1, c2, lookup):
    '''
    Calculates the true entropic distance between two clusters of genes.

    Parameters:

    - ``c1``: The first cluster.
    - ``c2``: The second cluster.
    - ``lookup``: A dictionary mapping cluster pairs to their previously
      found distances.  Should be reset if the population changes.
    '''
    try:
        return lookup[c1, c2]
    except KeyError:
        try:
            result = 2 - ((entropy(individuals, c1, lookup) +
                           entropy(individuals, c2, lookup))
                          / entropy(individuals, c1 + c2, lookup))
        except ZeroDivisionError:
            result = 2  # Zero division only happens in 0/0
        lookup[c1, c2] = result
        lookup[c2, c1] = result
        return result


def pairwiseDistance(individuals, c1, c2, lookup):
    '''
    Calculates the pairwise approximation of the entropic distance between
    two clusters of genes.

    Parameters:

    - ``c1``: The first cluster.
    - ``c2``: The second cluster.
    - ``lookup``: A dictionary mapping cluster pairs to their previously
      found distances.  Should be reset if the population changes.
    '''
    try:
        return lookup[c1, c2]
    except KeyError:
        # averages the pairwise distance between each cluster
        result = sum(clusterDistance(individuals, (a,), (b,), lookup) for a in c1 for b in c2) / float(len(c1) * len(c2))
        lookup[c1, c2] = result
        lookup[c2, c1] = result
        return result
