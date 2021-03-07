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

    # Use a connection object method to create cursor objects to navigate the three major table types
    sql_inventory_cursor = sql_connection.cursor()
    sql_orders_cursor = sql_connection.cursor()
    sql_employees_cursor = sql_connection.cursor()

    while 1 > 0:
        menu_option = input("What would you like to do? \n1. View all Inventory \n2. View all Orders \n"
                            "3. Filter by Inventory Type \n4. Filter by Order Type \n5. Sort Current Inventory \n"
                            "6. Sort Current Orders List \n7. Add Inventory Item \n8. Add Order \n"
                            "9. More \n0. Exit \n")
        if menu_option == '1':
            db_ops.view_inventory_full(sql_inventory_cursor)
        elif menu_option == '2':
            db_ops.view_orders_full(sql_orders_cursor)
        elif menu_option == '3':
            filter_db_inventory(sql_inventory_cursor)
        elif menu_option == '4':
            filter_db_orders(sql_orders_cursor)
        elif menu_option == '5':
            sort_table_inventory(sql_inventory_cursor)
        elif menu_option == '6':
            sort_table_orders(sql_orders_cursor)
        elif menu_option == '7':
            add_inventory(sql_connection)
        elif menu_option == '8':
            add_orders(sql_connection)
        elif menu_option == '9':
            more_option = input("1. Remove Inventory Item \n2. Remove Order \n3. Manager Functions \n")
            if more_option == '1':
                remove_inventory(sql_connection)
            elif more_option == '2':
                remove_inventory(sql_connection)
            elif more_option == '3':
                break
        elif menu_option == '0':
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
def sort_table_inventory(inventory_cursor):
    if current_inventory_table == "ProductsInventory":
        sort_option = input("You can filter by: \n 1. Year \n 2. Make \n 3. Model \n 4. Color \n 5. Item Number \n"
                            " 6. Price \n 7. Quantity \n")
        if sort_option == '1':
            db_ops.view_inventory_table_sorted(inventory_cursor, current_inventory_table, "YEAR")
        elif sort_option == '2':
            db_ops.view_inventory_table_sorted(inventory_cursor, current_inventory_table, "MAKE")
        elif sort_option == '3':
            db_ops.view_inventory_table_sorted(inventory_cursor, current_inventory_table, "MODEL")
        elif sort_option == '4':
            db_ops.view_inventory_table_sorted(inventory_cursor, current_inventory_table, "COLOR")
        elif sort_option == '5':
            db_ops.view_inventory_table_sorted(inventory_cursor, current_inventory_table, "ITEM_NUMBER")
        elif sort_option == '6':
            db_ops.view_inventory_table_sorted(inventory_cursor, current_inventory_table, "PRICE")
        elif sort_option == '7':
            db_ops.view_inventory_table_sorted(inventory_cursor, current_inventory_table, "QUANTITY")

    elif current_inventory_table == "PartsInventory":
        sort_option = input("You can filter by: \n 1. Item Number \n"
                            " 2. Price \n 3. Quantity \n")
        if sort_option == '1':
            db_ops.view_inventory_table_sorted(inventory_cursor, current_inventory_table, "ITEM_NUMBER")
        elif sort_option == '2':
            db_ops.view_inventory_table_sorted(inventory_cursor, current_inventory_table, "PRICE")
        elif sort_option == '3':
            db_ops.view_inventory_table_sorted(inventory_cursor, current_inventory_table, "QUANTITY")

    elif current_inventory_table == "MerchandiseInventory":
        sort_option = input("You can filter by: \n 1. Item Number \n"
                            " 2. Color \n 3. Size \n 4. Price \n 5. Quantity \n")
        if sort_option == '1':
            db_ops.view_inventory_table_sorted(inventory_cursor, current_inventory_table, "ITEM_NUMBER")
        elif sort_option == '2':
            db_ops.view_inventory_table_sorted(inventory_cursor, current_inventory_table, "COLOR")
        elif sort_option == '3':
            db_ops.view_inventory_table_sorted(inventory_cursor, current_inventory_table, "SIZE")
        elif sort_option == '4':
            db_ops.view_inventory_table_sorted(inventory_cursor, current_inventory_table, "PRICE")
        elif sort_option == '5':
            db_ops.view_inventory_table_sorted(inventory_cursor, current_inventory_table, "QUANTITY")


# Function that handles the (messy) UI side of sorting the current orders table by any one field
# Please note: this will not work unless a SINGLE orders list has already been picked.
# Every orders list has different columns, so they can't be sorted together.
def sort_table_orders(orders_cursor):
    if current_orders_table == "WorkOrders":
        sort_option = input("You can filter by: \n 1. Date \n 2. Order ID \n 3. Customer's First Name \n"
                            " 4. Customer's Last Name \n 5. Phone Number \n 6. Mechanic \n Archived/Active \n")
        if sort_option == '1':
            db_ops.view_orders_table_sorted(orders_cursor, current_orders_table, "DATE")
        elif sort_option == '2':
            db_ops.view_orders_table_sorted(orders_cursor, current_orders_table, "ORDER_ID")
        elif sort_option == '3':
            db_ops.view_orders_table_sorted(orders_cursor, current_orders_table, "CUSTOMER_FIRST")
        elif sort_option == '4':
            db_ops.view_orders_table_sorted(orders_cursor, current_orders_table, "CUSTOMER_LAST")
        elif sort_option == '5':
            db_ops.view_orders_table_sorted(orders_cursor, current_orders_table, "PHONE_NUMBER")
        elif sort_option == '6':
            db_ops.view_orders_table_sorted(orders_cursor, current_orders_table, "MECHANIC")
        elif sort_option == '7':
            db_ops.view_orders_table_sorted(orders_cursor, current_orders_table, "ARCHIVED")

    elif current_orders_table == "BikeOrders":
        sort_option = input("You can filter by: \n 1. Date \n 2. Item Number \n 3. Interest Rate \n"
                            " 4. Archived/Active \n")
        if sort_option == '1':
            db_ops.view_orders_table_sorted(orders_cursor, current_orders_table, "DATE")
        elif sort_option == '2':
            db_ops.view_orders_table_sorted(orders_cursor, current_orders_table, "ITEM_NUMBER")
        elif sort_option == '3':
            db_ops.view_orders_table_sorted(orders_cursor, current_orders_table, "INTEREST_RATE")
        elif sort_option == '4':
            db_ops.view_orders_table_sorted(orders_cursor, current_orders_table, "ARCHIVED")

    elif current_orders_table == "MerchandiseOrders":
        sort_option = input("You can filter by: \n 1. Date \n 2. Item Number \n 3. Archived/Active \n")
        if sort_option == '1':
            db_ops.view_orders_table_sorted(orders_cursor, current_orders_table, "DATE")
        elif sort_option == '2':
            db_ops.view_orders_table_sorted(orders_cursor, current_orders_table, "ITEM_NUMBER")
        elif sort_option == '3':
            db_ops.view_orders_table_sorted(orders_cursor, current_orders_table, "ARCHIVED")


# Function that handles the UI side of adding to an inventory.
def add_inventory(connection):
    global current_inventory_table  # The current inventory table will automatically switch to the one being added to.
    add_option = input("You can add to: \n 1. Products \n 2. Parts \n 3. Merchandise \n")
    if add_option == '1':
        current_inventory_table = "ProductsInventory"
        number_input = input("Item Number: ")  # Expected to be randomly generated in implementation
        year_input = input("Year: ")
        make_input = input("Make: ")
        model_input = input("Model: ")
        name = year_input + " " + make_input + " " + model_input
        color_input = input("Color: ")
        price_input = float(input("Price: "))
        quantity_input = int(input("Quantity: "))
        desc_input = input("Description: ")
        db_ops.add_product(connection, number_input, year_input, make_input, model_input, name, color_input,
                           price_input, quantity_input, desc_input)
    elif add_option == '2':
        current_inventory_table = "PartsInventory"
        number_input = input("Item Number: ")  # Expected to be randomly generated in implementation
        name_input = input("Item Name: ")
        price_input = float(input("Price: "))
        quantity_input = int(input("Quantity: "))
        desc_input = input("Description: ")
        db_ops.add_part(connection, number_input, name_input, price_input, quantity_input, desc_input)
    elif add_option == '3':
        current_inventory_table = "MerchandiseInventory"
        number_input = input("Item Number: ")  # Expected to be randomly generated in implementation
        name_input = input("Item Name: ")
        color_input = input("Color: ")
        size_input = input("Size: ")
        price_input = float(input("Price: "))
        quantity_input = int(input("Quantity: "))
        desc_input = input("Description: ")
        db_ops.add_merchandise(connection, number_input, name_input, color_input, size_input, price_input,
                               quantity_input, desc_input)


# Function that handles the UI side of adding to an orders list.
def add_orders(connection):
    global current_orders_table  # The current orders table will automatically switch to the one being added to.
    add_option = input("You can add a new: \n 1. Work Order \n 2. Bike Order \n 3. Merchandise Order \n")
    if add_option == '1':
        current_orders_table = "WorkOrders"
        date_input = input("Date: ")
        id_input = input("Order ID: ")
        first_input = input("Customer's First Name: ")
        last_input = input("Customer's Last Name: ")
        phone_input = input("Customer's Phone Number: ")
        mechanic_input = input("Assigned Mechanic: ")
        comments_input = input("Comments: ")
        archived = 0  # If a new order is being added, it's safe to assume it isn't archived.
        db_ops.add_work_order(connection, date_input, id_input, first_input, last_input, phone_input, mechanic_input,
                              comments_input, archived)
    elif add_option == '2':
        current_orders_table = "BikeOrders"
        date_input = input("Date: ")
        number_input = input("Item Number: ")
        interest_input = input("Interest Rate: ")
        archived = 0  # If a new order is being added, it's safe to assume it isn't archived.
        db_ops.add_bike_order(connection, date_input, number_input, interest_input, archived)
    elif add_option == '3':
        current_orders_table = "MerchandiseOrders"
        date_input = input("Date: ")
        number_input = input("Item Number: ")
        archived = 0  # If a new order is being added, it's safe to assume it isn't archived.
        db_ops.add_merchandise_order(connection, date_input, number_input, archived)


def remove_inventory(connection):
    # Removal functionality does not update the current table. This whole function is probably going to change quite
    # a bit in implementation, because we assume that the user clicked on something from the table they wanted to
    # remove from, so there wouldn't even be a choice that has to be made for the type of inventory to remove from.
    remove_option = input("You can remove from: \n 1. Products \n 2. Parts \n 3. Merchandise \n")
    if remove_option == '1':
        item_number_input = input("Product Item Number: ")
        db_ops.remove_product(connection, item_number_input)
    elif remove_option == '2':
        item_number_input = input("Part Item Number: ")
        db_ops.remove_part(connection, item_number_input)
    elif remove_option == '3':
        item_number_input = input("Merchandise Item Number: ")
        db_ops.remove_merchandise(connection, item_number_input)


def remove_orders(connection):
    # Removal functionality does not update the current table. This whole function is probably going to change quite
    # a bit in implementation, because we assume that the user clicked on something from the table they wanted to
    # remove from, so there wouldn't even be a choice that has to be made for the type of inventory to remove from.
    remove_option = input("You can remove from: \n 1. Work Orders \n 2. Bike Orders \n 3. Merchandise Orders \n")
    if remove_option == '1':
        id_input = input("Work Order ID: ")
        db_ops.remove_work_order(connection, id_input)
    elif remove_option == '2':
        item_number_input = input("Bike Item Number: ")
        db_ops.remove_bike_order(connection, item_number_input)
    elif remove_option == '3':
        item_number_input = input("Merchandise Item Number: ")
        db_ops.remove_merchandise_order(connection, item_number_input)


db_main()
