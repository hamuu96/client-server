import socket
import threading
from collections import Counter
from mysql.connector import connect
import database


####issues###
# view items does not change 
#issue with quit 
#########
class server:
    #global variables
    items =[]
    check = items
    user_choice = []
    FORMAT = 'utf-8'

    #create server socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #bind address and port 
    add = socket.gethostbyname(socket.gethostname())
    port = 8081
    ADDRESS = (add, port) #tuple containing address and port
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
            try:
                #receive data from client but not decoded
                recv = conn.recv(4096)
                #if message received
                if recv :
                    #decode message
                    self.received_msg = recv.decode(self.FORMAT)
                    terminate = self.menu(conn,self.received_msg)
                    if terminate == False:
                        connection = False
                else:
                    continue
                
            except ConnectionResetError or ConnectionAbortedError: 
                print('Host closed the connection')
                break
        conn.close()
    def menu(self,conn,message):
        
        checkout = ['c','checkout']
        exit = ['Q', 'q', 'quit']
        # selection = message.replace(' ','') #remove any spaces in message
        selection = message #remove any spaces in 
        #check if user pressed y to con
        if selection.lower() == 'y':
            try:
                conn.send(b'\n[+] vending machine items\n[+] press Enter key to display items\n')
                conn.sendall(str([ self.display(conn)]).encode())
            except TypeError:
                return False
        #check if user input is a digit , insert items to client shopping bag 
        elif selection.isdigit():
            try:
                #check if items selected is not in menu
                if int(selection) > len(self.database_items):
                    conn.send(b'\n[+] Please select items in the menu please!')
                else:
                    self.user_choice.append(selection)
                    purchased_items = self.insert_cart(conn) #return value from insert cart function
                    self.items.append(purchased_items) #list with user data
                    self.check +self.items #update the cart with each user insert
                    #list of user choices
                    self.user_cunter = Counter(self.user_choice) #check how many times an items has been selected
            except AttributeError:
                conn.send(b'[+] Press Y to interact with vending machine!')
        
        #view items in client shopping cart
        elif selection.lower() == 'v' or selection.lower() == 'view':
            self._view_Purchased_items(conn,self.check)  #execution of view cart function

        #allow user to checkout and pay
        elif selection.lower() in checkout: #check if user input is in checkout list (contains certain key words)
            conn.send(b'\n[+] proceeding to checkout...\n[+] please enter "credit card number", "Full Name", "Card CCV", "Date of Expiration"\n')
        #check if user entered all specified information during checkout
        elif len(selection) >=5:  
            #list of user information and card data
            card_info = selection.split() #split the user input into a list 
            #check if all the required information is entered
            if len(card_info) != 5: 
                conn.send(b'please fill the card information properly\n[+] please enter "credit card number", "Full Name", "Card CCV", "Date of Expiration"\n')
            else:
                Total_price = 0
                #add total of all items in cart 
                for i in range(len(self.items)): 
                    Total_price+=self.items[i][0][2] #add price of items in the cart

                # conn.send(str('\n[+] card information: {}\n[+] Items in Bag:{}\n[+] Total price: {}\n'.format(card_info, self.items,Total_price)).encode())
                conn.send(str('\n[+] card information: {}\n[+] Items in Bag:{}\n[+] Total price: {}\n\n[+] To continue shopping press Y or y '.format(card_info, self.items,Total_price)).encode())
                self.db.update_table(self.user_cunter)  #update database after user checks out
                
                #save every transaction in a text file 
                with open ('transactions.txt', 'a') as f:
                    f.write('\n[+] card information: {}\n[+] Items in Bag:{}\n[+] Total price: {}\n '.format(card_info, self.items,Total_price))
                #after every transaction cart, user_choices are reset to 0
                self.items = []
                self.user_choice = []
                self.user_cunter  = {}
                # return False
        #exit if user input is Q
        elif selection in exit:
                conn.send(b'\n[+]Connection to server closed\n[+]Thank you for shopping with us, sorry we could not help you with what you needed!\n[+]Press Q or q to exit application')
                return False
        #send user statement if they enter values other than the ones specified
        else:
            conn.send(b'[+] wrong input!')

    #display database table items
    def display(self,conn):
        self.database_items = self.db.show_items() #execution of show items method
        values = [''.join(str(self.database_items[i])) for i in range(len(self.database_items))]
        conn.send(b'\n[+]To buy item press itemID to add to cart\n\nItemID  Name   Price  Quantity\n')
        #iterate through each item in database and print as a menu
        for i in values:
            conn.send(str(i+'\n').encode())
    #insert item to cart based on user selection
    def insert_cart(self, conn):
        result  = self.db.select(self.received_msg) #select item from database 
        conn.send(str('{}\nitem added to cart'.format(result)).encode())
        return result
    #gather user payment infomation for checkout
    def checkout(self,conn, customer_data):
        #ask for name
        conn.send(b'\nThank you..proceeding to checkout\nplease enter your name,\tcredit card number , account no , ccv number and expiration date: ')
        customer = []
        customer.append(customer_data.split()) #add user information to list
        return customer
    def _view_Purchased_items(self,conn,purchased_items):
        conn.send(str(purchased_items).encode())
        purchased_items = []


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
    test = server()
    test.start()
