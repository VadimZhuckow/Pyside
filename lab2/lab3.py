"""
Реализация программу проверки состояния окна:
Форма для приложения (ui/c_signals_events_form.ui)

Программа должна обладать следующим функционалом:

1. Возможность перемещения окна по заданным координатам.
2. Возможность получения параметров экрана (вывод производить в plainTextEdit + добавлять время).
    * Кол-во экранов
    * Текущее основное окно
    * Разрешение экрана
    * На каком экране окно находится
    * Размеры окна
    * Минимальные размеры окна
    * Текущее положение (координаты) окна
    * Координаты центра приложения
    * Отслеживание состояния окна (свернуто/развёрнуто/активно/отображено)
3. Возможность отслеживания состояния окна (вывод производить в консоль + добавлять время).
    * При перемещении окна выводить его старую и новую позицию
    * При изменении размера окна выводить его новый размер
"""
import datetime

from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        loader = QUiLoader()
        file = QFile("ui/c_signals_events_form.ui")
        file.open(QFile.ReadOnly)
        self.ui = loader.load(file, self)
        file.close()
        self.setLayout(self.ui.layout())

        self.setWindowTitle("Состояние окна")
        self.setGeometry(100, 100, 400, 30)

        self.old_pos = self.pos()

        self.ui.pushButtonLT.clicked.connect(lambda: self.move_window(-10, -10))
        self.ui.pushButtonRT.clicked.connect(lambda: self.move_window(10, -10))
        self.ui.pushButtonLB.clicked.connect(lambda: self.move_window(-10, 10))
        self.ui.pushButtonRB.clicked.connect(lambda: self.move_window(10, 10))
        self.ui.pushButtonCenter.clicked.connect(self.center_window)
        self.ui.pushButtonMoveCoords.clicked.connect(self.move_to_coords)
        self.ui.pushButtonGetData.clicked.connect(self.get_window_data)

    def move_window(self, dx, dy):
        new_pos = self.pos() + QtCore.QPoint(dx, dy)
        self.move(new_pos)
        self.log(f"Перемещение окна: старая позиция {self.old_pos}, новая позиция {new_pos}")
        self.old_pos = new_pos

    def center_window(self):
        screen = QtWidgets.QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        center_x = screen_geometry.x() + (screen_geometry.width() - self.width()) // 2
        center_y = screen_geometry.y() + (screen_geometry.height() - self.height()) // 2
        self.move(center_x, center_y)
        self.log(f"Окно перемещено в центр: {self.pos()}")

    def move_to_coords(self):
        x = self.ui.spinBoxX.value()
        y = self.ui.spinBoxY.value()
        self.move(x, y)
        self.log(f"Окно перемещено в координаты: ({x}, {y})")

    def get_window_data(self):
        screen = QtWidgets.QApplication.primaryScreen()
        screen_geometry = screen.geometry()

        data = (
            f"Количество экранов: {len(QtWidgets.QApplication.screens())}\n"
            f"Текущее основное окно: {'Да' if self.isActiveWindow() else 'Нет'}\n"
            f"Разрешение экрана: {screen_geometry.width()}x{screen_geometry.height()}\n"
            f"На каком экране окно находится: {self.screen().name()}\n"
            f"Размеры окна: {self.size().width()}x{self.size().height()}\n"
            f"Минимальные размеры окна: {self.minimumSizeHint().width()}x{self.minimumSizeHint().height()}\n"
            f"Текущее положение окна: {self.pos()}\n"
            f"Координаты центра приложения: ({self.x() + self.width() // 2}, {self.y() + self.height() // 2})\n"
            f"Состояние окна: {'Свернуто' if self.isMinimized() else 'Развёрнуто' if self.isMaximized() else 'Активно' if self.isActiveWindow() else 'Отображено'}"
        )
        self.ui.plainTextEdit.appendPlainText(data)

    def log(self, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.log(f"Изменение размера окна: новый размер {self.size()}")

    def moveEvent(self, event):
        super().moveEvent(event)
        self.log(f"Перемещение окна: новая позиция {self.pos()}")


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
