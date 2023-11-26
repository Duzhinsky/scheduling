from dataclasses import dataclass
from typing import List

MachineId = int
JobId = int
ActionDuration = int


@dataclass
class Job:
    job_id: JobId
    actions: List[ActionDuration]
