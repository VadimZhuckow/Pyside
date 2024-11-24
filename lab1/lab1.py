from PySide6 import QtWidgets
from untitled import Ui_Form


class Window(QtWidgets.QRhiWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)


app = QtWidgets.QApplication()
window = Window()
window.show()

app.exec()
