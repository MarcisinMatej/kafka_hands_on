import logging
import random

from KafkaConfig import *

from kafka import KafkaProducer, KafkaConsumer
logging.basicConfig()
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)

SALES_DPT_CODES = [123, 456, 332, 452]

def validate_order(order_data:dict) -> bool:
    """
    Simple validation of order if the items field is not empty
    :param order_data: dictionary of order
    :return: bool
    """
    items = order_data.get("items", [])
    return len(items) > 0


def main():
    consumer = KafkaConsumer(ORDER_TOPIC,
                             bootstrap_servers=KAFKA_BROKER,
                             auto_offset_reset='earliest',
                             group_id='transaction_processor')

    producer = KafkaProducer(bootstrap_servers = KAFKA_BROKER)

    print(f"Start listening")
    for message in consumer:
        order_data = KAFKA_DESERIALIZER(message.value)
        logging.info(f"Recieved order {order_data}")
        if validate_order(order_data):
            logging.info("Order validated. Processing")
            order_data['assigned_sales_dpt'] = random.choice(SALES_DPT_CODES)
            producer.send(topic=ORDER_CONFIRMED_TOPIC, value=KAFKA_SERIALIZER(order_data))
        else:
            logging.error("Order INVALID. Order is Rejected.")
            # TODO we could do some dead-letter topic here





if __name__ == '__main__':
    main()