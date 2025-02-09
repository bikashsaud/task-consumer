from taskconsumerservice.utils.logger import BaseLogger


class BaseRepo:
    def __init__(self):
        self.logger = BaseLogger(__name__)

