import asyncio
import websockets
import json

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ListTrainer
#bot name
elena = ChatBot('elena')

# bot trainer
trainer = ListTrainer(elena)

questions = [
    'hi',
    'hello',
    'how are you doing',
    'fine'
]

trainer.train(questions)

#Already trained and it's supposed to be persistent
#chatbot.train("chatterbot.corpus.english")

async def chat_receiver(websocket, path):
    async for message in websocket:
        message = json.loads(message)
        text = message['text']

        chat_response = elena.get_response(text).text
        print(chat_response)
        await websocket.send(json.dumps({'response': chat_response}))

async def router(websocket, path):
	if path == "/":
		await chat_receiver(websocket, path)

    #the code below is how you add other path's
    
	# elif path == "/shade-area":
	# 	await get_shaded_area(websocket, path)
	# elif path == '/render':
	# 	await render(websocket, path)

asyncio.get_event_loop().run_until_complete(websockets.serve(router, '0.0.0.0', 8765))

asyncio.get_event_loop().run_forever()