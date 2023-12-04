import random
from typing import List

from ltga import Individual

class Mutation:

    def __init__(self, evaluator):
        self.evaluator = evaluator

    def mutate(self, individuals: List[Individual]):
        rate = int(len(individuals) / 2)

        for _ in range(rate):
            individual = individuals[random.randint(int(len(individuals) / 2), len(individuals) - 1)]
            for j in range(int(len(individual.genes) / 10)):
                i1, i2 = random.randint(0, len(individual.genes) - 1), random.randint(0, len(individual.genes) - 1)
                individual.genes[i1], individual.genes[i2] = individual.genes[i2], individual.genes[i1]
                individual.fitness = self.evaluator.evaluate(individual.genes)
        return individuals
