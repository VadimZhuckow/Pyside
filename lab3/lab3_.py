"""
Реализовать
Создавать форму можно как в ручную, так и с помощью программы Designer

Форма должна содержать:
1. поле для ввода широты и долготы (после запуска потока они должны блокироваться)
2. поле для ввода времени задержки  виджет, который будет работать с потоком WeatherHandler из модуля a_threads
(после запуска потока оно должно блокироваться)
3. поле для вывода информации о погоде в указанных координатах
4. поток необходимо запускать и останавливать при нажатии на кнопку
"""

import sys
from PySide6 import QtWidgets, QtCore
from lab3.lab1 import WeatherHandler


class WeatherWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Погодный виджет")
        self.setGeometry(100, 100, 400, 300)

        self.lat_input = QtWidgets.QLineEdit(self)
        self.lat_input.setPlaceholderText("Введите широту")

        self.lon_input = QtWidgets.QLineEdit(self)
        self.lon_input.setPlaceholderText("Введите долготу")

        self.delay_input = QtWidgets.QLineEdit(self)
        self.delay_input.setPlaceholderText("Введите время задержки")

        self.weather_output = QtWidgets.QTextEdit(self)
        self.weather_output.setReadOnly(True)

        self.start_stop_button = QtWidgets.QPushButton("Запустить поток", self)
        self.start_stop_button.clicked.connect(self.toggle_weather_thread)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.lat_input)
        layout.addWidget(self.lon_input)
        layout.addWidget(self.delay_input)
        layout.addWidget(self.weather_output)
        layout.addWidget(self.start_stop_button)

        self.weather_thread = None
        self.is_running = False

    def toggle_weather_thread(self):
        if not self.is_running:
            self.start_weather_thread()
        else:
            self.stop_weather_thread()

    def start_weather_thread(self):
        try:
            lat = float(self.lat_input.text())
            lon = float(self.lon_input.text())
            delay = float(self.delay_input.text())

            self.lat_input.setDisabled(True)
            self.lon_input.setDisabled(True)
            self.delay_input.setDisabled(True)

            self.weather_thread = WeatherHandler(lat, lon)
            self.weather_thread.weatherDataReceived.connect(self.update_weather_info)
            self.weather_thread.errorOccurred.connect(self.show_error)
            self.weather_thread.setDelay(delay)
            self.weather_thread.start()

            self.start_stop_button.setText("Остановить поток")
            self.is_running = True

        except ValueError:
            self.show_error("Ошибка: Неверные координаты или задержка")

    def stop_weather_thread(self):
        if self.weather_thread:
            self.weather_thread.__status = False
            self.weather_thread.quit()
            self.weather_thread.wait()

        self.lat_input.setDisabled(False)
        self.lon_input.setDisabled(False)
        self.delay_input.setDisabled(False)

        self.start_stop_button.setText("Запустить поток")
        self.is_running = False

    def update_weather_info(self, data):
        current_weather = data.get("current_weather", {})
        temperature = current_weather.get("temperature", "N/A")
        wind_speed = current_weather.get("windspeed", "N/A")
        self.weather_output.setText(f"Температура: {temperature}C\nСкорость ветра: {wind_speed} м/с")

    def show_error(self, message):
        self.weather_output.setText(message)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = WeatherWidget()
    widget.show()
    sys.exit(app.exec())
