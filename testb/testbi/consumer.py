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
    'yes',
    'What was the lesson about.',
    'List five things you learnt from the video',
    'What was the title of the lesson',
    'Where can you aquire the knowledge acquired in this tutorial.',
    'Please elaborate, your concern',
    'How are you feeling today by the way',
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