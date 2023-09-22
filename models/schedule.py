from dataclasses import dataclass, field
from typing import Mapping, Tuple, List
from models.job import MachineId, ActionDuration, JobId


@dataclass(init=True)
class Schedule:
    table: Mapping[MachineId, List[Tuple[int, JobId, ActionDuration]]] = field(default_factory=dict)
    makespan: int = field(default_factory=int)

    def __str__(self):
        string = ""
        string += "#" * self.makespan + "\n"
        for machine, tasks in self.table.items():
            machine_line = list(" " * self.makespan)
            for task in tasks:
                for i in range(task[0], task[0] + task[2]):
                    machine_line[i] = str(task[1])
            string += "".join(machine_line) + "\n"
        string += "#" * self.makespan + "\n"
        string += "Makespan: " + str(self.makespan) + "\n"

        return string