import copy
import random
from collections import deque
from functools import cmp_to_key
from random import randrange, shuffle
from typing import List, Deque
import pickle

import ltga.Distance
from data import load_data
from job import Job
from ltga import LTGA
from ltga.Crossover import globalCrossover, twoParentCrossover
from ltga.FitnessFunction import ScheduleFitness
from ltga.Individual import Individual
from ltga.Mutation import Mutation
from schedule import order_to_schedule


def f2_cmax_johnson_solver(jobs: List[Job]) -> List[Job]:
    """
    Solver for the "F2 || C_max" task introduced in the following article:

    S.M. Johnson. Optimal two-and-three-stage production schedules with set-up times included.
    Naval Research Logistic Quaterly, 1:61–68, 1954

    link: https://www.rand.org/content/dam/rand/pubs/papers/2008/P402.pdf

    :param jobs: list of jobs to optimize schedule
    :returns: jobs ordered to minimize the makespan. As for F2 an order is equal for both stages, list is 1xN
    """
    # Validate input
    for job in jobs:
        if len(job.actions) != 2:
            raise ValueError("Johnson solver is able to solve F2||C_max only. "
                             f"There is a job with {len(job.actions)} actions, so it couldn't be executed as F2 job")

    # Sort by minimal stage time
    def jobs_comparator(lhs: Job, rhs: Job) -> int:
        return min(lhs.actions) - min(rhs.actions)

    sorted_jobs = sorted(jobs, key=cmp_to_key(jobs_comparator))
    first_stage_jobs: Deque[Job] = deque()
    second_stage_jobs: Deque[Job] = deque()

    for job in sorted_jobs:
        if job.actions[0] < job.actions[1]:
            first_stage_jobs.append(job)
        else:
            second_stage_jobs.appendleft(job)

    return list(first_stage_jobs + second_stage_jobs)


def makeInitialPopulation(jobs: List[Job], evaluator, pop_size) -> List[Individual]:
    M = len(jobs[0].actions)
    N = len(jobs)
    individuals = [Individual([i for i in range(N) for _ in range(M)]) for _ in range(pop_size)]
    for individual in individuals:
        shuffle(individual.genes)
        individual.fitness = evaluator.evaluate(individual.genes)
    # print(*individuals)
    return individuals


def ltga_run(population, evaluator):
    config = {
        "maximumEvaluations": 100000,
        "maximumFitness": 100000
    }
    result = {"evaluations": 0}
    new_pop = copy.deepcopy(population)
    optimizer = LTGA().generate(population, evaluator, ltga.Distance.pairwiseDistance, globalCrossover, config)
    try:
        individual = next(optimizer)  # Get the first individual
        while (result['evaluations'] < config["maximumEvaluations"]):
            fitness = evaluator.evaluate(individual.genes)
            result['evaluations'] += 1
            individual = optimizer.send(fitness)
    except StopIteration:
        pass
    return population


def one_run(jobs_data):
    results = []
    evaluator = ScheduleFitness(jobs_data)
    mut = Mutation(evaluator)
    population = makeInitialPopulation(jobs_data, evaluator, 20)
    for _ in range(40):
        population = ltga_run(population, evaluator)
        population = mut.mutate(population)
        best = min(population, key=lambda x: x.fitness)
        results.append(best.fitness)
    return sorted(results, reverse=True)


# if __name__ == "__main__":
#     jobs_data = load_data("data2x20.pkl")
#     order = f2_cmax_johnson_solver(jobs_data)
#     schedule = order_to_schedule([order, order])
#     print(schedule)
#
#     for _ in range(10):
#         print(one_run(jobs_data))
