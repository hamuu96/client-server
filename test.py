import mysql.connector


######
# how to connect without database selected, then create database

#####


db = mysql.connector.connect(
    host='localhost',
    username = 'root',
    password = '802700',
    database = 'vending_machine'
)

mycursor = db.cursor()
mycursor.execute('select * from items')
result = mycursor.fetchall()
for i in range(len(result)):
    print('id: ', result[i][0],'name: ', result[i][1] ,' price:',result[i][2],'quantity: ', result[i][3])

        
