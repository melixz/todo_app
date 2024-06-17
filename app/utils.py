from typing import List, Optional
from .models import Task


def find_task(tasks: List[Task], task_id: int) -> Optional[Task]:
    for task in tasks:
        if task.id == task_id:
            return task
    return None
