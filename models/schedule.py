from dataclasses import dataclass, field
from typing import MutableMapping, Tuple, List
from models.job import MachineId, ActionDuration, JobId, Job


@dataclass(init=True)
class Schedule:
    table: MutableMapping[MachineId, List[Tuple[int, JobId, ActionDuration]]] = field(default_factory=dict)
    makespan: int = field(default_factory=int)

    def __str__(self):
        string = ""
        string += "#" * self.makespan + "\n"
        for machine, tasks in self.table.items():
            machine_line = list(" " * 3 * self.makespan)
            for task in tasks:
                for i in range(task[0], task[0] + task[2]):
                    machine_line[i] = f"\x1b[{self.__job_id_to_color__(task[1])}m" + " " + "\x1b[0m"
                if task[2] >= len(str(task[1])):
                    start = int(task[0] + task[2] / 2 - len(str(task[1])) / 2)
                    for i in range(len(str(task[1]))):
                        machine_line[start + i] = f"\x1b[{self.__job_id_to_color__(task[1])}m" + str(task[1])[
                            i] + "\x1b[0m"
            string += "".join(machine_line).rstrip() + "\n"
        string += "#" * self.makespan + "\n"
        string += "Makespan: " + str(self.makespan) + "\n"

        return string

    def __job_id_to_color__(self, job_id: int):
        fgs = (2, 4, 10, 12, 35, 36, 37, 38, 39)
        return "0;" + "97" + ";" + str(100 + job_id % 7)


def order_to_schedule(orders: List[List[Job]]) -> Schedule:
    """
    :returns: Schedule for the order
    :rtype: Schedule
    :param orders: List of orders. i-th order is for i-th machine
    """
    result = Schedule()
    stage_finish_map: MutableMapping[JobId, int] = {}
    makespan = 0
    for (machineId, orderForMachine) in enumerate(orders):
        last_job_finishes = 0
        for job in orderForMachine:
            previous_stage_finished = 0
            if job.job_id in stage_finish_map:
                previous_stage_finished = stage_finish_map[job.job_id]
            start_time = max(last_job_finishes, previous_stage_finished)
            if machineId not in result.table:
                result.table[machineId] = []
            result.table[machineId].append((start_time, job.job_id, job.actions[machineId]))
            last_job_finishes = start_time + job.actions[machineId]
            stage_finish_map[job.job_id] = last_job_finishes
        makespan = max(makespan, last_job_finishes)
    result.makespan = makespan

    return result
