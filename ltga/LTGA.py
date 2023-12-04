import random
from itertools import combinations
from ltga.Mutation import Mutation


class LTGA(object):

    def buildTree(self, distance):
        clusters = [(i,) for i in range(len(self.individuals[0].genes))]
        subtrees = [(i,) for i in range(len(self.individuals[0].genes))]
        random.shuffle(clusters)
        random.shuffle(subtrees)
        lookup = {}

        def allLowest():
            minVal = 3
            results = []
            for c1, c2 in combinations(clusters, 2):
                result = distance(self.individuals, c1, c2, lookup)
                if result < minVal:
                    minVal = result
                    results = [(c1, c2)]
                if result == minVal:
                    results.append((c1, c2))
            return results

        while len(clusters) > 1:
            c1, c2 = random.choice(allLowest())
            clusters.remove(c1)
            clusters.remove(c2)
            combined = c1 + c2
            clusters.append(combined)
            if len(clusters) != 1:
                subtrees.append(combined)
        return subtrees

    def smallestFirst(self, subtrees):
        return sorted(subtrees, key=len)

    def generate(self, initialPopulation, evaluator, distanceFcn, crossoverFcn):
        self.individuals = initialPopulation
        distance = distanceFcn
        ordering = self.smallestFirst
        crossover = crossoverFcn
        beforeGenerationSet = set(self.individuals)
        while True:
            subtrees = self.buildTree(distance)
            masks = ordering(subtrees)
            generator = crossover(self.individuals, masks)

            individual = next(generator)
            while True:
                fitness = yield individual
                try:
                    individual = generator.send(fitness)
                except StopIteration:
                    break

            self.individuals = Mutation(evaluator).mutate(self.individuals)

            #If all individuals are identical
            currentSet = set(self.individuals)
            if (len(currentSet) == 1 or
                    currentSet == beforeGenerationSet):
                break
            beforeGenerationSet = currentSet
