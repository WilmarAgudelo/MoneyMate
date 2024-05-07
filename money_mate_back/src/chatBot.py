import random
from logica import Logica


class ChatBot:
    def __init__(self):
        self.highest_prob = {}
        self.salario = 0
        self.gastos = 0
        self.result = 0

    def process_message_text(self, message):
 
        def response(bot_response, list_of_words, single_response=False, required_words=[]):
            self.highest_prob[bot_response] = self.message_probability(message, list_of_words, single_response, required_words)

        response('Hola! Buen día, ¿cuál es tu nombre?', ['hola', 'saludos', 'buenas', 'estas'], single_response=True)
        response('salario', ['wilmar', 'juan','paola','necid'], single_response=True)
        response('gastos', ['1300000','2600000','3900000','5200000','6500000','7800000','9100000',
                                                               '10400000','11700000','13000000','14300000','15600000','16900000'], single_response=True)
        response('Realiar analaisis: 1.Si 2.No', ['800000','1600000','500000','2000000','4500000','6000000','9000000','600000','1900000','15000000'], single_response=True)
        response('machineLearning', ['1', '2'], single_response=True)


        best_match = max(self.highest_prob, key=self.highest_prob.get)

        if best_match == 'salario':
            self.salario = message
            return '¿Cuento es tu salario mensual?'    
        elif best_match == 'gastos':
            self.gastos = message
            return '¿Cuanto es el monto de tus gastos al mes?'
        elif best_match == 'machineLearning':
            
            return 'finalizado'

        print(self.unknown()if self.highest_prob[best_match] < 1 else best_match  )
        return self.unknown() if self.highest_prob[best_match] < 1 else best_match    

    
   
    def message_probability(self, user_message, recognized_words, single_response=False, required_word=[]):
        message_certainty = 0
        has_required_words = True
        for word in user_message:
            if word in recognized_words:
                message_certainty +=1
        print(message_certainty)
       # print(recognized_words)
        percentage = float(message_certainty) / float(len(recognized_words))

        for word in required_word:
            if word not in user_message:
                has_required_words = False
                break
        if has_required_words or single_response:
            return int(percentage * 100)
        else:
            return 0

 
    def unknown(self):
        response = ['puedes decirlo de nuevo?', 'No estoy seguro de lo que quieres'][random.randrange(2)]
        return response
