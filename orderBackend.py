"""
Dummy generator for orders
"""
import random

from KafkaConfig import *
import logging
import time

from kafka import KafkaProducer


ORDER_LIMIT = 15
ITEMS = ["burger", "chicken", "sandwich", "cola", "french-fries", "kids-menu", "special"]

def main():
    logging.basicConfig()
    logger = logging.getLogger("order_backend")
    logger.setLevel(logging.INFO)
    logger.info("Going to generate orders after 5 sec")
    logger.info(f"Each 5 sec we genereate new order. In total we will generate {ORDER_LIMIT} orders")

    producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER, security_protocol="PLAINTEXT")

    for i in range(ORDER_LIMIT):
        order_data = {
            "order_id":i,
            "user_id": f"User_{i}",
            "total_cost": random.randint(1, 100),
            # -1 because randint included the last element of the range
            "items": random.sample(ITEMS,random.randint(0, len(ITEMS)-1))
        }
        logger.info(f"Sending message {i}")
        producer.send(topic=ORDER_TOPIC,value=KAFKA_SERIALIZER(order_data))

        time.sleep(5)

if __name__ == '__main__':
    main()
