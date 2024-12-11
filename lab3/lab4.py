import sys
from PySide6 import QtWidgets, QtCore

from lab3.lab2 import SystemInfoWidget

from lab3.lab3_ import WeatherWidget


class AllWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Объединенное окно")
        self.setGeometry(100, 100, 800, 600)

        self.weather_widget = WeatherWidget()
        self.system_info_widget = SystemInfoWidget()

        main_widget = QtWidgets.QWidget(self)
        layout = QtWidgets.QHBoxLayout(main_widget)

        layout.addWidget(self.weather_widget)
        layout.addWidget(self.system_info_widget)

        self.setCentralWidget(main_widget)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = AllWindow()
    main_window.show()
    sys.exit(app.exec())
