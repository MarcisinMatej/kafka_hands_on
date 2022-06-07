import json

KAFKA_BROKER = 'localhost:9092'
ORDER_TOPIC = "order_details"
ORDER_CONFIRMED_TOPIC = "order_confirmed"

__MESSAGE_ENCODING='utf-8'

def KAFKA_SERIALIZER(data: dict)->bytes:
    """
    Function to serialize dictionary to kafka message
    :param data:
    :return:
    """
    return json.dumps(data).encode(__MESSAGE_ENCODING)


def KAFKA_DESERIALIZER(data: bytes)->dict:
    """
    Function to de-serialize dictionary to kafka message
    :param data:
    :return:
    """
    return json.loads(data.decode(__MESSAGE_ENCODING))