'''
This module contains the implementation of LTGA itself.  It includes
functionality for each of the variants
'''
import random
from itertools import combinations
from ltga.Mutation import Mutation


class LTGA(object):
    '''
    Class containing all of the LTGA functionality.  Uses the coroutine
    design structure to interact with problems being optimized.  To use,
    create an LTGA object and then call the ``generate`` function.  This
    will send out individuals and expects their fitness to be sent back in.
    '''

    def buildTree(self, distance):
        '''
        Given a method of calculating distance, build the linkage tree for the
        current population.  The tree is built by finding the two clusters with
        the minimum distance and merging them into a single cluster.  The
        process is initialized with all possible clusters of size 1 and ends
        when only a single cluster remains.  Returns the subtrees in the order
        they were created.

        Parameters:

        - ``distance``: The method of calculating distance.  Current options
          are ``self.clusterDistance`` and ``self.pairwiseDistance``
        '''
        clusters = [(i,) for i in range(len(self.individuals[0].genes))]
        subtrees = [(i,) for i in range(len(self.individuals[0].genes))]
        random.shuffle(clusters)
        random.shuffle(subtrees)
        lookup = {}

        def allLowest():
            '''
            Internal function used to find the list of all clusters pairings
            with the current smallest distances.
            '''
            minVal = 3  # Max possible distance should be 2
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
            # Only add it as a subtree if it is not the root
            if len(clusters) != 1:
                subtrees.append(combined)
        return subtrees

    def leastLinkedFirst(self, subtrees):
        '''
        Reorders the subtrees such that the cluster pairs with the least
        linkage appear first in the list.  Assumes incoming subtrees are
        ordered by when they were created by the ``self.buildTree`` function.

        Parameters:

        - ``subtrees``: The list of subtrees ordered by how they were
          originally created.
        '''
        return list(reversed(subtrees))

    def smallestFirst(self, subtrees):
        '''
        Reorders the subtrees such that the cluster pairs with the smallest
        number of genes appear first in the list.  Assumes incoming subtrees
        are ordered by when they were created by the ``self.buildTree``
        function.

        Parameters:

        - ``subtrees``: The list of subtrees ordered by how they were
          originally created.
        '''
        return sorted(subtrees, key=len)

    def generate(self, initialPopulation, evaluator, distanceFcn, crossoverFcn, config):
        '''
        The individual generator for the LTGA population.  Sends out
        individuals that need to be evaluated and receives fitness information.
        Will continue sending out individuals until the population contains
        only one unique individual or a generation passes without the set of
        unique individuals changing.

        Parameters:

        - ``initialPopulation``: The list of individuals to be used as the
          basis for LTGA's evolution.  These individuals should already have
          fitness values set.  If local search is to be performed on the
          initial population, it should be done before sending to this
          function.
        - ``config``: A dictionary containing all configuration information
          required by LTGA to generate individuals.  Should include values
          for:

          - ``distance``: The method used to determine the distance between
            clusters, for instance ``clusterDistance`` and
            ``pairwiseDistance``.
          - ``ordering``: The method used to determine what order subtrees
            should be used as crossover masks, for instance
            ``leastLinkedFirst`` and ``smallestFirst``.
          - ``crossover``: The method used to generate new individuals, for
            instance ``twoParentCrossover`` and ``globalCrossover``.
        '''
        self.individuals = initialPopulation
        distance = distanceFcn
        ordering = self.smallestFirst # TODO change
        # ordering = Util.classMethods(self)[config["ordering"]]
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
