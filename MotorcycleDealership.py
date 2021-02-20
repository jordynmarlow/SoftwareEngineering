import sys
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from random import *

class Timesheet(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('TimesheetDialog.ui', self)
        self.setStyleSheet(open('Stylesheet.qss').read())

class Employees(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('EmployeesDialog.ui', self)
        self.setStyleSheet(open('Stylesheet.qss').read())
        self.add_employee_bt.clicked.connect(self.openAddEmployees)
    
    def openAddEmployees(self):
        #open AddEmployeeDialog.ui
        dlg = AddEmployee()
        dlg.exec_()

class AddEmployee(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('AddEmployeeDialog.ui', self)
        self.setStyleSheet(open('Stylesheet.qss').read())

class Advertisements(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('AdvertisementsDialog.ui', self)
        self.setStyleSheet(open('Stylesheet.qss').read())
        self.add_advertisement_bt.clicked.connect(self.openAddAdvertisements)
    
    def openAddAdvertisements(self):
        #open AddAdvertisementDialog.ui
        dlg = AddAdvertisements()
        dlg.exec_()

class AddAdvertisements(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('AddAdvertisementDialog.ui', self)
        self.setStyleSheet(open('Stylesheet.qss').read())

class NewOrder(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('NewOrderDialog.ui', self)
        self.setStyleSheet(open('Stylesheet.qss').read())

class Inventory(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('InventoryDialog.ui', self)
        self.setStyleSheet(open('Stylesheet.qss').read())

class Homepage(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MotorcycleDealership.ui', self)
        self.setStyleSheet(open('Stylesheet.qss').read())
        self.setWindowTitle('Motorcycle Dealership')
        self.show()
        self.widgetInteractions()

    def widgetInteractions(self):
        self.timesheet_bt.clicked.connect(self.openTimesheet)
        self.employees_bt.clicked.connect(self.openEmployees)
        self.ads_bt.clicked.connect(self.openAds)
        self.new_order_bt.clicked.connect(self.openNewOrder)
        # when a widget in inventory_scroll_area is clicked, connect to self.openInventory

    def openTimesheet(self):
        #open TimeSheetDialog.ui
        dlg = Timesheet()
        dlg.exec_()

    def openEmployees(self):
        #open EmployeesDialog.ui
        dlg = Employees()
        dlg.exec_()

    def openAds(self):
        #open AdvertisementsDialog.ui
        dlg = Advertisements()
        dlg.exec_()

    def openNewOrder(self):
        #open NewOrderDialog.ui
        dlg = NewOrder()
        dlg.exec_()

    def openInventory(self):
        #open InventoryDialog.ui
        dlg = Inventory()
        dlg.exec_()

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


"""GenerateCard()
GenerateSSN()
GenerateInterest()"""

app = QApplication(sys.argv)
window = Homepage()
window.show()
sys.exit(app.exec_())
