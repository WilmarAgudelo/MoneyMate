from flask import Flask, Response, request, jsonify
from flask_cors import CORS
import re

class RestApi:
    def __init__(self, chatbot):
        self.app = Flask(__name__)
        self.chatbot = chatbot
        CORS(self.app)
        self.initialize_routes()

    def initialize_routes(self):
        self.app.route('/get-response', methods=['POST'])(self.get_response)

   
    def get_response(self):
        user_message = request.get_json()['message'].lower()      
        split_message = re.split(r'(\d+)\s*|[,:;.?!-_]\s*', user_message)
        response = self.chatbot.process_message_text(split_message)
        return jsonify({'response': response})




    def run(self):
        self.app.run(debug=True) 

