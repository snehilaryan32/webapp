from google.cloud import pubsub_v1
import json
import os


try:
    # Initialize the Pub/Sub client with details from the environment variables
    publisher = pubsub_v1.PublisherClient()
    project_id = os.getenv("PROJECT_ID")
    topic_id = os.getenv("PUBSUB_TOPIC_ID")
    topic_path = publisher.topic_path(project_id, topic_id)
except Exception as e:
    print(f"An error occurred: {e}")

def publish_message(data):
    data = json.dumps(data).encode("utf-8")
    try:
        publish_future = publisher.publish(topic_path, data)
        publish_future.result()
        print("Published message to topic.")
    except Exception as e:
        print(f"An error occurred: {e}")

def generate_message_dict(user_data):
    return {
        "first_name": user_data['first_name'],
        "last_name": user_data['last_name'],
        "username": user_data['username'],
        "token_id": str(user_data['id'])
    }

