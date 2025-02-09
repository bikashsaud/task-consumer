
class TaskError(Exception):
    def __init__(self, *args, **kwargs):
        pass

class TaskRuntimeError(RuntimeError):
    def __init__(self, *args, **kwargs):
        pass


class TaskNotImplementedError(TaskRuntimeError):
    def __init__(self, *args, **kwargs):
        pass

