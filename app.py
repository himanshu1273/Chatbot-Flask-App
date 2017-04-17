from flask import Flask, render_template
from flask.ext.socketio import SocketIO
from flask_socketio import emit
from chatterbot import ChatBot
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config['SECRET KEY'] = 'gjr39dkjn344_!67#'
socketio = SocketIO(app)

chatbot = ChatBot('ChatRoom',
                  logic_adapters=[
                      'chatterbot.adapters.logic.EvaluateMathematically',
                      'chatterbot.adapters.logic.TimeLogicAdapter',
                      'chatterbot.adapters.logic.ClosestMatchAdapter'
                  ])
chatbot.train('chatterbot.corpus.english')
chatbot.train('chatterbot.corpus.english.greetings')
chatbot.train('chatterbot.corpus.english.conversations')


@app.route('/')
def chat():
	return render_template('index.html')

@socketio.on('message', namespace = '/machinelearning')
def receive_message(message):
    bot_response = chatbot.get_response(message['data'])
    emit('response', {'data': bot_response})

if __name__ == '__main__':
	socketio.run(app)