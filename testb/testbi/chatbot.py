from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

# Creating ChatBot Instance
chatbot = ChatBot('CoronaBot')

elena = ChatBot('elena')

# bot trainer
trainer = ListTrainer(elena)
questions = [
    "Hello",
    "Hi there!",
    "How are you doing?",
    "I'm doing great.",
    "That is good to hear",
    "Thank you.",
    "You're welcome."
]

trainer.train(questions)
print('Hi, my name is Elena. hope you had a good lesson.\n')
print('Here are some questions to test your understanding are you ready?\n')


while True:
    request=input('you :')
    if request == 'OK' or request == 'ok':
        print('Elena: bye')
        break
    else:
        print('Fill in the blanks')
        response=elena.get_response(request)
        print('Elena:', response)