import mysql.connector


class createdb:
    def __init__(self):
        #change database credentials to match your mysql login creds
        db = mysql.connector.connect(
                    host='localhost',
                    username = 'root',
                    password = '802700',
                    database = None
                )

        executor = db.cursor()
        sql = 'create  database if not exists vending_machine'
        executor.execute(sql)
