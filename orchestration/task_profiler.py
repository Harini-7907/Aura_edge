from dataclasses import dataclass


@dataclass
class AITask:

    task_id: str

    cpu_requirement: float

    memory_requirement: float

    deadline: float

    priority: int

    estimated_execution_time: float

    task_size: float


def create_task(
    task_id,
    cpu_requirement,
    memory_requirement,
    deadline,
    priority,
    estimated_execution_time,
    task_size
):

    task = AITask(
        task_id=task_id,
        cpu_requirement=cpu_requirement,
        memory_requirement=memory_requirement,
        deadline=deadline,
        priority=priority,
        estimated_execution_time=estimated_execution_time,
        task_size=task_size
    )

    return task


if __name__ == "__main__":

    print("Creating sample AI task...")

    task = create_task(
        task_id="task_001",
        cpu_requirement=40.0,
        memory_requirement=30.0,
        deadline=2.0,
        priority=2,
        estimated_execution_time=1.2,
        task_size=5.0
    )

    print("\n==========================================")
    print("AI TASK PROFILE")
    print("==========================================")

    print("Task ID:", task.task_id)

    print(
        "CPU requirement:",
        task.cpu_requirement,
        "%"
    )

    print(
        "Memory requirement:",
        task.memory_requirement,
        "%"
    )

    print(
        "Deadline:",
        task.deadline,
        "seconds"
    )

    print(
        "Priority:",
        task.priority
    )

    print(
        "Estimated execution time:",
        task.estimated_execution_time,
        "seconds"
    )

    print(
        "Task size:",
        task.task_size,
        "MB"
    )

    print("\n==========================================")
    print("TASK PROFILING COMPLETED")
    print("==========================================")