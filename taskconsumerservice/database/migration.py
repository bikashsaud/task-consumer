import mysql.connector

from taskconsumerservice.utils.logger import BaseLogger

logger = BaseLogger("migrations")
import mysql.connector



def check_table_exist(connection_pool, table_name):
    """Checks if a table exists in the database."""
    query = "SHOW TABLES LIKE %s"

    try:
        with connection_pool.cursor() as cursor:
            cursor.execute(query, (table_name,))
            return cursor.fetchone() is not None
    except Exception as e:
        logger.exception(f"Error checking table existence: {e}")
        return False


def create_new_table(db_connection):
    """Creates the 'tasks' table if it does not exist."""
    if check_table_exist(db_connection, 'tasks'):
        return True

    create_table_query = """
        CREATE TABLE tasks (
            id BIGINT AUTO_INCREMENT PRIMARY KEY,
            data JSON NOT NULL,
            status ENUM('pending', 'processing', 'completed', 'failed') DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );
    """

    try:
        with db_connection.cursor() as cursor:
            cursor.execute(create_table_query)
        logger.info("Table 'tasks' created successfully.")
        return True
    except mysql.connector.Error as err:
        logger.exception(f"Error creating table: {err}")
        return False
