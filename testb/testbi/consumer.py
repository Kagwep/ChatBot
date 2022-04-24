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

ask = []
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
        check_if = []

        if path_y not in check_if:
        
            if 'https://www.youtube.com/' in path_y:
                check_if.append(path_y)
                video_id = (str(path_y).replace('https://www.youtube.com/watch?v=', ''))
                srt = YouTubeTranscriptApi.get_transcript(video_id)
                par=''
                for element in srt:
                    sent = element.get("text")
                    par = par +' '+ str(sent)
                scriptName = par
                scriptName=p.punctuate(scriptName)
                #print(par)
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
                all_look = []
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
                    listToStr = ' '.join(map(str, ans))
                    if listToStr != '':
                        all_look.append(listToStr)       
                    i = i + 1
                #queries
                i = 1
                for query in queries:
                    query = (query)
                    if '__________' in query:
                        questions.append(query)
                    #print(answers)
                    #print ('\n')

                    i = i + 1
                global rep
                rep = all_look
                global ask
                ask= questions
                quiz = random.choice(questions)
                key = questions.index(quiz)
                answer = all_look[key]
                #print(quiz)

                # print(answer)
                # print(questions)
                # print(all_look)
                chat_response = str("")
 

        if msg != '' and 'https://www.youtube.com/' not in msg:
            if len(ask) == 0:
                chat_response = "Please wath the tutorial to the end."
            else:
                quiz = random.choice(ask)
                key_find = ask.index(quiz)
                answer_choice = rep[key_find]
                other_choice = random.choice(rep)
                to_chooce = [answer_choice,other_choice]
                get_A = random.choice(to_chooce)
                s_key = to_chooce.index(get_A)

                if s_key == 0:
                    option_a = other_choice
                    option_b = answer_choice
                else:
                    option_a = answer_choice
                    option_b = other_choice
                resp = "<b>Fill in the blacks. Reply with A or B accoriding to the answer selected</b> <br/>" + str((quiz )+ '<font color="green"> ' + '<br/>'  + 'A: ' + str(option_a) +'<br/>' + "B:" + str(option_b)) + '</font>'
                print(resp)
                chat_response = resp 

                
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