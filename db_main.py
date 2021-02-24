# A demo of how the the SQLite Database UI could work (logically).
# Any prompts to user input can be replaced with their GUI equivalent (clicking a button, etc.)
# Sorry about the if-else hell in some of the functions. Not too concerned since this isn't the actual interface
# (Also Python doesn't have built-in switch-case functionality).
# Main control program for the database

import db_ops  # Contains database operation functions

current_inventory_table = None  # A cursor for navigating the current inventory table
current_orders_table = None  # A cursor for navigating the current orders table

# Driving function of the Python-SQLite database interaction
def db_main():
    # Brief welcome statement
    print("Welcome to the Motorcycle Dealership SQLite Database Demo!")
    sql_connection = db_ops.connect_db('MotorDB.db')  # Call the connect_db function to get a connection object
    if sql_connection:
        print("You have connected to the database!")  # If the connection exists, it was successful. Tell the user.
    else:
        print("Connection failed.")  # If the connection does not exist, it failed. Tell the user.

    # Use a connection object method to create cursor objects to navigate the two major table types
    sql_inventory_cursor = sql_connection.cursor()
    sql_orders_cursor = sql_connection.cursor()

    while 1 > 0:
        menu_option = input("What would you like to do? \n 1. View all Inventory \n 2. View all Orders \n"
                            " 3. Filter by Inventory Type \n 4. Filter by Order Type \n 5. Sort Current Inventory \n"
                            " 6. Sort Current Orders List \n 7. Exit \n")
        if menu_option == '1':
            db_ops.view_inventory_full(sql_inventory_cursor)
        elif menu_option == '2':
            db_ops.view_orders_full(sql_orders_cursor)
        elif menu_option == '3':
            filter_db_inventory(sql_inventory_cursor)
        elif menu_option == '4':
            filter_db_orders(sql_orders_cursor)
        elif menu_option == '5':
            filter_table_inventory(sql_inventory_cursor)
        elif menu_option == '6':
            filter_table_orders(sql_orders_cursor)
        elif menu_option == '7':
            break


# Function that handles the UI side of picking a single inventory
def filter_db_inventory(inventory_cursor):
    global current_inventory_table
    db_option = input("Which inventory do you want to see? \n 1. Products \n 2. Parts \n 3. Merchandise \n")
    if db_option == '1':
        current_inventory_table = "ProductsInventory"
        db_ops.view_inventory_table(inventory_cursor, "ProductsInventory")
    elif db_option == '2':
        current_inventory_table = "PartsInventory"
        db_ops.view_inventory_table(inventory_cursor, "PartsInventory")
    elif db_option == '3':
        current_inventory_table = "MerchandiseInventory"
        db_ops.view_inventory_table(inventory_cursor, "MerchandiseInventory")


# Function that handles the UI side of picking a single orders list
def filter_db_orders(orders_cursor):
    global current_orders_table
    db_option = input("Which list of orders do you want to see? \n 1. Work Orders \n 2. Bike Orders \n"
                      " 3. Merchandise Orders \n")
    if db_option == '1':
        current_orders_table = "WorkOrders"
        db_ops.view_orders_table(orders_cursor, "WorkOrders")
    elif db_option == '2':
        current_orders_table = "BikeOrders"
        db_ops.view_orders_table(orders_cursor, "BikeOrders")
    elif db_option == '3':
        current_orders_table = "MerchandiseOrders"
        db_ops.view_orders_table(orders_cursor, "MerchandiseOrders")


# Function to handle the (messy) UI side of sorting the current inventory table by any one field
# Please note: this will not work unless a SINGLE inventory has already been picked.
# Every inventory has different columns, so they can't be sorted together.
def filter_table_inventory(inventory_cursor):
    if current_inventory_table == "ProductsInventory":
        filter_option = input("You can filter by: \n 1. Year \n 2. Make \n 3. Model \n 4. Color \n 5. Item Number \n"
                              " 6. Price \n 7. Quantity \n")
        if filter_option == '1':
            db_ops.view_inventory_table_sorted(inventory_cursor, current_inventory_table, "YEAR")
        elif filter_option == '2':
            db_ops.view_inventory_table_sorted(inventory_cursor, current_inventory_table, "MAKE")
        elif filter_option == '3':
            db_ops.view_inventory_table_sorted(inventory_cursor, current_inventory_table, "MODEL")
        elif filter_option == '4':
            db_ops.view_inventory_table_sorted(inventory_cursor, current_inventory_table, "COLOR")
        elif filter_option == '5':
            db_ops.view_inventory_table_sorted(inventory_cursor, current_inventory_table, "ITEM_NUMBER")
        elif filter_option == '6':
            db_ops.view_inventory_table_sorted(inventory_cursor, current_inventory_table, "PRICE")
        elif filter_option == '7':
            db_ops.view_inventory_table_sorted(inventory_cursor, current_inventory_table, "QUANTITY")

    elif current_inventory_table == "PartsInventory":
        filter_option = input("You can filter by: \n 1. Item Number \n"
                              " 2. Price \n 3. Quantity \n")
        if filter_option == '1':
            db_ops.view_inventory_table_sorted(inventory_cursor, current_inventory_table, "ITEM_NUMBER")
        elif filter_option == '2':
            db_ops.view_inventory_table_sorted(inventory_cursor, current_inventory_table, "PRICE")
        elif filter_option == '3':
            db_ops.view_inventory_table_sorted(inventory_cursor, current_inventory_table, "QUANTITY")

    elif current_inventory_table == "MerchandiseInventory":
        filter_option = input("You can filter by: \n 1. Item Number \n"
                              " 2. Color \n 3. Size \n 4. Price \n 5. Quantity \n")
        if filter_option == '1':
            db_ops.view_inventory_table_sorted(inventory_cursor, current_inventory_table, "ITEM_NUMBER")
        elif filter_option == '2':
            db_ops.view_inventory_table_sorted(inventory_cursor, current_inventory_table, "COLOR")
        elif filter_option == '3':
            db_ops.view_inventory_table_sorted(inventory_cursor, current_inventory_table, "SIZE")
        elif filter_option == '4':
            db_ops.view_inventory_table_sorted(inventory_cursor, current_inventory_table, "PRICE")
        elif filter_option == '5':
            db_ops.view_inventory_table_sorted(inventory_cursor, current_inventory_table, "QUANTITY")


# Function that handles the (messy) UI side of sorting the current orders table by any one field
# Please note: this will not work unless a SINGLE orders list has already been picked.
# Every orders list has different columns, so they can't be sorted together.
def filter_table_orders(orders_cursor):
    if current_orders_table == "WorkOrders":
        filter_option = input("You can filter by: \n 1. Date \n 2. Order ID \n 3. Customer's First Name \n"
                              " 4. Customer's Last Name \n 5. Phone Number \n 6. Mechanic \n Archived/Active \n")
        if filter_option == '1':
            db_ops.view_orders_table_sorted(orders_cursor, current_inventory_table, "DATE")
        elif filter_option == '2':
            db_ops.view_orders_table_sorted(orders_cursor, current_inventory_table, "ORDER_ID")
        elif filter_option == '3':
            db_ops.view_orders_table_sorted(orders_cursor, current_inventory_table, "CUSTOMER_FIRST")
        elif filter_option == '4':
            db_ops.view_orders_table_sorted(orders_cursor, current_inventory_table, "CUSTOMER_LAST")
        elif filter_option == '5':
            db_ops.view_orders_table_sorted(orders_cursor, current_inventory_table, "PHONE_NUMBER")
        elif filter_option == '6':
            db_ops.view_orders_table_sorted(orders_cursor, current_inventory_table, "MECHANIC")
        elif filter_option == '7':
            db_ops.view_orders_table_sorted(orders_cursor, current_inventory_table, "ARCHIVED")

    elif current_orders_table == "BikeOrders":
        filter_option = input("You can filter by: \n 1. Date \n 2. Item Number \n 3. Interest Rate \n"
                              " 4. Archived/Active \n")
        if filter_option == '1':
            db_ops.view_orders_table_sorted(orders_cursor, current_inventory_table, "DATE")
        elif filter_option == '2':
            db_ops.view_orders_table_sorted(orders_cursor, current_inventory_table, "ITEM_NUMBER")
        elif filter_option == '3':
            db_ops.view_orders_table_sorted(orders_cursor, current_inventory_table, "INTEREST_RATE")
        elif filter_option == '4':
            db_ops.view_orders_table_sorted(orders_cursor, current_inventory_table, "ARCHIVED")

    elif current_orders_table == "MerchandiseOrders":
        filter_option = input("You can filter by: \n 1. Date \n 2. Item Number \n 3. Archived/Active \n")
        if filter_option == '1':
            db_ops.view_orders_table_sorted(orders_cursor, current_inventory_table, "DATE")
        elif filter_option == '2':
            db_ops.view_orders_table_sorted(orders_cursor, current_inventory_table, "ITEM_NUMBER")
        elif filter_option == '3':
            db_ops.view_orders_table_sorted(orders_cursor, current_inventory_table, "ARCHIVED")


db_main()
