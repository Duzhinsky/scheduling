import pickle
from random import randrange

from job import Job


def generate_data(jobs, machines, filename="data.pkl"):
    dataset = []
    for i in range(jobs):
        dataset.append(Job(i, [randrange(1, 5) for j in range(machines)]))
    with open("data/" + filename, 'wb') as outp:
        pickle.dump(dataset, outp, pickle.HIGHEST_PROTOCOL)


def load_data(filename):
    with open("data/" + filename, 'rb') as inp:
        dataset = pickle.load(inp)
    return dataset

if __name__ == "__main__":
    generate_data(20, 2, "data2x20.pkl")