import mysql.connector.pooling

from taskconsumerservice.utils.logger import BaseLogger
from taskconsumerservice.utils.settings import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME


from abc import ABC, abstractmethod


class JDBCException(Exception):
    def __init__(self, *args, **kwargs):
        super(JDBCException, self).__init__(args, kwargs)


class ConnectionPool:
    def __init__(self, pool):
        self._pool = pool
        self.logger = BaseLogger(__name__)

    def get_connection(self):
        try:
            if self._pool is not None:
                return self._pool.get_connection()
            print("Connection pool created successfully!!")
        except Exception:
            self.logger.exception("Connection pool is not initialized")
            raise JDBCException("Connection pool is not initialized")

    @staticmethod
    def create():
        p = mysql.connector.pooling.MySQLConnectionPool(
            pool_name='taskconsumerservice',
            pool_size=4,
            pool_reset_session=True,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        )
        return ConnectionPool(pool=p)


class DatabaseConnection(ABC):
    def __init__(self):
        self.connection = None
        self.logger = BaseLogger(__name__)

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def get_connection(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def check_connection(self):
        pass


class MySQLConnection(DatabaseConnection, ABC):
    def __init__(self):
        super().__init__()
        self._SQL_CONN_TEST_QUERY = "SELECT 1"
        self._db_name = DB_NAME
        self._connection_pool = None
        self.logger = BaseLogger(__name__)

    def start(self):
        self.logger.info("MySQL connection started.")
        self._connection_pool = ConnectionPool.create()
        return self._connection_pool.get_connection()

    def get_connection(self):
        return self._connection_pool.get_connection()

    def stop(self):
        self._connection_pool.close()

    def check_connection(self):
        if self._connection_pool is None:
            self.logger.error("Connection pool is not initialized.")
            return False
        try:
            con = self._connection_pool.get_connection()
            cur = con.cursor()
            cur.execute(self._SQL_CONN_TEST_QUERY)
            return cur.rowcount > 0
        except Exception as e:
            self.logger.exception(f"Error while checking the connection: {e}")
            return False
