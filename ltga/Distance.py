from .Mask import getMaskValue
import math

def entropy(individuals, mask, lookup):
    try:
        return lookup[mask]
    except KeyError:
        occurances = {}
        for individual in individuals:
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
    try:
        return lookup[c1, c2]
    except KeyError:
        try:
            result = 2 - ((entropy(individuals, c1, lookup) +
                           entropy(individuals, c2, lookup))
                          / entropy(individuals, c1 + c2, lookup))
        except ZeroDivisionError:
            result = 2
        lookup[c1, c2] = result
        lookup[c2, c1] = result
        return result


def pairwiseDistance(individuals, c1, c2, lookup):
    try:
        return lookup[c1, c2]
    except KeyError:
        result = sum(clusterDistance(individuals, (a,), (b,), lookup) for a in c1 for b in c2) / float(len(c1) * len(c2))
        lookup[c1, c2] = result
        lookup[c2, c1] = result
        return result
