import sys
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class MotorcycleDealership(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MotorcycleDealership.ui', self)
        self.show()

app = QApplication(sys.argv)
window = MotorcycleDealership()
window.show()
sys.exit(app.exec_())