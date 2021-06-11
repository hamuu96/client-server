import socket
import threading

# from mysql.connector.cursor import RE_SQL_ON_DUPLICATE

import database


####issues###
# connection not clossing after user exits
# issue with database connecting when using wsl
#########
class server:

    FORMAT = 'utf-8'
    #create server socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #bind address and port 
    add = socket.gethostbyname(socket.gethostname())
    port = 8081

    ADDRESS = (add, port)
    server.bind(ADDRESS)

    #instantiating database class
    db = database.connection()
    #delete table items for each user before inserting items to database...prevent multiple insertion of items to database
    db.truncate()
    #insert items to database
    db.insert()

    #handle connections
    def handle(self,conn, addr):
        print('connection established from {}'.format(addr))

        connection = True
        while connection:
            #receive data from client but not decoded
            recv = conn.recv(4096)
            #if message received
            if recv :
                #decode message
                self.received_msg = recv.decode(self.FORMAT)
                self.menu(conn,self.received_msg)
                # continue
                
                


                
                    
        conn.close()
    
    def menu(self,conn,message):
        items = []
        checkout = ['c','checkout']
        selection = message
        if selection.lower() == 'y':
            conn.send(b'[+] vending machine items\n[+] press any key to display items\n')
            conn.sendall(str([ self.display(conn)]).encode())
        elif selection.isdigit():
            purchased_items = self.insert_cart(conn)
            items.append(purchased_items)
        elif selection.lower() in checkout:
            conn.send(b'[+] proceeding to checkout...\n[+] please enter "credit card number", "Full Name", "Card CCV", "Date of Expiration"\n')
            print(selection)
        elif len(selection) >=5:
            card_info = selection.split()
            print(card_info)
            if len(card_info) != 5:
                conn.send(b'please fill the card information properly\n[+] please enter "credit card number", "Full Name", "Card CCV", "Date of Expiration"\n')
            else:
                conn.send(str(card_info).format(self.FORMAT).encode())

            
    #display database table items
    def display(self,conn):
        items = self.db.show_items()
        values = [''.join(str(items[i])) for i in range(len(items))]
        conn.send(b'ItemID  Name   Price  Quantity\n')
        for i in values:
            conn.send(str(i+'\n').encode())
    #insert selected items to shopping cart
    def insert_cart(self, conn):
        result  = self.db.select(self.received_msg)
        conn.send(str('{}\nitem added to cart'.format(result)).encode())
        return result
    #gather user payment infomation for checkout
    def checkout(self,conn, customer_data):
        #ask for name
        conn.send(b'\nThank you..proceeding to checkout\nplease enter your name,\tcredit card number , account no , ccv number and expiration date: ')
        customer = []
        customer.append(customer_data.split())
        return customer
    def start(self):
    
        #listen for connections
        self.server.listen()
        print(f'[+] server is listening on {self.add, self.port}')
        #allow multiple user connections
        while True:
            #accept connections
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
        
        
    
           


if __name__ == "__main__":
    # conn, add = start()
    test = server()
    test.start()
    # handle(conn, add)
