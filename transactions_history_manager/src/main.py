import database
import models
import redis
import json


def run_subscriber_loop(subscriber, session):
    while True:
        message = subscriber.get_message()
        if message and message["type"] == "message":
            content = message.get("data")

            new_row = models.Message(content=content)
            # Add the new message to the session and commit the transaction
            session.add(new_row)
            session.commit()


if __name__ == "__main__":
    # Create the table if it doesn't exist
    models.Base.metadata.create_all(bind=database.engine)
    database.session.commit()
    # Create subscriber
    client = redis.Redis(host="redis", port=6379)
    subscriber = client.pubsub()
    subscriber.subscribe(
        "purchases-channel"
    )  # {'type': 'subscribe', 'pattern': None, 'channel': b'purchases-channel', 'data': 1}

    # Run watching loop
    run_subscriber_loop(subscriber, database.session)
