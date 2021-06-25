import socket


class client:
    def __init__(self) -> None:
        FORMAT = 'utf-8'

        #create socket instance
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        add = socket.gethostbyname(socket.gethostname())
        port = 8081
        SELECTION = ''
        #connect to address 
        client.connect((add, port))
        #receive data

        #send data
        print('\n[+] Click Y if you would like to go to use the vending machine\n[+] Q to exit\n[+] press "C or c or checkout" Checkout\n[+] press V or View to view cart ')
        while True:
            try:
                message = input('->: ') #get user input

                if message.lower() != 'q' or 'Q' or 'quit': #exit if one of this input is entered
                    if message.lower() == 'v' or message == 'V' or message.lower() == 'view':  #if v is pressed view cart
                        client.send(bytes(message, FORMAT))  #send user input
                        message = client.recv(1028)     #receive data from server
                        test = eval(message.decode(FORMAT))  #determine what data is send from server , in this case server returns list "cart items" 
                        self.shopping_bag = test
                        
                        print('\n[+] items in shopping bag:')
                        #iterate through list and print items in cart
                        for i in self.shopping_bag: #
                            print(i)
                        

                    else:
                        #receive data from server and decode to string
                        client.send(bytes(message, FORMAT))
                        message = client.recv(1028)
                        print(message.decode(FORMAT))

                else:
                    client.close()
                    exit()
            except ConnectionAbortedError:
                print("Application closed")
                break
def main():
    test = client()

if __name__ == '__main__':
    main()