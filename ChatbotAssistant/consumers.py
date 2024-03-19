from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio
from .LLMLogic import generate_response
from channels.generic.websocket import WebsocketConsumer

class ModelConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        prompt = text_data_json['prompt']

        for response_chunk in generate_response(prompt):
            self.send(text_data=json.dumps({'response': response_chunk}))