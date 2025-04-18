from fluvio import Fluvio

# Connect to the Fluvio cluster
fluvio = Fluvio.connect()

# Create a consumer for the 'screen-data' topic
consumer = fluvio.topic_consumer("screen-data")

# Consume messages from the topic
for message in consumer.stream():
    print(f"Received: {message.value_string()}")