import redis
import json

client = redis.Redis(host='redis', port=6379)
subscriber = client.pubsub()
subscriber.subscribe('purchases-channel') # {'type': 'subscribe', 'pattern': None, 'channel': b'purchases-channel', 'data': 1}

while True:
    message = subscriber.get_message() 
    if message:
        with open("logs.txt","a") as f:
            f.write(str(message))

            

# with open('messages.json', 'a') as f:

#     for message in p.listen():
#         print(message)
#         if message['type'] == 'message':
#             json_message = message['data'].decode('utf-8')

#             # Load the JSON message as a Python dictionary
#             message_dict = json.loads(json_message)

#             # Append the dictionary to the JSON file
#             json.dump(message_dict, f)
#             f.write('\n')
