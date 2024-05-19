import random
import pickle

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

        try:
            # Carga el modelo utilizando pickle
            with open('./util/modelito1.pkl', 'rb') as f:
                self.model = pickle.load(f)
            print("Modelo cargado exitosamente:", self.model)
        except Exception as e:
            print(f"Error al cargar el modelo: {e}")

    def process_message_text(self, message):
        if isinstance(message, list):
            message = ' '.join(message)  # Concatena la lista en una cadena si es necesario

        message = message.lower().split()
        self.highest_prob.clear()  # Clear the dictionary for each new message

        def response(bot_response, list_of_words, single_response=False, required_words=[]):
            self.highest_prob[bot_response] = self.message_probability(message, list_of_words, single_response, required_words)

        print(message)
        # Pregunta inicial
        if self.step == 0:
            response('Hola, ¿cómo te llamas?', ['hola', 'saludos', 'buenas', 'ey'], single_response=True)
        elif self.step == 1:
            response(f'{self.nombre}, ¿cuál es tu salario mensual?', [], single_response=True)
        elif self.step == 2:
            response(f'{self.nombre}, ¿cuál es tu ingreso fijo mensual?', [], single_response=True)
        elif self.step == 3:
            response(f'{self.nombre}, ¿cuánto son tus gastos mensuales?', [], single_response=True)
        elif self.step == 4:
            response(f'{self.nombre}, ¿cuánto estimas en imprevistos al mes?', [], single_response=True)
        elif self.step == 5:
            response(f'{self.nombre}, ¿cuánto gastas en gastos hormiga al mes?', [], single_response=True)
        elif self.step == 6:
            response(f'Análisis finalizado, {self.nombre}. Predicción: ', [], single_response=True)
        
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
            except ValueError:
                return f'{self.nombre}, por favor ingresa un número válido para el salario.'
            self.step = 3
            return f'{self.nombre}, ¿cuál es tu ingreso fijo mensual?'
        elif self.step == 3:
            try:
                self.ingreso_fijo = int(message[0])
            except ValueError:
                return f'{self.nombre}, por favor ingresa un número válido para el ingreso fijo.'
            self.step = 4
            return f'{self.nombre}, ¿cuánto son tus gastos mensuales?'
        elif self.step == 4:
            try:
                self.gastos_mensuales = int(message[0])
            except ValueError:
                return f'{self.nombre}, por favor ingresa un número válido para los gastos mensuales.'
            self.step = 5
            return f'{self.nombre}, ¿cuánto estimas en imprevistos al mes?'
        elif self.step == 5:
            try:
                self.imprevistos_mes = int(message[0])
            except ValueError:
                return f'{self.nombre}, por favor ingresa un número válido para los imprevistos.'
            self.step = 6
            return f'{self.nombre}, ¿cuánto gastas en gastos hormiga al mes?'
        elif self.step == 6:
            try:
                self.gastos_hormiga = int(message[0])
            except ValueError:
                return f'{self.nombre}, por favor ingresa un número válido para los gastos hormiga.'
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
            self.ingreso_fijo,
            self.gastos_mensuales,
            self.imprevistos_mes,
            self.gastos_hormiga
        ]
        prediction = self.model.predict([input_data])[0]
        return f'Análisis finalizado, {self.nombre}. Predicción: {prediction}'

# Código de prueba
if __name__ == '__main__':
    chatbot = ChatBot()
