1import mysql.connector


######
# how to connect without database selected, then create database

#####


class connection:
    create_databse = 'CREATE DATABASE IF NOT EXISTS VENDING_MACHINE;'
    select = 'SELECT * FROM DATABASE'
    check = 0
    database = 'VENDING_MACHINE'

    def __init__(self):
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
        
            self.cursors  = self.db.cursor()
            self.cursors.execute(self.create_databse)
            print('[+] successfully created database')
            # self.check = 0  

            self.createTable = "CREATE TABLE IF NOT EXISTS items (itemid INT AUTO_INCREMENT PRIMARY KEY, name varchar(20), price INT(5), quantity int )"
            self.tables = self.db.cursor()
            self.tables.execute(self.createTable)
            print('[+] Tables creation successful')
            
    def insert(self):
        self.sql = 'INSERT INTO items (name , price, quantity) VALUES (%s, %s, %s)'
        values = [
            ('coca cola', '20','10'),
            ('Pepsi', '25','20'),
            ('chocolate', '15','40'),
            ('crips', '5','12'),
            
        ]

        self.insert = self.db.cursor()
        self.insert.executemany(self.sql, values)
        self.db.commit()
        print('[+] items added to table')
    
    def show_items(self):
        self.show_items_sql = 'SELECT * FROM items;'
        self.cursors.execute(self.show_items_sql)
        result = self.cursors.fetchall()

        # # mycursor = self.db.cursor()

        # self.cursors.execute('select * from items')
        # result = self.cursors.fetchall()
        

        return result 
    
    def truncate(self):
        self.truncate_sql = 'truncate table items;'
        self.cursors.execute(self.truncate_sql)
        result = self.cursors.fetchall()
        print('[+] table truncated')

        return result 
    def select(self, message):
        self.select_items_sql = 'SELECT itemid, name, price FROM items where itemid = {} '.format(int(message))
        self.cursors.execute(self.select_items_sql)
        result = self.cursors.fetchall()
        
        return result 
    
   
# test = connection()
# test.connect()
# test.database_setup()
# test.show_database()
# test.create_table()
# test.insert_items()
# test.connect()


        
