import sys, sqlite3
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from random import *
from sqlite3 import Error

sql_connection = None

def connect_to_db():
    try:
        sql_connection = sqlite3.connect('MotorDB.db')  # Try to connect to the database
    except Error as e:  # ...Except if there is an sqlite3 error,
        print(e)  # print the error
    return sql_connection.cursor()

class InventoryDatabase():
    def __init__(self):
        self.cursor = connect_to_db()
    
    def get_all_inventory_items(self):
        self.cursor.execute('SELECT * FROM \
                                (SELECT I.ITEM_NUMBER, I.PRICE, I.QUANTITY FROM ProductsInventory I UNION\
                                SELECT I.ITEM_NUMBER, I.PRICE, I.QUANTITY FROM PartsInventory I UNION\
                                SELECT I.ITEM_NUMBER, I.PRICE, I.QUANTITY FROM MerchandiseInventory I)')
        return self.cursor.fetchall()

    def get_fields(self, item_no):
        self.cursor.execute('SELECT * FROM \
                                (SELECT I.ITEM_NUMBER, I.PRICE, I.QUANTITY FROM ProductsInventory I UNION\
                                SELECT I.ITEM_NUMBER, I.PRICE, I.QUANTITY FROM PartsInventory I UNION\
                                SELECT I.ITEM_NUMBER, I.PRICE, I.QUANTITY FROM MerchandiseInventory I) I\
                            WHERE I.ITEM_NUMBER=\'%s\'' % (item_no))
        return self.cursor.fetchall()[0]

class OrdersDatabase():
    def __init__(self):
        self.cursor = connect_to_db()
    
    def get_all_orders(self):
        self.cursor.execute('SELECT * FROM \
                                (SELECT O.ORDER_ID, O.DATE FROM WorkOrders O UNION\
                                SELECT O.ITEM_NUMBER, O.DATE FROM BikeOrders O UNION\
                                SELECT O.ITEM_NUMBER, O.DATE FROM MerchandiseOrders O)')
        return self.cursor.fetchall()

    def get_fields(self, item_no):
        self.cursor.execute('SELECT * FROM \
                                (SELECT O.ORDER_ID, O.DATE FROM WorkOrders O UNION\
                                SELECT O.ITEM_NUMBER, O.DATE FROM BikeOrders O UNION\
                                SELECT O.ITEM_NUMBER, O.DATE FROM MerchandiseOrders O) O\
                            WHERE O.ITEM_NUMBER=\'%s\'' % (item_no))
        return self.cursor.fetchall()[0]

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
    
    def populateFields(self, fields):
        self.item_no_lbl.setText(fields[0])
        #self.name_lbl.setText()
        self.price_lbl.setText(fields[1])
        self.quantity_lbl.setText(fields[2])
    
class Order(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('OrderDialog.ui', self)
        self.setStyleSheet(open('Stylesheet.qss').read())
    
    def populateFields(self, fields):
        # populate fields in OrderDialog.ui
        pass

class Homepage(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MotorcycleDealership.ui', self)
        self.setStyleSheet(open('Stylesheet.qss').read())
        self.setWindowTitle('Motorcycle Dealership')
        self.show()
        self.populateInventoryList()
        self.populateOrdersList()
        self.widgetInteractions()

    def widgetInteractions(self):
        self.timesheet_bt.clicked.connect(self.openTimesheet)
        self.employees_bt.clicked.connect(self.openEmployees)
        self.ads_bt.clicked.connect(self.openAds)
        self.new_order_bt.clicked.connect(self.openNewOrder)
        self.inventory_list.itemClicked.connect(self.openInventoryItem)
        # self.orders_list.itemClicked.connect(self.openOrder)
    
    def populateInventoryList(self):
        self.inventory_list.setVerticalScrollBar(QScrollBar(self))
        self.inventory = InventoryDatabase()
        items = self.inventory.get_all_inventory_items()
        for item in items:
            self.inventory_list.addItem(QListWidgetItem('\t\t\t'.join(item)))
    
    def populateOrdersList(self):
        self.orders_list.setVerticalScrollBar(QScrollBar(self))
        self.orders = OrdersDatabase()
        items = self.orders.get_all_orders()
        for item in items:
            self.orders_list.addItem(QListWidgetItem('\t\t'.join(item)))

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

    def openInventoryItem(self, item):
        #open InventoryDialog.ui
        dlg = Inventory()
        dlg.populateFields(self.inventory.get_fields(item.text().split('\t')[0]))
        dlg.exec_()
    
    def openOrder(self, item):
        #open OrderDialog.ui
        dlg = Order()
        dlg.populateFields(self.orders.get_fields(item.text().split('\t')[0]))
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

def GenerateInterest(credNum, ssnNum):
    if (CheckFormatCard(credNum) and CheckFormatSSN(ssnNum)):
        intRate = round(uniform(3,21), 2)
        print(intRate)

'''
print(CheckFormatCard("1234-4321-6343-2346"))
print(CheckFormatSSN("222-13-2543"))
GenerateInterest("1234-4321-6343-2346", "222-13-2543")
'''

app = QApplication(sys.argv)
window = Homepage()
window.show()
sys.exit(app.exec_())
