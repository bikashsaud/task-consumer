from datetime import datetime
from enum import Enum
from typing import List, Dict

from pydantic import BaseModel


class Status(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskEntity(BaseModel):
    id: int = None
    data: Dict = ""
    status: Status = Status.PENDING
    created_at: datetime = None
    updated_at: datetime = None


class TaskBaseEntity(BaseModel):
    count: int = None
    error: bool = False
    success: bool = False
    error_message: str = None
    tasks: List[TaskEntity] = None

