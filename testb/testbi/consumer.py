import json
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ListTrainer
#bot name
elena = ChatBot('elena')

# bot trainer
questions=[
    'Hi',
    'Hello',
    'I need roadmap for Competitive Programming',
    'Just create an account on GFG and start',
    'I have a query.',
    'Please elaborate, your concern',
    'How long it will take to become expert in Coding ?',
    'It usually depends on the amount of practice.',
    'Ok Thanks',
    'No Problem! Have a Good Day!'
]
trainer = ListTrainer(elena)



trainer.train(questions)
class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print('connected', event)

        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        print('receive', event)
        received_data = json.loads(event['text'])
        msg = received_data.get('message')
        if msg != '':
            chat_response = elena.get_response(msg)
            chat_response = str(chat_response)
        if not msg:
            print('Error:: empty message')
            return False
        response = {
            'message':chat_response ,

        }

        await self.send({
            'type': 'websocket.send',
            'text': json.dumps(response)
        })

    async def websocket_disconnect(self, event):
        print('disconnected', event)