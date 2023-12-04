class Individual(object):
    def __init__(self, genes=[], fitness=-1000):
        self.genes = genes
        self.fitness = fitness

    def __cmp__(self, other):
        if self.fitness > other.fitness:
            return 1
        elif self.fitness < other.fitness:
            return -1
        else:
            return 0

    def __str__(self):
        return "(%s) = %s" % (",".join(map(str, self.genes)),
                              str(self.fitness))