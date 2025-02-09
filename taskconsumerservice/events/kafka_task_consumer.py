import json
import threading

from confluent_kafka import Consumer, KafkaError, KafkaException
from taskconsumerservice.utils.logger import BaseLogger
from taskconsumerservice.utils.settings import KAFKA_BROKER, TASK_CONSUME_GROUP_ID, KAFKA_PENDING_TASK_PROCESSOR_TOPIC


class TaskConsumer(threading.Thread):
    def __init__(self, task_repo):
        """
        Initialize the Kafka consumer with the given broker configuration.
        """
        threading.Thread.__init__(self)
        self.group_id = TASK_CONSUME_GROUP_ID
        self.kafka_broker = KAFKA_BROKER
        self.__conf = {
            'bootstrap.servers': self.kafka_broker,
            'group.id': self.group_id,
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': False,
        }
        self.topics = [KAFKA_PENDING_TASK_PROCESSOR_TOPIC]
        self.consumer = Consumer(self.__conf)
        self.logger = BaseLogger(__name__)
        self._stop_event = threading.Event()
        self.task_repo = task_repo

    def subscribe(self):
        """
        Subscribe to the specified topics.
        """
        try:
            self.consumer.subscribe(self.topics)
            self.logger.info(f"Subscribed to topics: {self.topics}")
        except KafkaException as e:
            self.logger.exception(f"Error subscribing to topics: {e}")

    def stop(self):
        """
        Signal the consumer to stop gracefully.
        """
        self._stop_event.set()

    def stopped(self):
        """
        Check if the consumer is signaled to stop.
        """
        return self._stop_event.is_set()

    def run(self):
        """
        Override the run method to start consuming messages.
        """
        self.logger.info(f"Starting consumer with topics: {self.topics}")
        self.subscribe()
        self.consume()

    def consume(self):
        """
        Consume messages from the subscribed topics.
        """
        try:
            while not self.stopped():
                msg = self.consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        self.logger.info(f"End of partition reached {msg.partition()}")
                    else:
                        self.logger.error(f"Error: {msg.error()}")
                else:
                    self.process_message(msg)
                    self.consumer.commit(asynchronous=False)
        except Exception as e:
            self.logger.exception(f"Error consuming messages: {e}")
        finally:
            self.close()

    def process_message(self, msg):
        """
        Process the consumed message.
        """
        try:
            key = msg.key().decode('utf-8') if msg.key() else None
            value = json.loads(msg.value().decode('utf-8')) if msg.value() else None
            self.logger.info(f"Consumed message: key={key}, value={value}, topic={msg.topic()}, partition={msg.partition()}, offset={msg.offset()}")
            self.task_repo.task_handler(key, value)
        except Exception as e:
            self.logger.exception(f"Error processing message: {e}")

    def close(self):
        """
        Close the consumer connection.
        """
        try:
            self.consumer.close()
            self.logger.info("Consumer closed successfully")
        except Exception as e:
            self.logger.exception(f"Error closing consumer: {e}")


# if __name__ == "__main__":
#     TOPICS = [KAFKA_PENDING_TASK_PROCESSOR_TOPIC]
#     task_consumer = TaskConsumer()
#     task_consumer.start()
