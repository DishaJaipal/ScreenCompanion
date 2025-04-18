from fluvio import Fluvio

def send_to_fluvio(message):
    producer = Fluvio().topic_producer("screen-data")
    producer.send_string(message)
