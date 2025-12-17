import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt


# class WeatherApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.initUI()

#     def initUI(self):
#         self.setWindowTitle('Weather App')

#         self.layout = QVBoxLayout()

#         self.city_input = QLineEdit(self)
#         self.city_input.setPlaceholderText('Enter city name')
#         self.layout.addWidget(self.city_input)

#         self.get_weather_button = QPushButton('Get Weather', self)
#         self.get_weather_button.clicked.connect(self.fetch_weather)
#         self.layout.addWidget(self.get_weather_button)

#         self.result_label = QLabel('', self)
#         self.result_label.setAlignment(Qt.AlignCenter)
#         self.layout.addWidget(self.result_label)

#         self.setLayout(self.layout)
#         self.resize(300, 200)

#     def fetch_weather(self):
#         city = self.city_input.text()
#         api_key = 'your_api_key_here'  # Replace with your OpenWeatherMap API key
#         url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'

#         try:
#             response = requests.get(url)
#             data = response.json()

#             if data['cod'] == 200:
#                 temp = data['main']['temp']
#                 description = data['weather'][0]['description']
#                 self.result_label.setText(
#                     f'Temperature: {temp}°C\nDescription: {description}')
#             else:
#                 self.result_label.setText('City not found. Please try again.')
#         except Exception as e:
#             self.result_label.setText('Error fetching data. Please try again.')

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter City Name:", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.descryption_label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.descryption_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.descryption_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.descryption_label.setObjectName("descryption_label")

        self.setStyleSheet("""
            QLabel, QPushButton {
                Font-family:calibri;
            }
            QLabel#city_label {
                font-size:40px;
                font-style: italic;
                
            }
            QLineEdit#city_input {
                font-size:40px;
            }
            QPushButton#get_weather_button {
                font-size:30px;
                font-weight: bold;
            color: blue;
            }
            QLabel#temperature_label {
                font-size:5px;
            }
            QLabel#emoji_label {
                font-size:100px;
                font-family:Segoe UI emoji;
            }
            QLabel#descryption_label {
                font-size:50px;
            }
        """)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = "aa001bcb466041ac2424d37d17446c76"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error(
                        "Bad Request. \nPlease check the city name.")
                case 401:
                    self.display_error(
                        "Unauthorized/Invalid API key.\n Please check your API key.")

                case 403:
                    self.display_error(
                        "Forbidden! API key has been disabled. \nPlease contact support.")
                case 404:
                    self.display_error("City not found. \nPlease try again.")
                case 500:
                    self.display_error(
                        "Internal Server error.\n Please try again later.")
                case 502:
                    self.display_error(
                        "Bad gateway.\nInvalid response from the server.\n Please try again later.")
                case 503:
                    self.display_error(
                        "Service unavailable.\nServer is down.\n Please try again later.")
                case 504:
                    self.display_error(
                        "Gateway timeout.\nNo response from the server Please try again later.")
                case _:
                    self.display_error(
                        "HTTP error occurred.\n{http_error} \nPlease try again.")

        except requests.exceptions.ConnectionError:
            print("Network error. \nPlease check your internet connection.")
        except requests.exceptions.Timeout:
            print("The request timed out. \nPlease try again later.")
        except requests.exceptions.TooManyRedirects:
            print("Too many redirects. \nPlease check the URL.")
        except requests.exceptions.RequestException as req_error:
            print(f"An error occurred: {req_error} \nPlease try again.")

    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.descryption_label.clear()

    def display_weather(self, data):
        print(data)
        self.temperature_label.setStyleSheet("font-size: 75px;")
        temp_kelvin = data["main"]["temp"]
        temp_fahrenheit = (temp_kelvin - 273.15) * 9/5 + 32
        temp_celsius = temp_kelvin - 273.15
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]

        self.temperature_label.setText(f"{temp_celsius:.2f}°C")
        self.temperature_label.setText(f"{temp_fahrenheit:.2f}°F")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.descryption_label.setText(weather_description)

    @staticmethod
    def get_weather_emoji(weather_id):
        match weather_id:
            case _ if 200 <= weather_id < 300:
                return "⛈️"  # Thunderstorm
            case _ if 300 <= weather_id < 400:
                return "🌦️"  # Drizzle
            case _ if 500 <= weather_id < 600:
                return "🌧️"  # Rain
            case _ if 600 <= weather_id < 700:
                return "❄️"  # Snow
            case _ if 700 <= weather_id < 800:
                return "🌫️"  # Atmosphere
            case 800:
                return "☀️"  # Clear
            case _ if 801 <= weather_id < 900:
                return "☁️"  # Clouds
            case _:
                return "🌈"  # Default/Unknown


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
