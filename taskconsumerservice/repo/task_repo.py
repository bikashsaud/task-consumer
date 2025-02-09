import sys
import time

from taskconsumerservice.entities.task_entity import TaskEntity, TaskBaseEntity
from taskconsumerservice.repo.base_repo import BaseRepo
from taskconsumerservice.utils.settings import MAX_PROCESSING_RETRY


class TaskRepo(BaseRepo):

    def __init__(self, connection):
        super().__init__()
        self.__connection_pool = connection

    def tasks(self, debug_id) -> TaskBaseEntity:
        try:
            self.logger.info("Task Repo.")
        except Exception as e:
            self.logger.exception(f"Repo Exception: {e}")
            task_base_data = TaskBaseEntity(
                error=True,
                error_message="Unable to get task data"
            )
            return task_base_data

    def task_handler(self, key, value):
        try:

            task_id = value['id']
            self.logger.info(f"Task Repo: {task_id}.")
            self.process_task(value)
            self.complete_task(task_id)
            return True
        except Exception as e:
            self.logger.exception(f"Repo Exception: {e}")
            return False

    def complete_task(self, task_id, retries=0):
        try:
            self.logger.info(f"Completing task: {task_id}.")
            query = """
                    UPDATE tasks SET status = %s, retry_count=%s WHERE id = %s
                    """
            params = ['completed', retries, task_id]
            with self.__connection_pool.cursor() as cursor:
                self.logger.debug(f"Executing query: {query}, params: {params}")
                cursor.execute(query, params)
                self.__connection_pool.commit()
            return True
        except Exception as e:
            self.logger.exception(f"Exception to complete task: {e}")
            self.handle_failed_task(task_id)
            return False

    def process_task(self, task):
        try:
            self.logger.info(f"Task: {task['id']} Processing.")
        except Exception as e:
            self.logger.exception(f"Repo Exception: {e}")
            self.handle_failed_task(task['id'])

    def handle_failed_task(self, task_id):
        try:
            self.logger.info(f"Handle failed: {task_id}.")
            query = """
                    UPDATE tasks SET status = %s WHERE id = %s
                    """
            params = ['failed', task_id]
            self.logger.debug(f"Failed task query: {query}, params: {params}")
            with self.__connection_pool.cursor() as cursor:
                cursor.execute(query, params)
                self.__connection_pool.commit()
            return True
        except Exception as e:
            self.logger.exception(f"Repo Exception: {e}")
            sys.exit()

    def get_task_retry_count(self, task_id):
        """
        Note: Not implemented.
        """
        max_processing_retry = int(MAX_PROCESSING_RETRY)
        try:
            query = """
            SELECT retry_count FROM tasks WHERE id = %s
            """
            with self.__connection_pool.cursor() as cursor:
                cursor.execute(query, (task_id,))
                result = cursor.fetchone()
                if result is None:
                    return max_processing_retry
                else:
                    return result[0]
        except Exception as e:
            self.logger.exception(f"Repo Exception: {e}")
            return max_processing_retry