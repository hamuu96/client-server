import mysql.connector
import create_database


######
# change database 

#####

class connection:
    #global variables
    test = create_database.createdb()
    create_databse = 'CREATE DATABASE IF NOT EXISTS VENDING_MACHINE;'
    select = 'SELECT * FROM DATABASE' 
    check = 0
    database = 'VENDING_MACHINE' #database name
    no_of_database_items = 50 #no of database items

  

    def __init__(self):
        #connection to database
        self.db = mysql.connector.connect(
            host='localhost',
            username = 'root',
            password = '802700',
            database = self.database
        )
        if self.db :
            print('[+] successfull connecting to the database')
            # self.db.database = 'VENDING_MACHINE'
            self.check = 1
        
            self.cursors  = self.db.cursor() #cursor object creation, used to execute mysql commands
            self.cursors.execute(self.create_databse) #sql command execution
            print('[+] successfully created database')

            self.createTable = "CREATE TABLE IF NOT EXISTS items (itemid INT AUTO_INCREMENT PRIMARY KEY, name varchar(20), price INT(5), quantity int )"
            self.tables = self.db.cursor() #cursor object creation, used to execute mysql commands
            self.tables.execute(self.createTable)
            print('[+] Tables creation successful')
    
    #insert items in database
    def insert(self):
        self.sql = 'INSERT INTO items (name , price, quantity) VALUES (%s, %s, %s)'
        values = [
            ('Coca cola','20','{}'.format(self.no_of_database_items)),
            ('   Pepsi ','25','{}'.format(self.no_of_database_items)),
            ( 'Mask','     15','{}'.format(self.no_of_database_items)),
            (' Seven up','5','{}'.format(self.no_of_database_items)),
            ('Ice cream','5','{}'.format(self.no_of_database_items)),
            (' Chips','   5','{}'.format(self.no_of_database_items)),
            (' Water','   5','{}'.format(self.no_of_database_items)),
            (' Kitkat','  5','{}'.format(self.no_of_database_items)),
            (' Oreo','    5','{}'.format(self.no_of_database_items))
            
        ]

        self.insert = self.db.cursor()
        self.insert.executemany(self.sql, values)
        self.db.commit()
        print('[+] items added to table')
    
    #
    def show_items(self):
        self.show_items_sql = 'SELECT * FROM items;'
        self.cursors.execute(self.show_items_sql)
        database_items = self.cursors.fetchall()
        return database_items
 
    
    def truncate(self):
        self.truncate_sql = 'truncate table items;'
        self.cursors.execute(self.truncate_sql)
        delete_table = self.cursors.fetchall()
        print('[+] table truncated')

        return delete_table 
    def select(self, message):
        self.select_items_sql = 'SELECT itemid, name, price FROM items where itemid = {} '.format(int(message))
        self.cursors.execute(self.select_items_sql)
        seleted_items = self.cursors.fetchall()
        
        return seleted_items 
    def update_table(self,items):
        keys = list(items.keys())
        # print(len(keys)Q
        for i in range(1,len(keys)+len(keys)):
            if str(i) not in keys:
                continue
            remaining_total = self.no_of_database_items - int(items[str(i)])
            self.update_sql = "UPDATE items SET quantity = {} WHERE itemid = {}".format(remaining_total,i)
            self.cursors.execute(self.update_sql)
            self.db.commit()
            # print("updated quantity to  = {} where  itemid = {}".format(remaining_total,i))

    
   


        
