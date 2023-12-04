from .Mask import getMaskValue, setMaskValues
from .Individual import Individual


def applyMask(p1, p2, mask):
    maskSet = set(mask)
    return Individual([p2.genes[g] if g in maskSet else p1.genes[g]
                       for g in range(len(p1.genes))])


def globalCrossover(individuals, masks):
    values = {mask: [] for mask in masks}
    for mask in masks:
        for individual in individuals:
            value = getMaskValue(individual, mask)
            values[mask].append(value)
    for individual in individuals:
        for mask in masks:
            # """
            startingValue = getMaskValue(individual, mask)
            setMaskValues(individual, mask, startingValue)
            newFitness = yield individual
            if individual.fitness > newFitness:
                individual.fitness = newFitness
            else:
                setMaskValues(individual, mask, startingValue)
            # """
        """
            startingValue = getMaskValue(individual, mask)
            options = [value for value in values[mask]
                       if value != startingValue]
            if len(options) > 0:
                value = random.choice(options)
                setMaskValues(individual, mask, value)
                newFitness = yield individual
                # if the individual improved, update fitness
                if individual.fitness < newFitness:
                    individual.fitness = newFitness
                # The individual did not improve, revert changes
                else:
                    setMaskValues(individual, mask, startingValue)
        """
