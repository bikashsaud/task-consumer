from taskconsumerservice.utils.logger import BaseLogger


class BaseFacade:

    def __init__(self):
        self.logger = BaseLogger(__name__)
