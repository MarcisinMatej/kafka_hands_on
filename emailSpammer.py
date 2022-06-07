"""
Simple analytics for processed orders.
"""
import logging

from kafka import KafkaConsumer
from KafkaConfig import *
logging.basicConfig()
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)

def main():
    consumer = KafkaConsumer(ORDER_CONFIRMED_TOPIC,
                             bootstrap_servers=KAFKA_BROKER,
                             auto_offset_reset='earliest',
                             group_id='order_spammer')

    logger.info(f"Start listening")
    for message in consumer:
        confirmed_order = KAFKA_DESERIALIZER(message.value)

        logger.info(f"Sending email to {confirmed_order['user_id']}")


if __name__ == '__main__':
    main()