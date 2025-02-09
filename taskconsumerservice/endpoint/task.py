from abc import ABC

import grpc

from taskconsumerservice.facade.task_facade import TaskFacade
from taskconsumerservice.taskpb.task.task_pb2 import FetchTaskBaseRequest, FetchTaskBaseResponse
from taskconsumerservice.taskpb.task.task_rpc_pb2_grpc import TaskRpcServicer
from taskconsumerservice.utils.logger import BaseLogger


class TaskServicerImpl(TaskRpcServicer, ABC):

    def __init__(self, task_facade):
        super(TaskServicerImpl, self).__init__()
        self.logger =  BaseLogger(__name__)
        self.__task_facade: TaskFacade = task_facade

    def fetchTask(self, request: FetchTaskBaseRequest, context: grpc.ServicerContext) -> (
            FetchTaskBaseResponse):
        ...
