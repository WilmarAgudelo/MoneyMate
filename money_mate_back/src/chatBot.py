import random
import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler

class ChatBot:
    def __init__(self):
        self.highest_prob = {}
        self.nombre = ""
        self.salario = 0
        self.ingreso_fijo = 0
        self.gastos_mensuales = 0
        self.imprevistos_mes = 0
        self.gastos_hormiga = 0
        self.step = 0
        self.model = joblib.load('./util/modelito1.pkl')
        self.scaler = joblib.load('./util/scaler.pkl')

    def process_message_text(self, message):
        if isinstance(message, list):
            message = ' '.join(message)  # Concatena la lista en una cadena si es necesario

        message = message.lower().split()
        self.highest_prob.clear()  # Clear the dictionary for each new message

        def response(bot_response, list_of_words, single_response=False, required_words=[]):
            print(len(list_of_words))
            self.highest_prob[bot_response] = self.message_probability(message, list_of_words, single_response, required_words)

        if message[0] == 'Hola': 
            self.step = 0
        # Pregunta inicial
        if self.step == 0:
            response('Hola, ¿cómo te llamas?', ['hola', 'saludos', 'buenas', 'ey'], single_response=True)
        elif self.step == 1:
            response(f'{self.nombre}, ¿cuál es tu salario mensual?', [], single_response=True)
        elif self.step == 2:
            response(f'{self.nombre}, ¿Es este salario un monto fijo? 1: Si, 0: No', [], single_response=True)
        elif self.step == 3:
            response(f'{self.nombre}, ¿Cuánto suman tus gastos mensuales?', ['1', '0'], single_response=True)
        elif self.step == 4:
            response(f'{self.nombre}, ¿cuánto estimas en imprevistos al mes?', [], single_response=True)
        elif self.step == 5:
            response(f'{self.nombre}, ¿cómo categorizas tus gastos hormiga? 1: Pocos, 2: Moderados, 3: Bastante, 4: Exagerado ?', [], single_response=True)
        elif self.step == 6:
            response(f'Análisis finalizado, {self.nombre}. Predicción: ', ['1', '2', '3', '4'], single_response=True)
        
        best_match = max(self.highest_prob, key=self.highest_prob.get)

        if self.highest_prob[best_match] < 1:
            return self.unknown()

        if self.step == 0:
            self.step = 1
            return 'Hola, ¿cómo te llamas?'
        elif self.step == 1:
            self.nombre = ' '.join(message).capitalize()
            self.step = 2
            return f'{self.nombre}, ¿cuál es tu salario mensual?'
        elif self.step == 2:
            try:
                self.salario = int(message[0])
                self.step = 3
                return f'{self.nombre}, ¿Es este salario un monto fijo? <br><br> Elige una de las siguientes opciones: <br> 1. Si <br> 0. No'
            except ValueError:
                return f'{self.nombre}, por favor ingresa un número válido para el salario.'
        elif self.step == 3:
            if message[0] not in ['1', '0']:
                return f'{self.nombre}, por favor responde con 1 (Sí) o 0 (No) para la pregunta anterior.'
            self.ingreso_fijo = int(message[0])
            self.step = 4
            return f'{self.nombre}, ¿Cuánto suman tus gastos mensuales?'
        elif self.step == 4:
            try:
                self.gastos_mensuales = int(message[0])
                self.step = 5
                return f'{self.nombre}, ¿cuánto estimas en imprevistos al mes?'
            except ValueError:
                return f'{self.nombre}, por favor ingresa un número válido para los gastos mensuales.'
        elif self.step == 5:
            try:
                self.imprevistos_mes = int(message[0])
                self.step = 6
                return f'{self.nombre}, ¿cómo clasificarías tus gastos hormiga? <br><br> Elige una de las siguientes opciones: <br> 1. Poco <br> 2. Moderado <br> 3. Normal <br> 4. En exceso'
            except ValueError:
                return f'{self.nombre}, por favor ingresa un número válido para los imprevistos.'
        elif self.step == 6:
            if message[0] not in ['1', '2', '3', '4']:
                return f'{self.nombre}, por favor responde con 1, 2, 3, o 4 para los gastos hormiga.'
            self.gastos_hormiga = int(message[0])
            return self.run_prediction()

        return best_match

    def message_probability(self, user_message, recognized_words, single_response=False, required_words=[]):
        if len(recognized_words) == 0:
            return 1  # Si no hay palabras reconocidas, siempre devuelve 1 (100% de probabilidad)

        message_certainty = 0
        has_required_words = True

        for word in user_message:
            if word in recognized_words:
                message_certainty += 1

        percentage = float(message_certainty) / float(len(recognized_words)) if recognized_words else 0

        for word in required_words:
            if word not in user_message:
                has_required_words = False
                break

        if has_required_words or single_response:
            return int(percentage * 100)
        else:
            return 0

    def unknown(self):
        responses = ['¿Puedes decirlo de nuevo?', 'No estoy seguro de lo que quieres.']
        return random.choice(responses)

    def run_prediction(self):
        if not self.model:
            return "No se pudo cargar el modelo para realizar la predicción."

        input_data = [
            self.salario,
            self.gastos_mensuales,
            self.imprevistos_mes,
        ]

        try:
            self.step = 0
            input_data_scaled = self.scaler.transform([input_data])
            prediction = self.model.predict(input_data_scaled)[0]
            message = 'Probablemente no habrá endeudamiento' if prediction == 0 else 'Probablemente si habrá endeudamiento'
            return f'Análisis finalizado, {self.nombre}. Predicción: {message}'
        except Exception as e:
            return f'Error al realizar la predicción: {e}'

# Código de prueba
if __name__ == '__main__':
    chatbot = ChatBot()
