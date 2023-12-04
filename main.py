import copy
from random import shuffle
from typing import List

import ltga.Distance
from job import Job
from ltga.Crossover import globalCrossover
from ltga.FitnessFunction import ScheduleFitness
from ltga.Individual import Individual
from ltga.LTGA import LTGA
from ltga.Mutation import Mutation

def makeInitialPopulation(jobs: List[Job], evaluator, pop_size) -> List[Individual]:
    M = len(jobs[0].actions)
    N = len(jobs)
    individuals = [Individual([i for i in range(N) for _ in range(M)]) for _ in range(pop_size)]
    for individual in individuals:
        shuffle(individual.genes)
        individual.fitness = evaluator.evaluate(individual.genes)
    return individuals


def ltga_run(population, evaluator):
    evals = 0
    max_evals = 100000

    new_pop = sorted(copy.deepcopy(population), key=lambda x: x.fitness)
    optimizer = LTGA().generate(population, evaluator, ltga.Distance.pairwiseDistance, globalCrossover)
    try:
        individual = next(optimizer)  # Get the first individual
        while (evals < max_evals):
            fitness = evaluator.evaluate(individual.genes)
            if fitness < new_pop[0].fitness:
                for i in range(1, len(new_pop)):
                    new_pop[i] = new_pop[i - 1]
                new_pop[0] = individual
            evals += 1
            individual = optimizer.send(fitness)
    except StopIteration:
        pass
    return new_pop


def one_run(jobs_data):
    results = []
    evaluator = ScheduleFitness(jobs_data)
    mut = Mutation(evaluator)
    population = makeInitialPopulation(jobs_data, evaluator, 10)
    final_best = population[0]
    try:
        for _ in range(1000):
            population = ltga_run(population, evaluator)
            population = mut.mutate(population)
            population = population[0:7] + makeInitialPopulation(jobs_data, evaluator, 3)
            best = min(population, key=lambda x: x.fitness)
            results.append(best.fitness)
            if best.fitness < final_best.fitness:
                final_best = best
            print(len(population), best)
    except KeyboardInterrupt:
        pass
    return results, final_best

# if __name__ == "__main__":
#     jobs_data = load_data("data2x20.pkl")
#     order = f2_cmax_johnson_solver(jobs_data)
#     schedule = order_to_schedule([order, order])
#     print(schedule)
#
#     for _ in range(10):
#         print(one_run(jobs_data))
