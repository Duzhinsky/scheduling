from schedule import order_to_schedule

class FitnessFunction(object):
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
