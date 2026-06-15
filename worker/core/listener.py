from tasks import task_director


class WorkerListener:
    def __init__(self, ):
        ...

    def job_director(self, task_name: str) -> callable:
        return task_director.get(task_name, False)
