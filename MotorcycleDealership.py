import sys
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from random import *

class MotorcycleDealership(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MotorcycleDealership.ui', self)
        self.show()

def GenerateCard():
    credNum = 0
    for x in range(16):
        credNum = credNum*10 + randint(0,9)
    print("Card Int:", credNum)
    
    credNum_s = ""
    for x in range(16):
        credNum_s = credNum_s + str(randint(0,9))
    print("Card String: " + credNum_s)
    
    formatCred = credNum_s[0:4] + "-" + credNum_s[4:8] + "-" + credNum_s[8:12] + "-" + credNum_s[12:16]
    print("Formatted: " + formatCred)

def GenerateSSN():
    ssnNum = 0
    for x in range(9):
        ssnNum = ssnNum*10 + randint(0,9)
    print("Card Int:", ssnNum)
    
    ssnNum_s = ""
    for x in range(9):
        ssnNum_s = ssnNum_s + str(randint(0,9))
    print("Card String: " + ssnNum_s)
    
    formatSSN = ssnNum_s[0:3] + "-" + ssnNum_s[3:5] + "-" + ssnNum_s[5:9]
    print("Formatted: " + formatSSN)
    
    
def GenerateInterest():
    intRate = round(uniform(3,21), 2)
    print(intRate)


GenerateCard()
GenerateSSN()
GenerateInterest()
'''
app = QApplication(sys.argv)
window = MotorcycleDealership()
window.setStyleSheet(open('Stylesheet.qss').read())
window.show()
sys.exit(app.exec_())
'''