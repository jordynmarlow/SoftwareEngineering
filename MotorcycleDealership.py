import sys, sqlite3, configparser
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import random
from random import randint
import db_ops

# constants
CONFIG_FILE = 'config.ini'
UI_PATH = './UI/'

sql_connection = None
try:
    sql_connection = sqlite3.connect('MotorDB.db')  # Try to connect to the database
except Error as e:  # ...Except if there is an sqlite3 error,
    print(e)  # print the error
sql_cursor = sql_connection.cursor()

class InventoryDatabase():
    def __init__(self):
        pass

    def get_fields(self, item_no):
        if item_no[0] == 'M': # merchandise item
            sql_cursor.execute('SELECT I.NAME, I.ITEM_NUMBER, I.QUANTITY, I.PRICE, I.COLOR, I.SIZE FROM MerchandiseInventory I WHERE I.ITEM_NUMBER=\'%s\'' % (item_no))
        elif item_no[0] == 'B': # bike item
            sql_cursor.execute('SELECT I.NAME, I.ITEM_NUMBER, I.QUANTITY, I.PRICE, I.COLOR FROM ProductsInventory I WHERE I.ITEM_NUMBER=\'%s\'' % (item_no))
        elif item_no[0] == 'P': # parts item
            sql_cursor.execute('SELECT I.NAME, I.ITEM_NUMBER, I.QUANTITY, I.PRICE FROM PartsInventory I WHERE I.ITEM_NUMBER=\'%s\'' % (item_no))
        return sql_cursor.fetchall()

    def get_inventory_items(self, query):
        sql_cursor.execute(query)
        return sql_cursor.fetchall()
    
    def get_table(self, character):
        if character == 'M': # merchandise item
            return 'MerchandiseInventory'
        elif character == 'B': # bike item
            return 'ProductsInventory'
        elif character == 'P': # parts item
            return 'PartsInventory'
    
    def get_quantity(self, item_no):
        sql_cursor.execute('select I.QUANTITY from %s I where I.ITEM_NUMBER=\'%s\'' % (self.get_table(item_no[0]), item_no))
        return sql_cursor.fetchall()[0][0]

    def set_quantity(self, item_no, quantity):
        sql_cursor.execute('update %s set QUANTITY = %d where ITEM_NUMBER=\'%s\'' % (self.get_table(item_no[0]), self.get_quantity(item_no) + quantity, item_no))

class OrdersDatabase(): 
    def __init__(self):
        pass
    
    def get_fields(self, order_id):
        if order_id[0] == 'M': # merchandise order
            labels = ['Order Number', 'Item Number', 'Date']
            sql_cursor.execute('SELECT O.ORDER_ID, O.ITEM_NUMBER, O.DATE FROM MerchandiseOrders O WHERE O.ORDER_ID=\'%s\'' % (order_id))
        elif order_id[0] == 'B': # bike order
            labels = ['Order Number', 'Item Number', 'Date', 'Interest Rate']
            sql_cursor.execute('SELECT O.ORDER_ID, O.ITEM_NUMBER, O.DATE, O.INTEREST_RATE FROM BikeOrders O WHERE O.ORDER_ID=\'%s\'' % (order_id))
        elif order_id[0] == 'P': # parts order
            labels = ['Order Number', 'Item Number', 'Date', 'First Name', 'Last Name', 'Phone Number', 'Mechanic', 'Archived']
            sql_cursor.execute('SELECT O.ORDER_ID, O.ITEM_NUMBER, O.DATE, O.CUSTOMER_FIRST, O.CUSTOMER_LAST, O.PHONE_NUMBER, O.MECHANIC, O.ARCHIVED FROM WorkOrders O WHERE O.ORDER_ID=\'%s\'' % (order_id))
        return labels, sql_cursor.fetchall()
    
    def get_table(self, character):
        if character == 'M': # merchandise order
            return 'MerchandiseOrders'
        elif character == 'B': # bike order
            return 'BikeOrders'
        elif character == 'P': # work order
            return 'WorkOrders'

    def get_mechanics(self):
        sql_cursor.execute('select E.EMPLOYEE_ID from Employees E where E.POSITION=\'Mechanic\'')
        mechanics = [i[0] for i in sql_cursor.fetchall()]
        return mechanics
    
    def get_order_items(self, query):
        sql_cursor.execute(query)
        return sql_cursor.fetchall()

    def archive(self, order_id):
        sql_cursor.execute('update %s set ARCHIVED = 1 where ORDER_ID=\'%s\'' % (self.get_table(order_id[0]), order_id))
    
    def set_mechanic(self, order_id, new_mechanic):
        sql_cursor.execute('update WorkOrders set MECHANIC = \'%s\' where ORDER_ID = \'%s\'' % (new_mechanic, order_id))

class Timesheet(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(UI_PATH + 'TimesheetDialog.ui', self)
        self.setStyleSheet(open('Stylesheet.qss').read())

class Employees(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(UI_PATH + 'EmployeesDialog.ui', self)
        self.setStyleSheet(open('Stylesheet.qss').read())
        self.add_employee_bt.clicked.connect(self.openAddEmployees)
        self.temp_employee_bt.clicked.connect(self.openSingleEmployee)

    def openAddEmployees(self):
        # open AddEmployeeDialog.ui
        dlg = AddEmployee()
        dlg.exec_()
        
    def openSingleEmployee(self):
        #open SingleEmployeeDialog.ui
        dlg = SingleEmployee()
        dlg.exec_()

class AddEmployee(QDialog):
    def __init__(self):
        super().__init__()
        self.connection = db_ops.connect_db('MotorDB.db')
        uic.loadUi(UI_PATH + 'AddEmployeeDialog.ui', self)
        self.setStyleSheet(open('Stylesheet.qss').read())
        self.status_edit.selectionChanged.connect(self.setStatus)
        self.name_edit.selectionChanged.connect(self.setName)
        self.position_edit.selectionChanged.connect(self.setPosition)
        # self.phone_edit.selectionChanged.connect(self.setPhone)
        # self.address_edit.selectionChanged.connect(self.setAddress)
        # self.salary_edit.selectionChanged.connect(self.setSalary)
        # self.comments_edit.selectionChanged.connect(self.setComments)
        self.employee_id_edit = ""
        for x in range(6):
            self.employee_id_edit += str(randint(0,9))

        self.accepted.connect(self.confirm)
        self.rejected.connect(self.dbDisconnect)

    def setStatus(self):
        self.status = self.status_edit.text()

    def setName(self):
        self.name = self.name_edit.text()

    def setPosition(self):
        self.position = self.position_edit.text()
        
    # def setPhone(self):
    #     self.phone = self.phone_edit.text()

    # def setAddress(self):
    #     self.address = self.address_edit.text()

    # def setSalary(self):
    #     self.salary = self.salary_edit.text()
        
    # def setComments(self):
    #     self.comments = self.comments_edit.toPlainText()

    def confirm(self):
        db_ops.add_employee(self.connection, self.employee_id, self.name, self.position, self.status)
        db_ops.add_timesheet(self.connection, self.employee_id)

    def dbDisconnect(self):
        self.connection.close()

class SingleEmployee(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(UI_PATH + 'SingleEmployeeDialog.ui', self)
        self.setStyleSheet(open('Stylesheet.qss').read())
        self.edit_employee_bt.clicked.connect(self.openEditEmployee)
    
    def openEditEmployee(self):
        #open EditEmployeeDialog.ui
        dlg = EditEmployee()
        dlg.exec_()
   
class EditEmployee(QDialog):
    def __init__(self):
        super().__init__()
        # self.connection = db_ops.connect_db('MotorDB.db')
        uic.loadUi(UI_PATH + 'EditEmployeeDialog.ui', self)
        self.setStyleSheet(open('Stylesheet.qss').read())
        
        # pull from database to the labels first
        
        
        # send edit changes to database
        # self.status_edit.selectionChanged.connect(self.setStatus)
        # self.name_edit.selectionChanged.connect(self.setName)
        # self.position_edit.selectionChanged.connect(self.setPosition)
        # self.phone_edit.selectionChanged.connect(self.setPhone)
        # self.address_edit.selectionChanged.connect(self.setAddress)
        # self.salary_edit.selectionChanged.connect(self.setSalary)
        # self.comments_edit.selectionChanged.connect(self.setComments)
        
        # send employee ID too?

        # self.accepted.connect(self.confirm)
        # self.rejected.connect(self.dbDisconnect)

    # def setStatus(self):
    #     self.status = self.status_edit.text()

    # def setName(self):
    #     self.name = self.name_edit.text()

    # def setPosition(self):
    #     self.position = self.position_edit.text()
        
    # def setPhone(self):
    #     self.phone = self.phone_edit.text()

    # def setAddress(self):
    #     self.address = self.address_edit.text()

    # def setSalary(self):
    #     self.salary = self.salary_edit.text()
        
    # def setComments(self):
    #     self.comments = self.comments_edit.toPlainText()

class Advertisements(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(UI_PATH + 'AdvertisementsDialog.ui', self)
        self.setStyleSheet(open('Stylesheet.qss').read())
        self.add_advertisement_bt.clicked.connect(self.openAddAdvertisements)
        self.temp_advert_bt.clicked.connect(self.openSingleAdvertisement)

    def openAddAdvertisements(self):
        # open AddAdvertisementDialog.ui
        dlg = AddAdvertisements()
        dlg.exec_()
        
    def openSingleAdvertisement(self):
        #open SingleAdvertisementDialog.ui
        dlg = SingleAdvertisement()
        dlg.exec_()

class AddAdvertisements(QDialog):
    def __init__(self):
        super().__init__()
        # self.connection = db_ops.connect_db('MotorDB.db')
        uic.loadUi(UI_PATH + 'AddAdvertisementDialog.ui', self)
        self.setStyleSheet(open('Stylesheet.qss').read())
        # self.status_edit.selectionChanged.connect(self.setStatus)
        # self.name_edit.selectionChanged.connect(self.setName)
        # self.type_edit.selectionChanged.connect(self.setType)
        # self.cost_edit.selectionChanged.connect(self.setCost)
        # self.description_edit.selectionChanged.connect(self.setDescription)

        # self.accepted.connect(self.confirm)
        # self.rejected.connect(self.dbDisconnect)
        
    # def setStatus(self):
    #     self.status = self.status_edit.text()

    # def setName(self):
    #     self.name = self.name_edit.text()

    # def setType(self):
    #     self.type = self.type_edit.text()
        
    # def setCost(self):
    #     self.cost = self.cost_edit.text()
        
    # def setDesription(self):
    #     self.description = self.description_edit.toPlainText()
    
class SingleAdvertisement(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(UI_PATH + 'SingleAdvertisementDialog.ui', self)
        self.setStyleSheet(open('Stylesheet.qss').read())
        self.edit_advertisement_bt.clicked.connect(self.openEditAdvertisement)
    
    def openEditAdvertisement(self):
        #open EditAdvertisementDialog.ui
        dlg = EditAdvertisement()
        dlg.exec_()
    
class Order(QDialog):
    def __init__(self, order_id, homepage):
        super().__init__()
        uic.loadUi(UI_PATH + 'OrderDialog.ui', self)
        self.setStyleSheet(open('Stylesheet.qss').read())
        self.order_id = order_id
        self.homepage = homepage
        self.populateFields()
        self.reassign_mechanic_bt.clicked.connect(self.reassign_mechanic)
        self.archive_bt.clicked.connect(self.archive)
    
    def reassign_mechanic(self):
        if self.homepage.getPIN('manager'):
            mechanics = orders.get_mechanics()
            new_mechanic, ok = QInputDialog.getItem(self, 'Reassign Mechanic', 'Choose a new mechanic.', mechanics)
            orders.set_mechanic(self.order_id, new_mechanic)
            self.populateFields()

    def archive(self):
        orders.archive(self.order_id)
        self.populateFields()

    def populateFields(self):
        labels, values = orders.get_fields(self.order_id)
        desc = ''
        for i in range(0, len(values[0])):
            desc += labels[i] + ': ' + str(values[0][i]) + '\n'
        self.description_lbl.setText(desc)
        if self.order_id[0] != 'P':
            self.reassign_mechanic_bt.hide()
            self.archive_bt.hide()

class EditAdvertisement(QDialog):
    def __init__(self):
        super().__init__()
        # self.connection = db_ops.connect_db('MotorDB.db')
        uic.loadUi(UI_PATH + 'EditAdvertisementDialog.ui', self)
        self.setStyleSheet(open('Stylesheet.qss').read())
        
        # pull from database to the labels first
        
        # send edit changes to the database
        # self.status_edit.selectionChanged.connect(self.setStatus)
        # self.name_edit.selectionChanged.connect(self.setName)
        # self.type_edit.selectionChanged.connect(self.setType)
        # self.cost_edit.selectionChanged.connect(self.setCost)
        # self.description_edit.selectionChanged.connect(self.setDescription)

        # self.accepted.connect(self.confirm)
        # self.rejected.connect(self.dbDisconnect)
        
    # def setStatus(self):
    #     self.status = self.status_edit.text()

    # def setName(self):
    #     self.name = self.name_edit.text()

    # def setType(self):
    #     self.type = self.type_edit.text()
        
    # def setCost(self):
    #     self.cost = self.cost_edit.text()
        
    # def setDesription(self):
    #     self.description = self.description_edit.toPlainText()
        
class AddPayment(QDialog): # possibly in openAddPayment functions from new orders, send in the price as well (Phil)
    def __init__(self, orderPage):
        super().__init__()
        self.orderPage = orderPage  # order page the payment dialog opened from
        uic.loadUi(UI_PATH + 'AddPaymentDialog.ui', self)
        self.setStyleSheet(open('Stylesheet.qss').read())
        self.get_rate_bt.clicked.connect(self.getInterest)

    def getInterest(self):
        credNum = self.credit_card_text.toPlainText()
        ssnNum = self.ssn_text.toPlainText()
        if (CheckFormatCard(credNum) and CheckFormatSSN(ssnNum)):
            interest = GenerateInterest(credNum, ssnNum)
            self.interest_rate_lbl.setText(interest)
            self.message_lbl.setText("Interest generated and saved!")
            self.orderPage.order_interest_lbl.setText(
                interest)  # set interest in new order page (later should execute when OK is pressed)
            # self.get_rate_bt.hide()
        else:
            self.message_lbl.setText("Wrong format for Credit Card or SSN! Please double check them and try again.")
            self.interest_rate_lbl.setText("")

class NewWorkOrder(QDialog):
    def __init__(self, homepage):
        super().__init__()
        self.homepage = homepage
        uic.loadUi(UI_PATH + 'NewWorkOrderDialog.ui', self)
        self.setStyleSheet(open('Stylesheet.qss').read())
        self.connection = db_ops.connect_db('MotorDB.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT GROUP_CONCAT(NAME) FROM Employees WHERE POSITION = 'Mechanic'")
        self.mechanics = self.cursor.fetchone()[0].split(',')
        self.item_number = "defaultid"
        #self.add_payment_bt.clicked.connect(self.openAddPayment)
        self.add_mechanic_bt.clicked.connect(self.addMechanic)
        self.first_edit.editingFinished.connect(self.setFirst)
        self.last_edit.editingFinished.connect(self.setLast)
        self.phone_edit.editingFinished.connect(self.setPhone)
        self.date_edit.dateChanged.connect(self.setStartDate)
        self.end_date = "TBD"
        self.comments_edit.textChanged.connect(self.setComments)
        self.order_id = "P"
        for x in range(6):
            self.order_id += str(randint(0, 9))

        self.accepted.connect(self.confirm)
        self.rejected.connect(self.dbDisconnect)

    def openAddPayment(self):
        # open AddPaymentDialog.ui
        dlg = AddPayment(self)
        dlg.exec_()

    def addMechanic(self):
        new_mechanic, ok = QInputDialog.getItem(self, 'Add mechanic', 'Choose a mechanic.', self.mechanics, 0, True)
        self.mechanic_lbl.setText(new_mechanic)
        self.mechanic = new_mechanic

    def setFirst(self):
        self.first = self.first_edit.text()

    def setLast(self):
        self.last = self.last_edit.text()

    def setPhone(self):
        self.phone = self.phone_edit.text()

    def setStartDate(self):
        self.start_date = self.date_edit.date().toString("MM/dd/yyyy")

    def setEndDate(self):
        pass
        self.reassign_mechanic_bt.clicked.connect(self.reassignMechanic)
    
    def populateFields(self, fields):
        # populate description_lbl in OrderDialog.ui
        print(fields)

    def setComments(self):
        self.comments = self.comments_edit.toPlainText()

    def confirm(self):
        db_ops.add_work_order(self.connection, self.order_id, self.item_number, self.start_date, self.end_date, self.first,
                              self.last, self.phone, self.mechanic, self.comments, "0")

    def dbDisconnect(self):
        self.connection.close()

class NewBikeOrder(QDialog):
    def __init__(self, homepage):
        super().__init__()
        self.homepage = homepage
        uic.loadUi(UI_PATH + 'NewBikeOrderDialog.ui', self)
        self.setStyleSheet(open('Stylesheet.qss').read())

        self.connection = db_ops.connect_db('MotorDB.db')
        self.item_number = "defaultid"
        self.make_edit.editingFinished.connect(self.setMake)
        self.model_edit.editingFinished.connect(self.setModel)
        self.year_edit.editingFinished.connect(self.setYear)
        self.color_edit.editingFinished.connect(self.setColor)
        self.first_edit.editingFinished.connect(self.setFirst)
        self.last_edit.editingFinished.connect(self.setLast)
        self.phone_edit.editingFinished.connect(self.setPhone)
        self.date_edit.dateChanged.connect(self.setStartDate)
        self.add_payment_bt.clicked.connect(self.openAddPayment)
        self.comments_text.textChanged.connect(self.setComments)
        self.order_id = "B"
        for x in range(6):
            self.order_id += str(randint(0, 9))

        self.accepted.connect(self.confirm)
        self.rejected.connect(self.dbDisconnect)

    def setMake(self):
        self.make = self.make_edit.text()

    def setModel(self):
        self.model = self.model_edit.text()

    def setYear(self):
        self.year = self.year_edit.text()

    def setColor(self):
        self.color = self.color_edit.text()

    def setFirst(self):
        self.first = self.first_edit.text()

    def setLast(self):
        self.last = self.last_edit.text()

    def setPhone(self):
        self.phone = self.phone_edit.text()

    def setStartDate(self):
        self.start_date = self.date_edit.date().toString("MM/dd/yyyy")

    def openAddPayment(self):
        # open AddPaymentDialog.ui
        dlg = AddPayment(self)
        dlg.exec_()
        self.interest_rate = self.order_interest_lbl.text()

    def setComments(self):
        self.comments = self.comments_text.toPlainText()

    def confirm(self):
        self.name = self.year + " " + self.make + " " + self.model
        db_ops.add_bike_order(self.connection, self.order_id, self.item_number, self.make, self.model, self.year,
                              self.name, self.color, self.first, self.last, self.phone, self.start_date,
                              self.interest_rate, self.comments, '0')

    def dbDisconnect(self):
        self.connection.close()

class MerchandiseOrder(QDialog):
    def __init__(self, homepage):
        super().__init__()
        self.homepage = homepage
        uic.loadUi(UI_PATH + 'MerchandiseOrderDialog.ui', self)
        self.setStyleSheet(open('Stylesheet.qss').read())

        self.connection = db_ops.connect_db('MotorDB.db')
        self.item_number = "defaultid"
        self.type_edit.editingFinished.connect(self.setType)
        self.color_edit.editingFinished.connect(self.setColor)
        self.size_edit.editingFinished.connect(self.setSize)
        self.quantity_box.textChanged.connect(self.setQuantity)
        self.date_edit.dateChanged.connect(self.setDate)
        self.comments_text.textChanged.connect(self.setComments)
        self.order_id = "M"
        for x in range(6):
            self.order_id += str(randint(0, 9))

        self.accepted.connect(self.confirm)
        self.rejected.connect(self.dbDisconnect)

    def setType(self):
        self.item_type = self.type_edit.text()

    def setColor(self):
        self.color = self.color_edit.text()

    def setSize(self):
        self.size = self.size_edit.text()

    def setQuantity(self):
        self.quantity = self.quantity_box.cleanText()

    def setDate(self):
        self.date = self.date_edit.date().toString("MM/dd/yyyy")

    def setComments(self):
        self.comments = self.comments_text.toPlainText()

    def confirm(self):
        db_ops.add_merchandise_order(self.connection, self.order_id, self.item_number, self.item_type, self.color,
                                     self.size, self.quantity, self.date, self.comments, '0')

    def dbDisconnect(self):
        self.connection.close()

class Inventory(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(UI_PATH + 'InventoryDialog.ui', self)
        self.setStyleSheet(open('Stylesheet.qss').read())
        self.new_order_bt.clicked.connect(self.openNewOrder)
        self.restock_bt.clicked.connect(self.restockItem)
    
    def restockItem(self):
        inventory.set_quantity(self.item_no, self.restock_quantity_sb.value())
        self.populateFields(self.item_no)
    
    def populateFields(self, item_no):
        self.item_no = item_no
        values = inventory.get_fields(item_no)
        self.name_lbl.setText(values[0][0])
        labels = ['Name', 'Item Number', 'Quantity', 'Price', 'Color', 'Size']
        self.item_no = values[0][1]
        desc = ''
        for i in range(1, len(values[0])):
            desc += labels[i] + ': ' + str(values[0][i]) + '\n'
        self.description_lbl.setText(desc)

    def openNewOrder(self):  # open one of the 3 new orders
        if self.item_no[0] == 'B':
            dlg = NewBikeOrder(self)

        elif self.item_no[0] == 'P':
            dlg = NewWorkOrder(self)

        elif self.item_no[0] == 'M':
            dlg = MerchandiseOrder(self)

        dlg.exec_()


class NewProductItem(QDialog):
    def __init__(self, homepage):
        super().__init__()
        self.homepage = homepage
        uic.loadUi(UI_PATH + 'NewProductItemDialog.ui', self)
        self.setStyleSheet(open('Stylesheet.qss').read())

        self.connection = db_ops.connect_db('MotorDB.db')
        self.year_edit.editingFinished.connect(self.setYear)
        self.make_edit.editingFinished.connect(self.setMake)
        self.model_edit.editingFinished.connect(self.setModel)
        self.color_edit.editingFinished.connect(self.setColor)
        self.price_edit.editingFinished.connect(self.setPrice)
        self.quantity_box.textChanged.connect(self.setQuantity)
        self.desc_text.textChanged.connect(self.setDescription)
        self.item_number = "B"
        for x in range(6):
            self.item_number += str(randint(0,9))

        self.accepted.connect(self.confirm)
        self.rejected.connect(self.dbDisconnect)

    def setYear(self):
        self.year = self.year_edit.text()

    def setMake(self):
        self.make = self.make_edit.text()

    def setModel(self):
        self.model = self.model_edit.text()

    def setColor(self):
        self.color = self.color_edit.text()

    def setPrice(self):
        self.price = self.price_edit.text()

    def setQuantity(self):
        self.quantity = self.quantity_box.cleanText()

    def setDescription(self):
        self.description = self.desc_text.toPlainText()

    def confirm(self):
        self.name = self.year + " " + self.make + " " + self.model
        db_ops.add_product(self.connection, self.item_number, self.year, self.make, self.model, self.name, self.color,
                           self.price, self.quantity, self.description)

    def dbDisconnect(self):
            self.connection.close()


class NewPartItem(QDialog):
    def __init__(self, homepage):
        super().__init__()
        self.homepage = homepage
        uic.loadUi(UI_PATH + 'NewPartItemDialog.ui', self)
        self.setStyleSheet(open('Stylesheet.qss').read())

        self.connection = db_ops.connect_db('MotorDB.db')
        self.name_edit.editingFinished.connect(self.setName)
        self.price_edit.editingFinished.connect(self.setPrice)
        self.quantity_box.textChanged.connect(self.setQuantity)
        self.desc_text.textChanged.connect(self.setDescription)
        self.item_number = "P"
        for x in range(6):
            self.item_number += str(randint(0,9))

        self.accepted.connect(self.confirm)
        self.rejected.connect(self.dbDisconnect)

    def setName(self):
        self.name = self.name_edit.text()

    def setPrice(self):
        self.price = self.price_edit.text()

    def setQuantity(self):
        self.quantity = self.quantity_box.cleanText()

    def setDescription(self):
        self.description = self.desc_text.toPlainText()

    def confirm(self):
        db_ops.add_part(self.connection, self.item_number, self.name, self.price, self.quantity, self.description)

    def dbDisconnect(self):
        self.connection.close()


class NewMerchandiseItem(QDialog):
    def __init__(self, homepage):
        super().__init__()
        self.homepage = homepage
        uic.loadUi(UI_PATH + 'NewMerchandiseItemDialog.ui', self)
        self.setStyleSheet(open('Stylesheet.qss').read())

        self.connection = db_ops.connect_db('MotorDB.db')
        self.name_edit.editingFinished.connect(self.setName)
        self.color_edit.editingFinished.connect(self.setColor)
        self.size_edit.editingFinished.connect(self.setSize)
        self.price_edit.editingFinished.connect(self.setPrice)
        self.quantity_box.textChanged.connect(self.setQuantity)
        self.desc_text.textChanged.connect(self.setDescription)
        self.item_number = "M"
        for x in range(6):
            self.item_number += str(randint(0,9))

        self.accepted.connect(self.confirm)
        self.rejected.connect(self.dbDisconnect)

    def setName(self):
        self.name = self.name_edit.text()

    def setColor(self):
        self.color = self.color_edit.text()

    def setSize(self):
        self.size = self.size_edit.text()

    def setPrice(self):
        self.price = self.price_edit.text()

    def setQuantity(self):
        self.quantity = self.quantity_box.cleanText()

    def setDescription(self):
        self.description = self.desc_text.toPlainText()

    def confirm(self):
        db_ops.add_merchandise(self.connection, self.item_number, self.name, self.color, self.size, self.price,
                               self.quantity, self.description)

    def dbDisconnect(self):
        self.connection.close()


    def reassignMechanic(self):
        if self.homepage.getPIN():
            mechanics = orders.get_mechanics(self.order_id)
            new_mechanic, ok = QInputDialog.getItem(self, 'Reassign Mechanic', 'Choose a new mechanic.', mechanics, 0, True)

class InventoryFilters(QDialog):
    def __init__(self, homepage):
        super().__init__()
        self.homepage = homepage
        uic.loadUi(UI_PATH + 'FilterInventory.ui', self)
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

class OrderFilters(QDialog):
    def __init__(self, homepage):
        super().__init__()
        self.homepage = homepage
        uic.loadUi(UI_PATH + 'FilterOrders.ui', self)
        self.setStyleSheet(open('Stylesheet.qss').read())
        self.filter_mechanics_combo.hide()
        self.show_items_bt.clicked.connect(self.update_list)
        self.work_rb.toggled.connect(self.extra_filters)
        self.filter_mechanics_combo.addItem('Filter by mechanic...')
        for mechanic in orders.get_mechanics():
            self.filter_mechanics_combo.addItem(mechanic)
    
    def extra_filters(self):
        if self.work_rb.isChecked():
            self.filter_mechanics_combo.show()
        else:
            self.filter_mechanics_combo.hide()
    
    def update_list(self):
        merch = 'SELECT O.ORDER_ID, O.DATE FROM MerchandiseOrders O'
        work = 'SELECT O.ORDER_ID, O.DATE FROM WorkOrders O'
        bikes = 'SELECT O.ORDER_ID, O.DATE FROM BikeOrders O'
        if self.merch_rb.isChecked():
            query = merch
        elif self.work_rb.isChecked():
            query = work
            if self.filter_mechanics_combo.currentIndex() > 0:
                query += ' where O.MECHANIC=\'%s\'' % (self.filter_mechanics_combo.currentText())
        elif self.bikes_rb.isChecked():
            query = bikes
        else: # all_rb is checked
            query = 'SELECT O.ORDER_ID, O.DATE FROM (%s UNION %s UNION %s) O' % (merch, work, bikes)
        self.items = orders.get_order_items(query)
        self.close()

class Homepage(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(UI_PATH + 'MotorcycleDealership.ui', self)
        self.setStyleSheet(open('Stylesheet.qss').read())
        self.setWindowTitle('Motorcycle Dealership')
        #self.show()
        self.inventory_filters = InventoryFilters(self)
        self.order_filters = OrderFilters(self)
        self.populateInventoryList()
        self.populateOrdersList()
        self.widgetInteractions()

    def widgetInteractions(self):
        self.timesheet_bt.clicked.connect(self.openTimesheet)
        self.employees_bt.clicked.connect(self.openEmployees)
        self.ads_bt.clicked.connect(self.openAds)
        self.new_order_bt.clicked.connect(self.openNewOrder)
        self.change_pin_bt.clicked.connect(self.changePIN)
        self.add_item_bt.clicked.connect(self.addItem)
        self.inventory_list.itemClicked.connect(self.openInventoryItem)
        self.orders_list.itemClicked.connect(self.openOrder)
        self.filter_inventory_bt.clicked.connect(self.openInventoryFilters)
        self.filter_orders_bt.clicked.connect(self.openOrderFilters)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Exit', 'Are you sure you want to exit?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            sql_cursor.close()
            sql_connection.commit()
            event.accept()
        else:
            event.ignore()

    def addItem(self):
        items = ['Bike', 'Part', 'Merchandise']
        item, ok = QInputDialog.getItem(self, 'Add Inventory Item', 'Select item type: ', items, 0, False)
        if item == 'Bike':
            self.openNewProduct()
        elif item == 'Part':
            self.openNewPart()
        else: # item == 'Merchandise'
            self.openNewMerch()

    def populateInventoryList(self):
        self.inventory_list.setVerticalScrollBar(QScrollBar(self))
        self.inventory_filters.update_list()
        self.inventory_list.clear()
        for item in self.inventory_filters.items:
            self.inventory_list.addItem(QListWidgetItem(str(item[0]) + '\t' + item[1] + '\t' + str(item[2]) + '\t' + str(item[3])))

    def populateOrdersList(self):
        self.orders_list.setVerticalScrollBar(QScrollBar(self))
        self.order_filters.update_list()
        self.orders_list.clear()
        for item in self.order_filters.items:
            self.orders_list.addItem(QListWidgetItem(str(item[0]) + '\t\t' + item[1]))
        # when a widget in inventory_scroll_area is clicked, connect to self.openInventory

    def addNewID(self, id):  # Allows new users to be added. Outside of #51 scope.
        return False

    def verifyID(self):  # Ensures that any ID being entered is valid
        id, ok = QInputDialog.getText(self, 'Enter ID', 'Enter your ID.')
        id = "".join(id.split())  # Clears whitespace from entries
        id = id.lower()  # Keeps CONFIG_FILE sections safe
        parser = configparser.ConfigParser()
        parser.read(CONFIG_FILE)
        id_list = parser['LOGIN']
        while ok:
            try:
                id_list[id]  # If a user's section exists, we can move on to asking for a password
                if ok:
                    return self.getPIN(id), id
                else:
                    return False, ""  # No reason to ask for PIN if user stops entering ID
            except:  # If a user's section does not exist, we can ask if they would like to add it before requesting re-entry
                id, ok = QInputDialog.getText(self, 'Enter Name',
                                              'Enter your name.\nRemember you have to enter it the same way every time.')
                if self.addNewID(id):
                    return True, id

    def getPIN(self, id):  # Ensures that any PIN being entered is valid
        pin, ok = QInputDialog.getText(self, 'Enter PIN', 'Enter PIN for ' + id + ":")
        parser = configparser.ConfigParser()
        parser.read(CONFIG_FILE)
        while ok and pin != parser['LOGIN'][id]:
            pin, ok = QInputDialog.getText(self, 'Enter PIN', 'Incorrect PIN.\nPlease try again.')
        return ok

    def changePIN(self):  # Changes the PIN for a given user
        ok, id = self.verifyID()
        if ok:
            new_pin, ok = QInputDialog.getText(self, 'Enter PIN', 'Enter your new PIN:')
            while ok:
                if id == 'manager' or (len(new_pin) == 4 and new_pin.isnumeric()):
                    break
                else:
                    new_pin, ok = QInputDialog.getText(self, 'Enter PIN',
                                                       'PIN must be 4-digit number.\nEnter your new PIN:')
            parser = configparser.ConfigParser()
            parser.read(CONFIG_FILE)
            parser['LOGIN'][id] = new_pin
            with open(CONFIG_FILE, 'w') as config_file:
                parser.write(config_file)

    def openInventoryFilters(self):
        self.inventory_filters.exec_()
        self.populateInventoryList()
    
    def openOrderFilters(self):
        self.order_filters.exec_()
        self.populateOrdersList()

    def openTimesheet(self):
        # open TimeSheetDialog.ui
        if self.verifyID():
            dlg = Timesheet()
            dlg.exec_()

    def openEmployees(self):
        # open EmployeesDialog.ui
        if self.getPIN('manager'):
            dlg = Employees()
            dlg.exec_()

    def openAds(self):
        # open AdvertisementsDialog.ui
        if self.getPIN('manager'):
            dlg = Advertisements()
            dlg.exec_()

    def openNewOrder(self):
        # open NewWorkOrderDialog.ui
        dlg = NewWorkOrder(self)
        dlg.exec_()

    def openInventoryItem(self, item):
        # open InventoryDialog.ui
        dlg = Inventory()
        item_no = item.text().split('\t')[0]
        dlg.populateFields(item_no)
        dlg.exec_()

    def openNewProduct(self):
        # open NewProductItemDialog.ui
        dlg = NewProductItem(self)
    
    def openOrder(self, item):
        #open OrderDialog.ui
        order_id = item.text().split('\t')[0]
        dlg = Order(order_id, self)
        dlg.exec_()

    def openNewPart(self):
        #open NewPartItemDialog.ui
        dlg = NewPartItem(self)
        dlg.exec_()

    def openNewMerch(self):
        #open NewMerchandiseItemDialog.ui
        dlg = NewMerchandiseItem(self)
        dlg.exec_()


def CheckFormatCard(credNum):
    '''for x in range(16):
      credNum = credNum_s + str(randint(0,9))
  print("Card String: " + credNum)
  formatCred = credNum[0:4] + "-" + credNum[4:8] + "-" + credNum[8:12] + "-" + credNum[12:16]
  print("Formatted: " + formatCred)'''
    checkCard = True

    if (len(credNum) == 19):  # correct length
        # xxxx-xxxx-xxxx-xxxx
        if (credNum[4] != "-" or credNum[9] != "-" or credNum[14] != "-"):  # correct dash spots
            checkCard = False
        else:  # only integers
            noDash = credNum.split("-")
            for num in noDash:
                try:
                    int(num)
                except ValueError:
                    checkCard = False

    else:
        checkCard = False

    return checkCard


def CheckFormatSSN(ssnNum):
    '''for x in range(9):
      ssnNum = ssnNum + str(randint(0,9))
  print("Card String: " + ssnNum)
  formatSSN = ssnNum[0:3] + "-" + ssnNum[3:5] + "-" + ssnNum[5:9]
  print("Formatted: " + formatSSN)'''
    checkSSN = True

    if (len(ssnNum) == 11):  # correct length
        # xxx-xx-xxxx
        if (ssnNum[3] != "-" or ssnNum[6] != "-"):  # correct dash spots
            checkSSN = False

        else:  # only integers
            noDash = ssnNum.split("-")
            for num in noDash:
                try:
                    int(num)
                except ValueError:
                    checkSSN = False

    else:
        checkSSN = False

    return checkSSN


def GenerateInterest(credNum, ssnNum):
    ''' random interest rate
  intRate = round(uniform(3,21), 2)
  return str(intRate)
  #     print(intRate)
  '''
    credNoDash = credNum.split("-")
    ssnNoDash = ssnNum.split("-")
    finalC = 1
    finalS = 1

    for cNum in credNoDash:
        finalC += finalC * int(cNum) + int(cNum) / 10000

    for sNum in ssnNoDash:
        finalS += finalS * int(sNum) + int(sNum) / 10000

    interest = round(finalC % 11 + finalS % 11 + 1, 2)
    return str(interest)


'''
#print(CheckFormatCard("1234-4421-6333-2346"))
#print(CheckFormatSSN("222-13-2443"))
GenerateInterest("3274-3422-6739-2367", "236-16-2838")
'''

inventory = InventoryDatabase()
orders = OrdersDatabase()
app = QApplication(sys.argv)
window = Homepage()
window.show()
sys.exit(app.exec_())