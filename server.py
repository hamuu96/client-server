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

    db = database.connection()
    db.truncate()
    db.insert()

    #handle connections
    def handle(self,conn, addr):
        print('connection established from {}'.format(addr))

        connection = True
        while connection:
            #receive data from client but not decoded
            recv = conn.recv(4096)

            if recv :
                self.received_msg = recv.decode(self.FORMAT)
                if self.received_msg =="Y":
                    conn.send(b'Welcome to the vending machine. \npress any key to continue: ')
                    # conn.sendall(b"'itemid', 'item', 'price', 'Quantity'\n")
                    conn.sendall(str([ self.display(conn)]).encode())
                    # self.display(conn)
                    conn.send(b'\nHere are the menu items \n')
                    conn.send(b'\nPlease select an item you would like to buy:')
                    conn.send(b'\n')
                    items = []
                if self.received_msg.isdigit():
                    purchased_items = self.insert_cart(conn)
                    items.append(purchased_items)
                    continue
                else:
                    if self.received_msg == 'Q':
                        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
                        connection = False
                        conn.send(b'[+] Thank you see you next time')
                    print(f'{addr} : {self.received_msg} ' )
                    conn.send(str(items).encode())
                    conn.send("\nMsg received".encode(self.FORMAT))
                    
        conn.close()
        
    def display(self,conn):
        #send data
        # result = self.db.show_items()
        items = self.db.show_items()
      
        results = [x for x in items]
        #iterate through items in selected table
        
        values = [''.join(str(items[i])) for i in range(len(items))]
        printable_items = [ values[_] for _ in range(len(values))]
        
        for i in values:
            conn.send(str(i+'\n').encode())

        # for i in range(len(result)):
        #     conn.send(str(('id: ', result[i][0],'name: ', result[i][1] ,' price:',result[i][2],'quantity: ', result[i][3] )).encode())
            # print('id: ', result[i][0],'name: ', result[i][1] ,' price:',result[i][2],'quantity: ', result[i][3] )
        # conn.send(b'\n[+] item added to shopping bag.\n')
        # conn.send(b'\nPlease select an item you would like to buy: \n')
        # for i in result:
    
        #     print(i)
    def insert_cart(self, conn):
        result  = self.db.select(self.received_msg)
        conn.send(str('{}\nitem added to cart'.format(result)).encode())

        return result
        
        # conn.send(b'\nitem added to bag')

   
        
        

    def start(self):
    
        #listen for connections
        self.server.listen()
        print(f'[+] server is listening on {self.add, self.port}')
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
