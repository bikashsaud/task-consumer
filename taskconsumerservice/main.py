import os
import sys
import threading
from concurrent import futures

import grpc

from taskconsumerservice.database.configuration import MySQLConnection
from taskconsumerservice.database.migration import create_new_table
from taskconsumerservice.endpoint.task import TaskServicerImpl
from taskconsumerservice.events.kafka_task_consumer import TaskConsumer
from taskconsumerservice.facade.task_facade import TaskFacade
from taskconsumerservice.repo.task_repo import TaskRepo
from taskconsumerservice.taskpb.task.task_rpc_pb2_grpc import add_TaskRpcServicer_to_server
from taskconsumerservice.utils.logger import BaseLogger
from taskconsumerservice.utils.settings import SERVICE_PORT

sys.path.append(os.path.abspath('./'))


class TaskConsumerServiceRunner(threading.Thread):
    """
    Task service runner class
    """
    def __init__(self, port):
        threading.Thread.__init__(self)
        super().__init__()
        self.server = None
        self.port = port
        self.db_connection = MySQLConnection()
        self.logger = BaseLogger(__name__)

    def configure(self):
        thread_pool = futures.ThreadPoolExecutor(max_workers=10)
        self.server = grpc.server(thread_pool=thread_pool)
        self.db_connection.start()
        connection = self.db_connection.get_connection()
        create_new_table(connection)

        task_repo = TaskRepo(connection)
        task_facade = TaskFacade(task_repo)
        task_rpc_servicer = TaskServicerImpl(task_facade=task_facade)
        task_consumer = TaskConsumer(task_repo)
        try:
            task_consumer.start()
        except KeyboardInterrupt:
            pass

        add_TaskRpcServicer_to_server(servicer=task_rpc_servicer,
                                      server=self.server)
        self.server.add_insecure_port("[::]:" + str(self.port))
        self.logger.info("Task Service port: %s", self.port)

    def run(self):
        """Starts the gRPC server."""
        self.configure()
        self.server.start()
        self.logger.info("Task Service started successfully.")

    def wait_for_termination(self):
        """Blocks execution until the server is terminated."""
        try:
            self.server.wait_for_termination()
        except KeyboardInterrupt:
            self.logger.info("Server interrupted, shutting down...")
            self.clean()

    def clean(self):
        """Gracefully shuts down the server and database connection."""
        if self.server:
            self.server.stop(0)
            self.logger.info("gRPC server stopped.")

        if self.db_connection:
            self.db_connection.stop()
            self.logger.info("Database connection closed.")


if __name__ == '__main__':
    logger = BaseLogger("root")
    runner = TaskConsumerServiceRunner(SERVICE_PORT)
    try:
        runner.run()
        runner.wait_for_termination()
        logger.debug("Server exited!")
    except KeyboardInterrupt:
        logger.info("Received KeyboardInterrupt, exiting...")
        sys.exit(0)
