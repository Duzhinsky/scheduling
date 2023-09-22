from dataclasses import dataclass
from typing import List

MachineId = int
JobId = int
ActionDuration = int


@dataclass
class Job:
    job_id: JobId
    actions: List[ActionDuration]

    def __int__(self, job_id, actions):
        self.job_id = job_id
        self.actions = actions
        self.preemption = False
        self.setup_time = 0