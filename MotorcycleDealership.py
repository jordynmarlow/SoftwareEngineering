import sys, configparser
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from random import *

# constants
CONFIG_FILE = 'config.ini'

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
        
class AddPayment(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('AddPaymentDialog.ui', self)
        self.setStyleSheet(open('Stylesheet.qss').read())
        self.get_rate_bt.clicked.connect(self.getInterest)
        
    def getInterest(self):
        checkCard = CheckFormatCard(self.credit_card_text.toPlainText())
        checkSSN = CheckFormatSSN(self.ssn_text.toPlainText())
        if (checkCard and checkSSN):
            self.interest_rate_lbl.setText(GenerateInterest())
            self.get_rate_bt.hide()

class NewOrder(QDialog):
    def __init__(self, homepage):
        super().__init__()
        self.homepage = homepage
        self.mechanics = ['mechanic1', 'mechanic2'] # change this list to pull from all mechanics in db
        uic.loadUi('NewWorkOrderDialog.ui', self)
        self.setStyleSheet(open('Stylesheet.qss').read())
        #self.add_payment_bt_1.clicked.connect(self.openAddPayment)
        self.reassign_mechanic_bt.clicked.connect(self.reassignMechanic)
        
    def openAddPayment(self):
        #open AddPaymentDialog.ui
        dlg = AddPayment()
        dlg.exec_()

    def reassignMechanic(self):
        if self.homepage.getPIN():
            new_mechanic, ok = QInputDialog.getItem(self, 'Reassign mechanic', 'Choose a new mechanic.', self.mechanics, 0, True)
            self.mechanic_lbl.setText(new_mechanic)
            # change mechanic name in database for this work order

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
        self.change_pin_bt.clicked.connect(self.changePIN)
        # when a widget in inventory_scroll_area is clicked, connect to self.openInventory
    
    def getPIN(self):
        pin, ok = QInputDialog.getText(self, 'Manager PIN', 'Enter your PIN:')
        parser = configparser.ConfigParser()
        parser.read(CONFIG_FILE)
        while ok and pin != parser['DEFAULT']['ManagerPIN']:
            pin, ok = QInputDialog.getText(self, 'Manager Access Only', 'Incorrect PIN. Please try again.')
        return ok
    
    def changePIN(self):
        if self.getPIN():
            new_pin, ok = QInputDialog.getText(self, 'Manager PIN', 'Enter your new PIN:')
            parser = configparser.ConfigParser()
            parser['DEFAULT']['ManagerPIN'] = new_pin
            with open(CONFIG_FILE, 'w') as config_file:
                parser.write(config_file)

    def openTimesheet(self):
        #open TimeSheetDialog.ui
        dlg = Timesheet()
        dlg.exec_()

    def openEmployees(self):
        #open EmployeesDialog.ui
        if self.getPIN():
            dlg = Employees()
            dlg.exec_()

    def openAds(self):
        #open AdvertisementsDialog.ui
        if self.getPIN():
            dlg = Advertisements()
            dlg.exec_()

    def openNewOrder(self):
        #open NewOrderDialog.ui
        dlg = NewOrder(self)
        dlg.exec_()

    def openInventory(self):
        #open InventoryDialog.ui
        dlg = Inventory()
        dlg.exec_()

def CheckFormatCard(credNum):
    '''for x in range(16):
        credNum = credNum_s + str(randint(0,9))
    print("Card String: " + credNum)
    
    formatCred = credNum[0:4] + "-" + credNum[4:8] + "-" + credNum[8:12] + "-" + credNum[12:16]
    print("Formatted: " + formatCred)'''
    checkCard = True
    
    if (len(credNum) == 19):
        #xxxx-xxxx-xxxx-xxxx
        if (credNum[4] != "-" or credNum[9] != "-" or credNum[14] != "-"):
            checkCard = False
            
    else: checkCard = False
            
    return checkCard

def CheckFormatSSN(ssnNum):
    '''for x in range(9):
        ssnNum = ssnNum + str(randint(0,9))
    print("Card String: " + ssnNum)

    formatSSN = ssnNum[0:3] + "-" + ssnNum[3:5] + "-" + ssnNum[5:9]
    print("Formatted: " + formatSSN)'''
    checkSSN = True
    
    if (len(ssnNum) == 11):
        #xxx-xx-xxxx
        if (ssnNum[3] != "-" or ssnNum[6] != "-"):
            checkSSN = False
            
    else: checkSSN = False
            
    return checkSSN
    
def GenerateInterest():
    #if (CheckFormatCard(credNum) and CheckFormatSSN(ssnNum)):
    intRate = round(uniform(3,21), 2)
    return str(intRate)
    #     print(intRate)

'''
print(CheckFormatCard("1234-4321-6343-2346"))
print(CheckFormatSSN("222-13-2543"))
GenerateInterest("1234-4321-6343-2346", "222-13-2543")
'''

app = QApplication(sys.argv)
window = Homepage()
window.show()
sys.exit(app.exec_())

