from restApi import RestApi
from chatBot import ChatBot

if __name__ == '__main__':
    chatbot = ChatBot()
    rest_api = RestApi(chatbot)
    rest_api.run()
