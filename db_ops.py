# This file contains a variety of functions for interacting with the database.
# These include connecting to the database, viewing the database, filter the database, and adding to the database.

# import os  # Allows for directory traversal (delete if not needed)
import sqlite3  # Allows for sqlite3 database interaction
from sqlite3 import Error  # Allows python to communicate errors from sqlite3 database


# Function to connect to the database
def connect_db(database):
    # os.chdir('..\sqlite')  # Goes up one directory, then goes into sqlite directory (delete if not needed)
    new_connection = None  # Instantiates connection variable with value None
    try:
        new_connection = sqlite3.connect(database)  # Try to connect to the database
        print(sqlite3.version)  # Print the version of sqlite (Verify that the connection worked)
    except Error as e:  # ...Except if there is an sqlite3 error,
        print(e)  # print the error

    return new_connection  # Return the created connection object


# Function to display full inventory list
# Argument is a cursor object that we assume was create in the main controller program with the connection object.
def view_inventory_full(cursor):
    view_inventory_table(cursor, "ProductsInventory")
    view_inventory_table(cursor, "PartsInventory")
    view_inventory_table(cursor, "MerchandiseInventory")


# Function to display full order list
# Argument is a cursor object that we assume was create in the main controller program with the connection object.
def view_orders_full(cursor):
    view_orders_table(cursor, "WorkOrders")
    view_orders_table(cursor, "BikeOrders")
    view_orders_table(cursor, "MerchandiseOrders")


# Function to view only one inventory at once
# Arguments include cursor object and name of desired table
def view_inventory_table(cursor, inventory_table):
    cursor.execute("SELECT * FROM %s" % inventory_table)  # Select from the desired inventory table...
    table = cursor.fetchall()  # Take every entry in this table
    for rows in table:  # For every row in this table,
        print(rows)  # Print the row.


# Function to view only one order list at once
# Arguments include cursor object and name of desired table
def view_orders_table(cursor, orders_table):
    cursor.execute("SELECT * FROM %s" % orders_table)  # Select from the desired inventory table...
    table = cursor.fetchall()  # Take every entry in this table
    for rows in table:  # For every row in this table,
        print(rows)  # Print the row.


# Function to view only one inventory that has been filtered according to a user-selected field
# Arguments include cursor object, the inventory table to be filtered, and the field by which to filter
# For now, the code assumes that ascending order (ASC) is preferred.
def view_inventory_table_sorted(cursor, inventory_table, inventory_column):
    cursor.execute("SELECT * FROM %s ORDER BY %s ASC" % (inventory_table, inventory_column))
    table = cursor.fetchall()
    for rows in table:
        print(rows)


# Function to view only one orders list that has been filtered according to a user-selected field
# Arguments include cursor object, the orders list table to be filtered, and the field by which to filter
# For now, the code assumes that ascending order (ASC) is preferred.
def view_orders_table_sorted(cursor, orders_table, orders_column):
    cursor.execute("SELECT * FROM %s ORDER BY %s ASC" % (orders_table, orders_column))
    table = cursor.fetchall()
    for rows in table:
        print(rows)


# Function to add a product to the inventory
# Arguments include the connection object and fields corresponding to required database columns
def add_product(connection, item_number, year, make, model, name, color, price, quantity, description):
    # Uses the connection object to execute an insertion. Important: arguments used in VALUES need to be strings inside
    # strings. When we implement this, we can totally just use (str(str()) on user input values.
    connection.execute("INSERT INTO ProductsInventory (ITEM_NUMBER,YEAR,MAKE,MODEL,NAME,COLOR,PRICE,QUANTITY,"
                       "DESCRIPTION) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')"
                       % (item_number, year, make, model, name, color, price, quantity, description))

    connection.commit()  # Commit the changes made to the database. Won't save without this.
    print("Product added!")  # Send message confirming product addition to database.


# Function to add a part to the inventory
# Arguments include the connection object and fields corresponding to required database columns
def add_part(connection, item_number, name, price, quantity, description):
    # Uses the connection object to execute an insertion. Important: arguments used in VALUES need to be strings inside
    # strings. When we implement this, we can totally just use (str(str()) on user input values.
    connection.execute("INSERT INTO PartsInventory (ITEM_NUMBER,NAME,PRICE,QUANTITY,DESCRIPTION) VALUES "
                       "('%s','%s','%s','%s','%s')" % (item_number, name, price, quantity, description))

    connection.commit()  # Commit the changes made to the database. Won't save without this.
    print("Part added!")  # Send the message confirming part addition to database.


# Function to add merchandise to the inventory
# Arguments include the connection object and fields corresponding to required database columns
def add_merchandise(connection, item_number, name, color, size, price, quantity, description):
    # Uses the connection object to execute an insertion. Important: arguments used in VALUES need to be strings inside
    # strings. When we implement this, we can totally just use (str(str()) on user input values.
    connection.execute("INSERT INTO MerchandiseInventory (ITEM_NUMBER,NAME,COLOR,SIZE,PRICE,QUANTITY,DESCRIPTION) "
                       "VALUES ('%s','%s','%s','%s','%s','%s','%s')" % (item_number, name, color, size, price, quantity,
                                                              description))

    connection.commit()  # Commit the changes made to the database. Won't save without this.
    print("Merch added!")  # Send the message confirming merchandise addition to database.


# Function to add work order
# Arguments include the connection object and fields corresponding to required database columns
def add_work_order(connection, order_id, item_number, start_date, end_date, customer_first, customer_last, phone_number, mechanic, comments, archived):
    # Uses the connection object to execute an insertion. Important: arguments used in VALUES need to be strings inside
    # strings. When we implement this, we can totally just use (str(str()) on user input values.
    connection.execute(
        "INSERT INTO WorkOrders (ORDER_ID,ITEM_NUMBER,DATE,END_DATE,CUSTOMER_FIRST,CUSTOMER_LAST,PHONE_NUMBER,"
        "MECHANIC,COMMENTS,ARCHIVED) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
        % (order_id, item_number, start_date, end_date, customer_first, customer_last, phone_number, mechanic, comments, archived))

    connection.commit()  # Commit the changes made to the database. Won't save without this.
    print("Work order added!")  # Send the message confirming work order addition to database.


# Function to add bike order
# Arguments include the connection object and fields corresponding to required database columns
def add_bike_order(connection, order_id, item_number, make, model, year, name, color, customer_first, customer_last, phone_number, date, interest_rate, comments, archived):
    # Uses the connection object to execute an insertion. Important: arguments used in VALUES need to be strings inside
    # strings. When we implement this, we can totally just use (str(str()) on user input values.
    connection.execute("INSERT INTO BikeOrders (ORDER_ID,ITEM_NUMBER,MAKE,MODEL,YEAR,NAME,COLOR,CUSTOMER_FIRST,CUSTOMER_LAST,PHONE_NUMBER,DATE,"
                       "INTEREST_RATE,COMMENTS,ARCHIVED) VALUES "
                       "('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
                       % (order_id, item_number, make, model, year, name, color, customer_first, customer_last,
                          phone_number, date, interest_rate, comments, archived))

    connection.commit()  # Commit the changes made to the database. Won't save without this.
    print("Bike order added!")  # Send the message confirming bike order addition to database.


# Function to add merchandise order
# Arguments include the connection object and fields corresponding to required database columns
def add_merchandise_order(connection, order_id, item_number, item_type, color, size, quantity, date, comments, archived):
    # Uses the connection object to execute an insertion. Important: arguments used in VALUES need to be strings inside
    # strings. When we implement this, we can totally just use (str(str()) on user input values.
    connection.execute("INSERT INTO MerchandiseOrders (ORDER_ID,ITEM_NUMBER,ITEM_TYPE,COLOR,SIZE,QUANTITY,DATE,COMMENTS,ARCHIVED) VALUES "
                       "('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (order_id, item_number, item_type, color, size, quantity, date, comments, archived))

    connection.commit()  # Commit the changes made to the database. Won't save without this.
    print("Merch order added!")  # Send the message confirming merchandise order addition to database.


# Function to remove a product from the inventory
def remove_product(connection, item_number):
    connection.execute("DELETE FROM ProductsInventory WHERE ITEM_NUMBER = '%s'" % item_number)
    connection.commit()
    print("Product removed!")


# Function to remove a part from the inventory
def remove_part(connection, item_number):
    connection.execute("DELETE FROM PartsInventory WHERE ITEM_NUMBER = '%s'" % item_number)
    connection.commit()
    print("Part removed!")


# Function to remove a piece of merchandise from the inventory
def remove_merchandise(connection, item_number):
    connection.execute("DELETE FROM MerchandiseInventory WHERE ITEM_NUMBER = '%s'" % item_number)
    connection.commit()
    print("Merchandise removed!")


# Function to remove an order from the work orders list
def remove_work_order(connection, order_id):
    connection.execute("DELETE FROM WorkOrders WHERE ORDER_ID = '%s'" % order_id)
    connection.commit()
    print("Work Order removed!")


# Function to remove an order from the bike orders list
def remove_bike_order(connection, item_number):
    connection.execute("DELETE FROM BikeOrders WHERE ITEM_NUMBER = '%s'" % item_number)
    connection.commit()
    print("Bike Order removed!")


# Function to remove an order from the merchandise orders list
def remove_merchandise_order(connection, item_number):
    connection.execute("DELETE FROM MerchandiseOrders WHERE ITEM_NUMBER = '%s'" % item_number)
    connection.commit()
    print("Merchandise removed!")


# Function to view the list of employees
def view_employees(cursor):
    cursor.execute("SELECT * FROM Employees")  # Select from the employees table
    table = cursor.fetchall()  # Take every entry in this table
    for rows in table:  # For every row in this table,
        print(rows)  # Print the row.

def add_employee(connection, employee_id, name, position, status):
    connection.execute("INSERT INTO Employees (EMPLOYEE_ID,NAME,POSITION,STATUS) VALUES "
                       "('%s','%s','%s','%s')" % (employee_id, name, position, status))
    connection.commit()
    print("Employee added!")

def add_timesheet(connection, employee_id):
    connection.execute("CREATE TABLE Timesheet_%s (WEEK INT NOT NULL PRIMARY KEY,SUNDAY FLOAT NOT NULL,"
                        "MONDAY FLOAT NOT NULL,TUESDAY FLOAT NOT NULL,WEDNESDAY FLOAT NOT NULL,THURSDAY FLOAT NOT NULL,"
                       "FRIDAY FLOAT NOT NULL,SATURDAY FLOAT NOT NULL,TOTAL_HOURS FLOAT NOT NULL );" % employee_id)
    connection.commit()