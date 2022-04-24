import json
import ast
from .models import Video
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from youtube_transcript_api import YouTubeTranscriptApi
import nltk
import random
from punctuator import Punctuator
p = Punctuator('trainer\INTERSPEECH-T-BRNN.pcl')
""" from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ListTrainer """
""" import wave, math, contextlib
import speech_recognition as sr
from moviepy.editor import AudioFileClip
import os """
#bot name
#elena = ChatBot('elena')

# bot trainer
""" questions=[
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
trainer = ListTrainer(elena) """

ask = []
# trainer.train(questions)
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
        path_y=msg
       # filePath = received_data.get('vid_file')
       # print(filePath)

        
        if 'https://www.youtube.com/' in path_y:
            video_id = (str(path_y).replace('https://www.youtube.com/watch?v=', ''))
            srt = YouTubeTranscriptApi.get_transcript(video_id)
            par=''
            for element in srt:
                sent = element.get("text")
                par = par +' '+ str(sent)
            scriptName = par
            scriptName=p.punctuate(scriptName)
            print(par)
            tolist = scriptName.split(".")# split an occurence of "."
            vid_script = []
            for el in tolist:
                vid_script.append(el)
            #script opened
            def readFile(scriptName):
                paragraph = scriptName
                return paragraph
            #tokenizaton of the script
            def tokenization(paragraph):
                sents = nltk.sent_tokenize(paragraph)
                words = [nltk.word_tokenize(sent) for sent in sents]
                return sents, words
            # parts of speech  tagging, helps in creating the questions.
            def posTagging(words):
                posWords = [nltk.pos_tag(word) for word in words]
                return posWords

            # get script
            paragraph = readFile(scriptName)

            # tokenize
            sents, words = tokenization(paragraph)

            # pos tagging
            posWords = posTagging(words)

            # question generated bank to help train the bot
            questions = []

            i = 0
            #list to store the all the answers to questions
            answers = []

            queries = sents
            que=[]

            # Replace Nouns with '____'
            for posWord in posWords:
                ans = []
                for x in posWord:
                    
                    if (x[1] == 'NN'):
                
                        queries[i] = queries[i].replace(x[0], '__________')
                        que.append(queries[i])
                        ans.append(x[0])
                        answers.append(x[0])
                        
                i = i + 1
            #queries
            i = 1
            for query in queries:
                query = (query)
                questions.append(query)
                #print(answers)
                #print ('\n')

                i = i + 1
            global ask
            ask= que
            quiz = random.choice(que)
            key = que.index(quiz)
            answer = answers[key]
            print(quiz)
            print(answer)
            chat_response = str("")
        #     transcribed_audio_file_name = "transcribed_speech.wav"
        #     zoom_video_file_name = 'media\video\22\python.mp4'
        #     audioclip = AudioFileClip(zoom_video_file_name)
        #     audioclip.write_audiofile(transcribed_audio_file_name)
        #     with contextlib.closing(wave.open(transcribed_audio_file_name,'r')) as f:
        #         frames = f.getnframes()
        #         rate = f.getframerate()
        #         duration = frames / float(rate)
        #     total_duration = math.ceil(duration / 60)
        #     r = sr.Recognizer()
        #     for i in range(0, total_duration):
        #         with sr.AudioFile(transcribed_audio_file_name) as source:
        #             audio = r.record(source, offset=i*60, duration=60)
        #         f = open("transcription.txt", "a")
        #         f.write(r.recognize_google(audio))
        #         f.write(" ")
        #     f.close() 

        if msg != '' and 'https://www.youtube.com/' not in msg:
            #chat_response = elena.get_response(msg)

            quiz = random.choice(ask)
            chat_response = str(quiz)
        if not msg:
            print('Error:: empty message')
            return False
        response = {
            'message':chat_response,

        }

        await self.send({
            'type': 'websocket.send',
            'text': json.dumps(response)
        })

    async def websocket_disconnect(self, event):
        print('disconnected', event)