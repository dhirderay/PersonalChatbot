from django.shortcuts import render
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio
from .LLMLogic import generate_response

class ModelConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        prompt = text_data_json['prompt']

        for response_chunk in generate_response(prompt):
            await self.send(text_data=json.dumps({'response': response_chunk}))

        await self.send(text_data=json.dumps({'response': 'END'}))

def index(request):
    return render(request, 'index/PersonalChatbot.html')