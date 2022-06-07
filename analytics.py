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

    sales_stats = {}
    consumer = KafkaConsumer(ORDER_CONFIRMED_TOPIC,
                             bootstrap_servers=KAFKA_BROKER,
                             auto_offset_reset='earliest',
                             group_id='order_analytics')


    print(f"Start listening")
    for message in consumer:
        print("Got message")
        confirmed_order = KAFKA_DESERIALIZER(message.value)
        assigned_sales_dept = confirmed_order['assigned_sales_dpt']
        print(f"Assigned dept is {assigned_sales_dept}")
        dept_stats = sales_stats.get(assigned_sales_dept, [])
        dept_stats.append(confirmed_order['order_id'])
        sales_stats[assigned_sales_dept]=dept_stats
        for key in sales_stats.keys():
            print(f"Dept {key} has {len(sales_stats[key])} orders")


if __name__ == '__main__':
    main()