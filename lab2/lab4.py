from PySide6 import QtWidgets, QtCore
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QSettings
import sys


class Window(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_ui()
        self.setup_ui()
        self.load_settings()

    def load_ui(self):
        loader = QUiLoader()
        self.ui = loader.load("ui/d_eventfilter_settings_form.ui", self)
        self.setLayout(self.ui.layout())

    def setup_ui(self):
        self.ui.comboBox.addItem("Decimal")
        self.ui.comboBox.addItem("Binary")
        self.ui.comboBox.addItem("Octal")
        self.ui.comboBox.addItem("Hexadecimal")

        self.ui.comboBox.setCurrentIndex(0)

        self.ui.dial.valueChanged.connect(self.update_value)
        self.ui.horizontalSlider.valueChanged.connect(self.update_dial_and_lcd)

        self.ui.comboBox.currentIndexChanged.connect(self.update_lcd_format)

        self.ui.dial.setFocusPolicy(QtCore.Qt.StrongFocus)

    def keyPressEvent(self, event):
        if self.ui.dial.hasFocus():
            if event.key() == QtCore.Qt.Key_Plus:
                self.ui.dial.setValue(self.ui.dial.value() + 1)
            elif event.key() == QtCore.Qt.Key_Minus:
                self.ui.dial.setValue(self.ui.dial.value() - 1)
            event.accept()
        else:
            super().keyPressEvent(event)

    def update_value(self, value):
        self.ui.lcdNumber.display(value)
        self.ui.horizontalSlider.setValue(value)
        self.update_lcd_format()

    def update_dial_and_lcd(self, value):
        self.ui.dial.setValue(value)
        self.ui.lcdNumber.display(value)
        self.update_lcd_format()

    def update_lcd_format(self):
        format_index = self.ui.comboBox.currentIndex()
        value = int(self.ui.lcdNumber.value())

        print(f"ComboBox changed: {format_index}")

        if format_index == 0:
            self.ui.lcdNumber.display(value)
        elif format_index == 1:
            self.ui.lcdNumber.display(int(bin(value)[2:]))
        elif format_index == 2:
            self.ui.lcdNumber.display(int(oct(value)[2:]))
        elif format_index == 3:
            self.ui.lcdNumber.display(int(hex(value)[2:], 16))

    def load_settings(self):
        settings = QSettings()
        last_value = settings.value("lcdValue", 0, type=int)
        last_format = settings.value("lcdFormat", 0, type=int)

        self.ui.lcdNumber.display(last_value)
        self.ui.comboBox.setCurrentIndex(last_format)
        self.update_lcd_format()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
