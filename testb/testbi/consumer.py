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
number_of_questions = 0
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
       
        
        marking_scheme = []
        confirm_marks = []

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
                print('done')
                #print(quiz)

                # print(answer)
                # print(questions)
                # print(all_look)
                global chat_response
                chat_response = str("")
 

        if msg != '' and 'https://www.youtube.com/' not in msg:
            
            if len(ask) == 0:
               
                chat_response = "Please watch or re-watch the tutorial to the end to take a test."
            else:
                with open("resco/score.txt","r",encoding="utf8") as f:#
                        n_data = f.readlines()
                        f.close()
                with open("resco/marks.txt","r",encoding="utf8") as f:#
                        m_data = f.readlines()
                        f.close()
                with open("resco/scorecheck.txt","r",encoding="utf8") as f:#
                        s_data = f.readlines()
                        f.close()

                if len(n_data) <= 10:
                    n_data.append('count')
                    n_data1 = []
                    for words1 in n_data:
                        n_data1.append(words1.strip())                        
                    with open('resco/score.txt','w') as f:
                        f.writelines('\n'.join(n_data1))
                        f.close()
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
                        s_data.append('B')
                        s_data1 = []
                        for words2 in s_data:
                            s_data1.append(words2.strip())
                                                
                        with open('resco/scorecheck.txt','w') as f:
                            f.writelines('\n'.join(s_data1))
                            f.close()

                    else:
                        option_a = answer_choice
                        option_b = other_choice
                        s_data.append('A')
                        s_data1 = []
                        for words2 in s_data:
                            s_data1.append(words2.strip())
                                                
                        with open('resco/scorecheck.txt','w') as f:
                            f.writelines('\n'.join(s_data1))
                            f.close()
                    resp = "<b>Fill in the blanks. Reply with A or B accoriding to the answer selected</b> <br/>" + str((quiz )+ '<font color="green"> ' + '<br/>'  + 'A: ' + str(option_a) +'<br/>' + "B:" + str(option_b)) + '</font>'

                    chat_response = resp 
                    if str(msg).lower() == 'a':
                        m_data.append(msg)
                        m_data1 = []
                        for words3 in m_data:
                            m_data1.append(words3.strip())
                                                
                        with open('resco/marks.txt','w') as f:
                            f.writelines('\n'.join(m_data1))
                            f.close()
                        
                    elif str(msg).lower() == 'b':
                        
                        m_data.append(msg)
                        m_data1 = []
                        for words4 in m_data:
                            m_data1.append(words4.strip())
                                                
                        with open('resco/marks.txt','w') as f:
                            f.writelines('\n'.join(m_data1))
                            f.close()
                    else:
                        m_data.append(msg)
                        m_data6 = []
                        for words6 in m_data:
                            m_data6.append(words6.strip())
                                                
                        with open('resco/marks.txt','w') as f:
                            f.writelines('\n'.join(m_data6))
                            f.close()

                    

                else:
                    total_marks= 10
                    marks = 0
                    for ans_ch in s_data:
                        num = s_data.index(ans_ch)
                        if num <= 9:
                            key2 = s_data.index(ans_ch)
                            ans_of_q = m_data[key2]
                            if ans_ch == ans_of_q:
                                 marks +=1
                            else:
                                marks = marks
                    print(marks)
                    marks_p = float((marks/total_marks)*100)
                    if marks_p >= 0 and marks_p <=20 :
                        mes = 'Please Watch the video again 🙂'
                    elif marks_p >=31 and marks_p < 50 :
                        mes = 'Nice work 👍'
                    elif marks_p >=50 and marks_p < 60 :
                        mes = 'Good work 👏'
                    elif marks_p >=60 and marks_p < 70 :
                        mes = 'Great 👏👏'
                    elif marks_p >=70 and marks_p < 90 :
                        mes = 'That was amazing 👏👏👏'
                    else:
                        mes = 'Excellent 🙌🙌'
                    you_got = str(marks_p) + '%' + mes
                    chat_response = "Your score: " + you_got 
                    n_data2 = []
                    m_data2 = []
                    s_data2 = []
                    ask = []
                    with open('resco/score.txt','w') as f:
                        f.writelines('\n'.join(n_data2))
                        f.close()
                    with open('resco/scorecheck.txt','w') as f:
                        f.writelines('\n'.join(s_data2))
                        f.close()
                    with open('resco/marks.txt','w') as f:
                        f.writelines('\n'.join(m_data2))
                        f.close()



                
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