import redis
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Connect to Redis and subscribe to the channel
r = redis.Redis(host='redis', port=6379)
p = r.pubsub()
p.subscribe('my-channel')

# Connect to the database and create a session
engine = create_engine('sqlite:///messages.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Define the model for messages
class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.now)

# Create the table if it doesn't exist
Base.metadata.create_all(engine)

# Wait for messages and save them to the database
for message in p.listen():
    # Extract the message content
    content = message.get('data')

    # Create a new message object
    new_message = Message(content=content)

    # Add the new message to the session and commit the transaction
    session.add(new_message)
    session.commit()