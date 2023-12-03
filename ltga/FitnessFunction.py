'''
This module provides an interface for how fitness functions should interact
with solvers, as well as the definitions for a few benchmark problems
'''
from schedule import order_to_schedule


class FitnessFunction(object):
    '''
    An interface for a fitness function provided to ensure all required
    functions of a fitness function object are implemented
    '''
    def evaluate(self, genes):
        raise NotImplementedError()


class ScheduleFitness(FitnessFunction):

    def __init__(self, jobs):
        self.jobs = jobs

    def genesToOrder(self, genes):
        M = len(self.jobs[0].actions)
        result = [[] for i in range(M)]
        nextMachine = {}
        for i in range(len(self.jobs)):
            nextMachine[i] = 0
        for jobId in genes:
            job = self.jobs[jobId]
            result[nextMachine[jobId]].append(job)
            nextMachine[jobId] += 1
        return result

    def genesToSchedule(self, genes):
        order = self.genesToOrder(genes)
        return order_to_schedule(order)

    def evaluate(self, genes):
        return self.genesToSchedule(genes).makespan
