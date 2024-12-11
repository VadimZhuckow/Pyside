import sys
from PySide6 import QtWidgets, QtCore
from lab3.lab1 import SystemInfo


class SystemInfoWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Информация о системе")
        self.setGeometry(100, 100, 300, 200)

        self.delay = QtWidgets.QLineEdit(self)
        self.delay.setPlaceholderText("Введите время задержки")

        self.cpu = QtWidgets.QLabel("Загрузка CPU: 0%", self)
        self.ram = QtWidgets.QLabel("Загрузка RAM: 0%", self)

        self.start_btn = QtWidgets.QPushButton("Запустить поток", self)
        self.start_btn.clicked.connect(self.start_system_info_thread)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.delay)
        layout.addWidget(self.cpu)
        layout.addWidget(self.ram)
        layout.addWidget(self.start_btn)

        self.system_info_thread = SystemInfo()
        self.system_info_thread.systemInfoReceived.connect(self.update_system_info)

        self.delay.textChanged.connect(self.update_delay)

    def start_system_info_thread(self):
        self.system_info_thread.start()

    def update_system_info(self, system_info):
        # print(system_info)
        cpu_value, ram_value = system_info
        self.cpu.setText(f"Загрузка CPU: {cpu_value}%")
        self.ram.setText(f"Загрузка RAM: {ram_value}%")

    def update_delay(self):
            delay = float(self.delay.text())
            self.system_info_thread.delay = delay


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = SystemInfoWidget()
    widget.show()
    sys.exit(app.exec())
