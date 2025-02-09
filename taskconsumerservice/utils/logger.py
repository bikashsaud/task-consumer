import logging
import logging.config


class BaseLogger:
    _logger = None
    _initialized = False

    def __init__(self, name="root"):
        BaseLogger.build()
        BaseLogger._logger = logging.getLogger(name=name)

    @staticmethod
    def build():
        if not BaseLogger._initialized:
            logging.basicConfig(
                level=logging.DEBUG,
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                handlers=[
                    logging.StreamHandler(),  # Logs to console
                    logging.FileHandler("task_logger.log")
                ]
            )
            BaseLogger._initialized = True

    @property
    def get_logger(self):
        return BaseLogger._logger

    @staticmethod
    def _get_debug_msg(debug):
        return "debug: {}".format(debug).rstrip("\n")

    @classmethod
    def info(cls, msg, *args, **kwargs):
        cls._logger.info(msg, *args, **kwargs)

    @classmethod
    def debug(cls, msg, *args, **kwargs):
        cls._logger.debug(msg, *args, **kwargs)

    @classmethod
    def warning(cls, msg, *args, **kwargs):
        cls._logger.warning(msg, *args, **kwargs)

    @classmethod
    def error(cls, msg, *args, **kwargs):
        cls._logger.error(msg, *args, **kwargs)

    @classmethod
    def exception(cls, msg, *args, exc_info=True, **kwargs):
        cls._logger.exception(msg, *args, exc_info=exc_info, **kwargs)

