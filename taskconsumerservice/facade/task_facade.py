from taskconsumerservice.entities.task_entity import TaskBaseEntity
from taskconsumerservice.facade.base_facade import BaseFacade
from taskconsumerservice.mapper.task_mapper import map_task_entity_to_proto
from taskconsumerservice.taskpb.task.task_pb2 import FetchTaskRequest, FetchTaskResponse, FetchTaskBaseResponse


class TaskFacade(BaseFacade):

    def __init__(self, task_repo):
        super().__init__()
        self.__task_repo = task_repo

    def tasks(self, request: FetchTaskRequest, debug) -> FetchTaskResponse:
        ...
