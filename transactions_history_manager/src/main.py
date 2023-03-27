import database
import models
import redis
from sqlalchemy.orm.session import Session
import os

def run_subscriber_loop(subscriber:redis.client.PubSub, session:Session)-> None:
    """
    Runs a subscriber loop that listens for messages from a Redis PubSub channel and adds them to the database as new message rows.

    Args:
    subscriber (redis.client.PubSub): A Redis PubSub subscriber object.
    session (Session): A SQLAlchemy Session object for the database.

    Returns:
    None
    """
    while True:
        message = subscriber.get_message()
        if message and message["type"] == "message":
            content = message.get("data")

            new_row = models.Transactions(content=content)
            # Add the new message to the session and commit the transaction
            session.add(new_row)
            session.commit()


if __name__ == "__main__":
    # Create the table if it doesn't exist
    models.Base.metadata.create_all(bind=database.engine)
    database.session.commit()
    # Create subscriber
    client = redis.Redis(host=os.getenv("REDIS_SERVICE", "redis"), port=6379)
    subscriber = client.pubsub()
    subscriber.subscribe(
        os.getenv("MESSAGE_QUEUE","transaction_logs")
    )  # {'type': 'subscribe', 'pattern': None, 'channel': b'purchases-channel', 'data': 1}

    # Run watching loop
    run_subscriber_loop(subscriber, database.session)
