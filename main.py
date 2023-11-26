from random import randrange, shuffle
from typing import List

import ltga.Distance
from job import Job
from ltga import LTGA
from ltga.Crossover import globalCrossover, twoParentCrossover
from ltga.FitnessFunction import ScheduleFitness
from ltga.Individual import Individual

def makeInitialPopulation(jobs: List[Job], evaluator) -> List[Individual]:
    M = len(jobs[0].actions)
    N = len(jobs)
    individuals = [Individual([i for i in range(N) for _ in range(M)]) for _ in range(5)]
    for individual in individuals:
        shuffle(individual.genes)
        individual.fitness = evaluator.evaluate(individual.genes)
    return individuals

def oneRun(jobs):
    config = {
        "maximumEvaluations": 100000,
        "maximumFitness": 100000
    }
    evaluator = ScheduleFitness(jobs)
    population = makeInitialPopulation(jobs, evaluator)
    # print(*population)
    result = {"evaluations": 0}

    bestFitness = max(population, key=lambda x: x.fitness)
    optimizer = LTGA().generate(population, evaluator, ltga.Distance.pairwiseDistance, globalCrossover, config)
    try:
        individual = next(optimizer)  # Get the first individual
        while (result['evaluations'] < config["maximumEvaluations"]):
            fitness = evaluator.evaluate(individual.genes)
            result['evaluations'] += 1
            if bestFitness.fitness < fitness:
                bestFitness = individual
            # Send the fitness into the optimizer and get the next individual
            individual = optimizer.send(fitness)
            print(individual)
    except StopIteration:  # If the optimizer ever stops, just end the run
        pass

    result['bestFitness'] = bestFitness
    return result


if __name__ == "__main__":
    randomJobs = [
        Job(i + 1, [
            randrange(1, 5),
            randrange(1, 5),
            randrange(1, 5)
        ]) for i in range(4)
    ]
    print(oneRun(randomJobs), sep="\n")
