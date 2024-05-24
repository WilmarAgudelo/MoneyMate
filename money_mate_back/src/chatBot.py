import random
import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler
import requests

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
        self.selected_flow = 0  # 0: None, 1: Financial Advice, 2: Financial Analysis
        self.model = joblib.load('./util/modelito1.pkl')
        self.scaler = joblib.load('./util/scaler.pkl')
        self.alpha_vantage_api_key = 'EOG3FOU4HP3QDV8W'
        self.financial_advice_list = [
            "Crea y mantén un presupuesto mensual detallado. Anota todos tus ingresos y gastos, categorízalos y evalúa áreas donde puedes reducir gastos. Utiliza aplicaciones de presupuesto para ayudarte a seguir tus finanzas y asegúrate de revisarlo regularmente para ajustarlo según sea necesario.",
            "Establece un fondo de emergencia que cubra entre tres y seis meses de tus gastos esenciales. Esto te proporcionará una red de seguridad en caso de pérdida de empleo, emergencias médicas o cualquier otra situación inesperada. Asegúrate de mantener este fondo en una cuenta de fácil acceso.",
            "Elimina tus deudas de alto interés lo antes posible. Prioriza el pago de deudas como tarjetas de crédito y préstamos personales con altos intereses. Considera usar métodos como la bola de nieve de deuda (pagar las deudas más pequeñas primero) o la avalancha de deuda (pagar las deudas con los intereses más altos primero).",
            "Invierte a largo plazo y diversifica tu cartera. No pongas todos tus ahorros en un solo tipo de inversión. Distribuye tus inversiones entre acciones, bonos, bienes raíces y otros activos para reducir riesgos y aumentar tus oportunidades de rendimiento a largo plazo.",
            "Automatiza tus ahorros e inversiones para asegurarte de que contribuyes regularmente. Configura transferencias automáticas desde tu cuenta corriente a tus cuentas de ahorro e inversión cada mes. Esto te ayudará a ahorrar e invertir de manera constante sin tener que pensarlo cada vez.",
            "Evita los gastos innecesarios y vive dentro de tus posibilidades. Antes de hacer una compra, pregúntate si realmente la necesitas o si puedes prescindir de ella. Adopta un estilo de vida frugal que te permita ahorrar más dinero y evitar deudas innecesarias.",
            "Revisa y ajusta tus metas financieras periódicamente. A medida que tu vida cambia, también lo harán tus objetivos financieros. Asegúrate de revisar tus metas cada seis meses o cada año y ajústalas según tus necesidades y circunstancias actuales.",
            "Aprovecha los planes de jubilación y las contribuciones equivalentes de tu empleador. Si tu empleador ofrece un plan de jubilación con contribuciones equivalentes, maximiza esta ventaja contribuyendo al menos el porcentaje necesario para obtener el máximo aporte del empleador.",
            "Infórmate sobre impuestos y busca formas legales de minimizarlos. Conoce las deducciones y créditos fiscales disponibles para ti y aprovecha al máximo los beneficios fiscales. Considera hablar con un asesor fiscal para asegurarte de que estás optimizando tu situación tributaria.",
            "Consulta con un asesor financiero profesional para obtener orientación personalizada. Un asesor financiero puede ayudarte a desarrollar un plan financiero integral, recomendarte inversiones adecuadas y ofrecerte asesoramiento sobre cómo alcanzar tus metas financieras a largo plazo."
        ]

    def process_message_text(self, message):
        if isinstance(message, list):
            message = ' '.join(message)  # Concatena la lista en una cadena si es necesario

        message = message.lower().split()
        self.highest_prob.clear()  # Clear the dictionary for each new message

        def response(bot_response, list_of_words, single_response=False, required_words=[]):
            self.highest_prob[bot_response] = self.message_probability(message, list_of_words, single_response, required_words)

        if message[0].lower() == 'hola' or message[0].lower() == 'gracias':
            self.step = 0
            self.selected_flow = 0

        if self.selected_flow == 0:
            response('¿Qué deseas realizar hoy? <br><br> 1. Recibir consejos financieros <br> 2. Realizar análisis financiero', ['hola', 'saludos', 'buenas', 'ey'], single_response=True)
            if '1' in message:
                self.selected_flow = 1
                self.step = 1
                self.highest_prob.clear()  # Clear for the next set of responses
                return self.financial_advice_flow()
            elif '2' in message:
                self.selected_flow = 2
                self.step = 0
                self.highest_prob.clear()  # Clear for the next set of responses
                return self.financial_analysis_flow(message, response)
        elif self.selected_flow == 1:
            return self.financial_advice_flow(response)
        elif self.selected_flow == 2:
            return self.financial_analysis_flow(message, response)

        if self.highest_prob:
            best_match = max(self.highest_prob, key=self.highest_prob.get)
            if self.highest_prob[best_match] > 0:
                return best_match

        return self.unknown()

    def financial_advice_flow(self):
        advice = random.choice(self.financial_advice_list)
        self.step = 0
        self.selected_flow = 0  # Reset selected flow to show the menu again
        self.highest_prob.clear()  # Clear for the next set of responses
        return f"{advice} <br><br> ¿Qué deseas realizar hoy? <br><br> 1. Recibir consejos financieros <br> 2. Realizar análisis financiero"
            

    def financial_analysis_flow(self, message, response):
        print(response)
        if self.step == 0:
            self.step = 1
            return f'¡Hola! ¿Cuál es tu nombre?'
        elif self.step == 1:
            self.step = 2
            self.nombre = ' '.join(message).capitalize()
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
            else:
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
            else:
                self.gastos_hormiga = int(message[0])
                self.step = 0
                self.selected_flow = 0
                prediction_response = self.run_prediction()
                return f"{prediction_response} <br><br> ¿Qué deseas realizar hoy? <br><br> 1. Recibir consejos financieros <br> 2. Realizar análisis financiero"
    
    def message_probability(self, user_message, recognized_words, single_response=False, required_words=[]):
        if len(recognized_words) == 0:
            return 1  # Si no hay palabras reconocidas, siempre devuelve 1 (100% de probabilidad)

        if not user_message:
            return 0
        
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

    def get_financial_advice(self):
        # Aquí haces una solicitud a la API de Alpha Vantage para obtener el consejo financiero
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=MSFT&interval=5min&apikey={self.alpha_vantage_api_key}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                # Aquí parseas la respuesta de la API y extraes el consejo financiero
                advice = "Tu consejo financiero personalizado aquí."
                return advice
            else:
                return "Lo siento, no pude obtener un consejo financiero en este momento. Inténtalo de nuevo más tarde."
        except Exception as e:
            print("Error al obtener el consejo financiero:", e)
            return "Lo siento, ha ocurrido un error al obtener el consejo financiero. Inténtalo de nuevo más tarde."

# Código de prueba
if __name__ == '__main__':
    chatbot = ChatBot()
