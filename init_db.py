import sqlite3
con = sqlite3.connect('database.db')
cursor = con.cursor()

schema = 'NAME, COLOR, PRICE, QUANTITY'
cursor.execute('drop table ProductsInventory')
cursor.execute('create table ProductsInventory(ITEM_NUMBER integer primary key autoincrement, NAME varchar(100), COLOR varchar(20), PRICE int, QUANTITY int)')
cursor.execute('insert into ProductsInventory (ITEM_NUMBER, %s) values (16753495, \'2021 Yamaha Star Venture\', \'white\', 26999, 4)' % schema)
cursor.execute('insert into ProductsInventory (%s) values (\'2021 Harley Davidson Low Rider S\', \'black\', 17999, 4)' % schema)
cursor.execute('insert into ProductsInventory (%s) values (\'2020 Yamaha Tracer 900 GT\', \'black\', 12999, 3)' % schema)
cursor.execute('insert into ProductsInventory (%s) values (\'2019 Honda Gold Wing Tour\', \'red\', 28300, 2)' % schema)
cursor.execute('insert into ProductsInventory (%s) values (\'2021 Yamaha FJR1300ES\', \'blue\', 17999, 6)' % schema)
cursor.execute('insert into ProductsInventory (%s) values (\'2021 Harley Davidson Livewire\', \'black\', 29799, 6)' % schema)
cursor.execute('insert into ProductsInventory (%s) values (\'2019 Honda Rebel 500\', \'black\', 4599, 3)' % schema)
cursor.execute('insert into ProductsInventory (%s) values (\'2020 Harley Davidson Forty-Eight\', \'black\', 11299, 3)' % schema)
cursor.execute('insert into ProductsInventory (%s) values (\'2018 Honda CRF300L Rally\', \'red\', 5999, 0)' % schema)
cursor.execute('insert into ProductsInventory (%s) values (\'2020 Harley Davidson Softail Slim\', \'red\', 15999, 4)' % schema)
cursor.execute('insert into ProductsInventory (%s) values (\'2018 Yamaha Star Eluder\', \'silver\', 22499, 2)' % schema)
cursor.execute('select * from ProductsInventory')
print(cursor.fetchall())

schema = 'NAME, PRICE, QUANTITY'
cursor.execute('drop table PartsInventory')
cursor.execute('create table PartsInventory(ITEM_NUMBER integer primary key autoincrement, NAME varchar(100), PRICE int, QUANTITY int)')
cursor.execute('insert into PartsInventory (ITEM_NUMBER, %s) values (26973564, \'Shinko 777 Tires\', 153.99, 4)' % schema)
cursor.execute('insert into PartsInventory (%s) values (\'Legend Suspension REVO-A Shocks\', 924.99, 3)' % schema)
cursor.execute('insert into PartsInventory (%s) values (\'Dunlop D401 Tires\', 228.89, 4)' % schema)
cursor.execute('insert into PartsInventory (%s) values (\'EBC Double-H Sintered Front/Rear Brake Pads\', 27.18, 6)' % schema)
cursor.execute('insert into PartsInventory (%s) values (\'Twin Power high Performance AGM Battery\', 202.95, 0)' % schema)
cursor.execute('insert into PartsInventory (%s) values (\'Red Line Synthetic Motorcycle Oil\', 16.99, 7)' % schema)
cursor.execute('select * from PartsInventory')
print(cursor.fetchall())

schema = 'NAME, COLOR, SIZE, PRICE, QUANTITY'
cursor.execute('drop table MerchandiseInventory')
cursor.execute('create table MerchandiseInventory(ITEM_NUMBER integer primary key autoincrement, NAME varchar(100), COLOR varchar(20), SIZE varchar(10), PRICE int, QUANTITY int)')
cursor.execute('insert into MerchandiseInventory (ITEM_NUMBER, %s) values (34129345, \'H-D Brawler Leather Jacket\', \'black\', \'M\', 450.00, 3)' % schema)
cursor.execute('insert into MerchandiseInventory (%s) values (\'Wrecking Crew Banner\', \'multi\', \'One Size\', 20.00, 5)' % schema)
cursor.execute('insert into MerchandiseInventory (%s) values (\'Yamaha Paddock Pulse Pit Shirt\', \'blue\', \'XL\', 79.99, 0)' % schema)
cursor.execute('insert into MerchandiseInventory (%s) values (\'HDMC Bottle Opener\', \'silver\', \'One Size\', 9.95, 7)' % schema)
cursor.execute('insert into MerchandiseInventory (%s) values (\'Alpinestars Andes Honda V2 Pants\', \'multi\', \'S\', 249.95, 3)' % schema)
cursor.execute('select * from MerchandiseInventory')
print(cursor.fetchall())

cursor.execute('drop table BikeOrders')
cursor.execute('create table BikeOrders(ORDER_ID integer primary key autoincrement, ITEM_NUMBER integer, DATE varchar(10), INTEREST_RATE int)')

cursor.execute('drop table WorkOrders')
cursor.execute('create table WorkOrders(ORDER_ID integer primary key autoincrement, ITEM_NUMBER integer, DATE varchar(10), NAME varchar(30), PHONE varchar(10), MECHANIC varchar(20), ARCHIVED boolean)')

cursor.execute('drop table MerchandiseOrders')
cursor.execute('create table MerchandiseOrders(ORDER_ID integer primary key autoincrement, ITEM_NUMBER integer, DATE varchar(10))')

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