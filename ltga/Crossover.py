import random
from .Mask import getMaskValue, setMaskValues
from .Individual import Individual


def applyMask(p1, p2, mask):
    '''
    Used by two parent crossover to create an individual by coping the
    genetic information from p2 into a clone of p1 for all genes in the
    given mask.  Returns the newly created individual.

    Parameters:

    - ``p1``: The first parent.
    - ``p2``: The second parent.
    - ``mask``: The list of indices used in this crossover.
    '''
    maskSet = set(mask)
    return Individual([p2.genes[g] if g in maskSet else p1.genes[g]
                       for g in range(len(p1.genes))])


def twoParentCrossover(individuals, masks):
    '''
    Creates individual generator using the two parent crossover variant.
    Uses coroutines to send out individuals and receive their fitness
    values.  Terminates when a complete evolutionary generation has
    finished.

    Parameters:

    - ``masks``: The list of crossover masks to be used when generating
      individuals, ordered based on how they should be applied.
    '''
    offspring = []
    # Does the following twice in order to make enough children
    for _ in [0, 1]:
        random.shuffle(individuals)
        # pairs off parents with their neighbor
        for i in range(0, len(individuals) - 1, 2):
            p1 = individuals[i]
            p2 = individuals[i + 1]
            for mask in masks:
                c1 = applyMask(p1, p2, mask)
                c2 = applyMask(p2, p1, mask)
                # Duplicates are caught higher up
                c1.fitness = yield c1
                c2.fitness = yield c2
                # if the best child is better than the best parent
                if max(p1.fitness, p2.fitness) > max(c1.fitness, c2.fitness):
                    p1, p2 = c1, c2
            # Overwrite the parents with the modified version
            individuals[i] = p1
            individuals[i + 1] = p2
            # The offspring is the best individual created during the cross
            offspring.append(max(p1.fitness, p2.fitness))
    individuals = offspring


def globalCrossover(individuals, masks):
    '''
    Creates individual generator using the global crossover variant.
    Uses coroutines to send out individuals and receive their fitness
    values.  Terminates when a complete evolutionary generation has
    finished.

    Parameters:

    - ``masks``: The list of crossover masks to be used when generating
      individuals, ordered based on how they should be applied.
    '''
    # Creates a dictionary to track individual's values for each mask
    values = {mask: [] for mask in masks}
    for mask in masks:
        for individual in individuals:
            value = getMaskValue(individual, mask)
            values[mask].append(value)
    # each individual creates a single offspring, which replaces itself
    for individual in individuals:
        for mask in masks:
            # """
            startingValue = getMaskValue(individual, mask)
            # Find the list of values in the population that differ from
            # the current individual's values for this mask
            setMaskValues(individual, mask, startingValue)
            newFitness = yield individual
            # if the individual improved, update fitness
            if individual.fitness > newFitness:
                individual.fitness = newFitness
            # The individual did not improve, revert changes
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
