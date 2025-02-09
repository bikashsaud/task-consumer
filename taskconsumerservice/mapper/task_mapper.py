from typing import List

from taskconsumerservice.entities.task_entity import TaskEntity
from taskconsumerservice.taskpb.task.task_pb2 import FetchTaskResponse, Status
from taskconsumerservice.utils.helper import convert_datetime_to_unix_ms
from taskconsumerservice.utils.logger import BaseLogger

logger = BaseLogger(__name__)


def get_status_enum(status) -> Status.ValueType:
    if status=="failed":
        return Status.FAILED
    elif status=="processing":
        return Status.PROCESSING
    elif status=="completed":
        return Status.COMPLETED
    else:
        return Status.PENDING



def map_task_entity_to_proto(tasks_entity: List[TaskEntity], debug_id):
    try:
        logger.info(f"Mapping {tasks_entity} tasks: {debug_id}")
        tasks_proto_list = []
        for task in tasks_entity:
            logger.info(f"one Mapping {task.created_at} task")
            status_enum = get_status_enum(task.status)
            task_proto = FetchTaskResponse(
                id=task.id,
                status=status_enum,
                created_at=convert_datetime_to_unix_ms(task.created_at),
                updated_at=convert_datetime_to_unix_ms(task.updated_at),
            )
            tasks_proto_list.append(task_proto)
        return tasks_proto_list
    except Exception as e:
        logger.exception(f"Exception to map data: {e}")
        return []
