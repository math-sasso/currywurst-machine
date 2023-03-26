from database import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime


# Define the model for messages
class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.now)


# # Define the model for messages
# class TransactionHistory(Base):
#     __tablename__ = 'transaction_history'
#     id = Column(Integer, primary_key=True)
#     # machine_id = Column(Integer)
#     # status:Column(String)
#     # returned_coins:Column(String)
#     # error_msg: Column(String)
#     created_at = Column(DateTime, default=datetime.now)

# new_row = models.TransactionHistory(
#                 machine_id = content_json["machine_id"],
#                 status = content_json["status"],
#                 returned_coins = json.dumps(content_json["returned_coins"]),
#                 error_msg = content_json["error_msg"],

#             )
