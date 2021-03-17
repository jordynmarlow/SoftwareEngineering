import sqlite3
con = sqlite3.connect('MotorDB.db')
cursor = con.cursor()

"""schema = 'ITEM_NUMBER, YEAR, MAKE, MODEL, NAME, COLOR, PRICE, QUANTITY, DESCRIPTION'
#cursor.execute('drop table ProductsInventory')
#cursor.execute('create table ProductsInventory(ITEM_NUMBER integer primary key autoincrement, NAME varchar(100), COLOR varchar(20), PRICE int, QUANTITY int)')
cursor.execute('insert into ProductsInventory (%s) values (\'B16753495\', \'2021\', \'Yamaha\', \'Star Venture\', \'2021 Yamaha Star Venture\', \'white\', 26999, 4, \'\')' % schema)
cursor.execute('insert into ProductsInventory (%s) values (\'B16753496\', \'2021\', \'Harley Davidson\', \'Low Rider S\', \'2021 Harley Davidson Low Rider S\', \'black\', 17999, 4, \'\')' % schema)
cursor.execute('insert into ProductsInventory (%s) values (\'B16753497\', \'2020\', \'Yamaha\', \'Tracer 900 GT\', \'2020 Yamaha Tracer 900 GT\', \'black\', 12999, 3, \'\')' % schema)
cursor.execute('insert into ProductsInventory (%s) values (\'B16753498\', \'2019\', \'Honda\', \'Gold Wing Tour\', \'2019 Honda Gold Wing Tour\', \'red\', 28300, 2, \'\')' % schema)
cursor.execute('insert into ProductsInventory (%s) values (\'B16753499\', \'2021\', \'Yamaha\',  \'FJR1300ES\', \'2021 Yamaha FJR1300ES\', \'blue\', 17999, 6, \'\')' % schema)
cursor.execute('insert into ProductsInventory (%s) values (\'B16753500\', \'2021\', \'Harley Davidson\', \'Livewire\', \'2021 Harley Davidson Livewire\', \'black\', 29799, 6, \'\')' % schema)
cursor.execute('insert into ProductsInventory (%s) values (\'B16753501\', \'2019\', \'Honda\', \'Rebel 500\', \'2019 Honda Rebel 500\', \'black\', 4599, 3, \'\')' % schema)
cursor.execute('insert into ProductsInventory (%s) values (\'B16753502\', \'2020\', \'Harley Davidson\', \'Forty-Eight\', \'2020 Harley Davidson Forty-Eight\', \'black\', 11299, 3, \'\')' % schema)
cursor.execute('insert into ProductsInventory (%s) values (\'B16753503\', \'2018\', \'Honda\', \'CRF300L Rally\', \'2018 Honda CRF300L Rally\', \'red\', 5999, 0, \'\')' % schema)
cursor.execute('insert into ProductsInventory (%s) values (\'B16753504\', \'2020\', \'Harley Davidson\', \'Softail Slim\', \'2020 Harley Davidson Softail Slim\', \'red\', 15999, 4, \'\')' % schema)
cursor.execute('insert into ProductsInventory (%s) values (\'B16753505\', \'2018\', \'Yamaha\', \'Star Eluder\', \'2018 Yamaha Star Eluder\', \'silver\', 22499, 2, \'\')' % schema)
cursor.execute('select * from ProductsInventory')
print(cursor.fetchall())

schema = 'ITEM_NUMBER, NAME, PRICE, QUANTITY, DESCRIPTION'
#cursor.execute('drop table PartsInventory')
#cursor.execute('create table PartsInventory(ITEM_NUMBER integer primary key autoincrement, NAME varchar(100), PRICE int, QUANTITY int)')
cursor.execute('insert into PartsInventory (%s) values (\'P26973564\', \'Shinko 777 Tires\', 153.99, 4, \'\')' % schema)
cursor.execute('insert into PartsInventory (%s) values (\'P26973565\', \'Legend Suspension REVO-A Shocks\', 924.99, 3, \'\')' % schema)
cursor.execute('insert into PartsInventory (%s) values (\'P26973566\', \'Dunlop D401 Tires\', 228.89, 4, \'\')' % schema)
cursor.execute('insert into PartsInventory (%s) values (\'P26973567\', \'EBC Double-H Sintered Front/Rear Brake Pads\', 27.18, 6, \'\')' % schema)
cursor.execute('insert into PartsInventory (%s) values (\'P26973568\', \'Twin Power high Performance AGM Battery\', 202.95, 0, \'\')' % schema)
cursor.execute('insert into PartsInventory (%s) values (\'P26973569\', \'Red Line Synthetic Motorcycle Oil\', 16.99, 7, \'\')' % schema)
cursor.execute('select * from PartsInventory')
print(cursor.fetchall())

schema = 'ITEM_NUMBER, NAME, COLOR, SIZE, PRICE, QUANTITY, DESCRIPTION'
#cursor.execute('drop table MerchandiseInventory')
#cursor.execute('create table MerchandiseInventory(ITEM_NUMBER integer primary key autoincrement, NAME varchar(100), COLOR varchar(20), SIZE varchar(10), PRICE int, QUANTITY int)')
cursor.execute('insert into MerchandiseInventory (%s) values (\'M34129345\', \'H-D Brawler Leather Jacket\', \'black\', \'M\', 450.00, 3, \'\')' % schema)
cursor.execute('insert into MerchandiseInventory (%s) values (\'M34129346\', \'Wrecking Crew Banner\', \'multi\', \'One Size\', 20.00, 5, \'\')' % schema)
cursor.execute('insert into MerchandiseInventory (%s) values (\'M34129347\', \'Yamaha Paddock Pulse Pit Shirt\', \'blue\', \'XL\', 79.99, 0, \'\')' % schema)
cursor.execute('insert into MerchandiseInventory (%s) values (\'M34129348\', \'HDMC Bottle Opener\', \'silver\', \'One Size\', 9.95, 7, \'\')' % schema)
cursor.execute('insert into MerchandiseInventory (%s) values (\'M34129349\', \'Alpinestars Andes Honda V2 Pants\', \'multi\', \'S\', 249.95, 3, \'\')' % schema)
cursor.execute('select * from MerchandiseInventory')
print(cursor.fetchall())"""

schema = 'ORDER_ID, ITEM_NUMBER, MAKE, MODEL, YEAR, NAME, COLOR, CUSTOMER_FIRST, CUSTOMER_LAST, PHONE_NUMBER, DATE, INTEREST_RATE, COMMENTS, ARCHIVED'
#cursor.execute('drop table BikeOrders')
#cursor.execute('create table BikeOrders(ORDER_ID integer primary key autoincrement, ITEM_NUMBER integer, DATE varchar(10), INTEREST_RATE int)')
cursor.execute('insert into BikeOrders (%s) values (\'B48657932\', \'B16753498\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'01/13/2021\', 10.0, \'\', 0)' % (schema))

schema = 'ORDER_ID, ITEM_NUMBER, DATE, END_DATE, CUSTOMER_FIRST, CUSTOMER_LAST, PHONE_NUMBER, MECHANIC, COMMENTS, ARCHIVED'
#cursor.execute('drop table WorkOrders')
#cursor.execute('create table WorkOrders(ORDER_ID integer primary key autoincrement, ITEM_NUMBER integer, DATE varchar(10), NAME varchar(30), PHONE varchar(10), MECHANIC varchar(20), ARCHIVED boolean)')
cursor.execute('insert into WorkOrders (%s) values (\'P64875423\', \'P26973565\', \'02/27/2021\', \'\', \'Sabrina\', \'Young\', \'2438551646\', \'Payton\', \'\', 1)' % (schema))
"""cursor.execute('insert into WorkOrders (%s) values (\'P64875424\', \'P26973567\', \'03/02/2021\', \'\', \'Tyler\', \'Flores\', \'8643561973\', \'Payton\', \'\', 0)' % (schema))

schema = 'ORDER_ID, ITEM_NUMBER, ITEM_TYPE, COLOR, SIZE, QUANTITY, DATE, COMMENTS, ARCHIVED'
#cursor.execute('drop table MerchandiseOrders')
#cursor.execute('create table MerchandiseOrders(ORDER_ID integer primary key autoincrement, ITEM_NUMBER integer, DATE varchar(10))')
cursor.execute('insert into MerchandiseOrders (%s) values (\'M97531024\', \'M34129348\', \'\', \'\', \'\', 1, \'02/25/2021\', \'\', 1)' % (schema))"""

cursor.execute('select * from ProductsInventory')
print(cursor.fetchall())
cursor.execute('select * from PartsInventory')
print(cursor.fetchall())
cursor.execute('select * from MerchandiseInventory')
print(cursor.fetchall())

cursor.execute('select * from BikeOrders')
print(cursor.fetchall())
cursor.execute('select * from BikeOrders')
print(cursor.fetchall())
cursor.execute('select * from BikeOrders')
print(cursor.fetchall())

cursor.execute('select name from sqlite_master where type=\'table\'')
print(cursor.fetchall())

con.commit()
cursor.close()
con.close()