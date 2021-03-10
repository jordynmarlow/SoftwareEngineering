import sys, sqlite3
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from random import *
from sqlite3 import Error


sql_connection = None

def connect_to_db():
    try:
        sql_connection = sqlite3.connect('database.db')  # Try to connect to the database
    except Error as e:  # ...Except if there is an sqlite3 error,
        print(e)  # print the error
    return sql_connection.cursor()

class InventoryDatabase():
    def __init__(self):
        self.cursor = connect_to_db()
    
    def get_all_inventory_items(self):
        self.cursor.execute('SELECT * FROM \
                                (SELECT I.ITEM_NUMBER, I.NAME FROM ProductsInventory I UNION\
                                SELECT I.ITEM_NUMBER, I.NAME FROM PartsInventory I UNION\
                                SELECT I.ITEM_NUMBER, I.NAME FROM MerchandiseInventory I)')
        return self.cursor.fetchall()

    def get_fields(self, item_no, name):
        self.cursor.execute('SELECT * FROM \
                                (SELECT I.ITEM_NUMBER, I.NAME, I.QUANTITY, I.PRICE, I.COLOR FROM ProductsInventory I UNION\
                                SELECT I.ITEM_NUMBER, I.NAME, I.QUANTITY, I.PRICE FROM PartsInventory I UNION\
                                SELECT I.ITEM_NUMBER, I.NAME, I.QUANTITY, I.PRICE, I.COLOR, I.SIZE FROM MerchandiseInventory I) I WHERE I.ITEM_NUMBER=%s AND NAME=\'%s\'' % (item_no, name))
        print(self.cursor.fetchall())

    def get_type(self, item_no, name):
        tables = ['ProductsInventory', 'PartsInventory', 'MerchandiseInventory']
        for table in tables:
            self.cursor.execute('SELECT * FROM %s WHERE ITEM_NUMBER=%s AND NAME=\'%s\'' % (table, item_no, name))
            if len(self.cursor.fetchall()) > 0:
                return table

    def get_inventory_items(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

class OrdersDatabase(): 
    def __init__(self):
        self.cursor = connect_to_db()
    
    def get_all_orders(self):
        self.cursor.execute('SELECT * FROM \
                                (SELECT O.ORDER_ID, O.DATE FROM WorkOrders O UNION\
                                SELECT O.ORDER_ID, O.DATE FROM BikeOrders O UNION\
                                SELECT O.ORDER_ID, O.DATE FROM MerchandiseOrders O)')
        return self.cursor.fetchall()

    def get_mechanics(order_id):
        self.cursor.execute('SELECT O.MECHANIC FROM WorkOrders O WHERE O.ORDER_ID=%s' % (order_id))
        return self.cursor.fetchall()

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
        # populate description_lbl in InventoryDialog.ui
        pass

class Order(QDialog):
    def __init__(self, order_id):
        super().__init__()
        uic.loadUi('OrderDialog.ui', self)
        self.setStyleSheet(open('Stylesheet.qss').read())
        self.order_id = order_id
        self.reassign_mechanic_bt.clicked.connect(self.reassignMechanic)
    
    def populateFields(self, fields):
        # populate description_lbl in OrderDialog.ui
        pass

    def reassignMechanic(self):
        if self.homepage.getPIN():
            mechanics = orders.get_mechanics(self.order_id)
            new_mechanic, ok = QInputDialog.getItem(self, 'Reassign Mechanic', 'Choose a new mechanic.', mechanics, 0, True)

class InventoryFilters(QDialog):
    def __init__(self, homepage):
        super().__init__()
        self.homepage = homepage
        uic.loadUi('FilterInventory.ui', self)
        self.setStyleSheet(open('Stylesheet.qss').read())
        self.show_items_bt.clicked.connect(self.update_list)

    def update_list(self):
        cols = 'I.ITEM_NUMBER, I.NAME, I.QUANTITY, I.PRICE'
        merch = 'SELECT %s FROM MerchandiseInventory I' % (cols)
        parts = 'SELECT %s FROM PartsInventory I' % (cols)
        bikes = 'SELECT %s FROM ProductsInventory I' % (cols)
        if self.merch_rb.isChecked():
            query = merch
        elif self.parts_rb.isChecked():
            query = parts
        elif self.bikes_rb.isChecked():
            query = bikes
        else: # all_rb is checked
            query = 'SELECT * FROM (%s UNION %s UNION %s) I' % (merch, parts, bikes)
        if self.in_stock_cb.isChecked():
            query += ' WHERE I.QUANTITY>0'
        if self.sort_combo.currentIndex() == 1: # sort by price (low to high)
            query += ' ORDER BY PRICE ASC'
        elif self.sort_combo.currentIndex() == 2: # sort by price (high to low)
            query += ' ORDER BY PRICE DESC'
        self.items = inventory.get_inventory_items(query)
        self.close()

class Homepage(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MotorcycleDealership.ui', self)
        self.setStyleSheet(open('Stylesheet.qss').read())
        self.setWindowTitle('Motorcycle Dealership')
        self.show()
        self.inventory_filters = InventoryFilters(self)
        self.populateInventoryList()
        self.populateOrdersList()
        self.widgetInteractions()

    def widgetInteractions(self):
        self.timesheet_bt.clicked.connect(self.openTimesheet)
        self.employees_bt.clicked.connect(self.openEmployees)
        self.ads_bt.clicked.connect(self.openAds)
        self.new_order_bt.clicked.connect(self.openNewOrder)
        #self.inventory_list.itemClicked.connect(self.openInventoryItem)
        #self.orders_list.itemClicked.connect(self.openOrder)
        self.filter_inventory_bt.clicked.connect(self.openInventoryFilters)

    def populateInventoryList(self):
        self.inventory_list.setVerticalScrollBar(QScrollBar(self))
        self.inventory_filters.update_list()
        self.inventory_list.clear()
        for item in self.inventory_filters.items:
            self.inventory_list.addItem(QListWidgetItem(str(item[0]) + '\t' + item[1] + '\t' + str(item[2]) + '\t' + str(item[3])))
    
    def populateOrdersList(self):
        self.orders_list.setVerticalScrollBar(QScrollBar(self))
        self.orders = OrdersDatabase()
        items = self.orders.get_all_orders()
        for item in items:
            self.orders_list.addItem(QListWidgetItem('\t\t'.join(item)))

    def openInventoryFilters(self):
        #open TimeSheetDialog.ui
        self.inventory_filters.exec_()
        self.populateInventoryList()

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
        item_no = item.text().split('\t')[0]
        name = item.text().split('\t')[1]
        dlg.populateFields(inventory.get_fields(item_no, name))
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

inventory = InventoryDatabase()
orders = OrdersDatabase()
app = QApplication(sys.argv)
window = Homepage()
window.show()
sys.exit(app.exec_())
