import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # Define the name of the room group that this consumer will join
        self.room_group_name = 'test'

        # Add this consumer to the specified group (synchronously)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        # Accept the WebSocket connection
        self.accept()

    def disconnect(self, close_code):
        # Remove this consumer from the specified group when the WebSocket disconnects
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, 
            self.channel_name
        )

    def receive(self, text_data):
        # Receive the message from the WebSocket client
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Print the received message to the console (useful for debugging)
        print('Message:', message)

        # Send the message to the room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, 
            {
                "type": "chat.message",  # Specify the type of message (used to route the event)
                "message": message       # The actual message content
            }
        )

    def chat_message(self, event):
        # This method is called when a message is received from the room group
        message = event["message"]

        # Send the message to the WebSocket client
        self.send(text_data=json.dumps({
            "type": 'chat',
            "message": message
        }))
