import socket
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext



class client:
    FORMAT = 'utf-8'
    def __init__(self,master = None) -> None:
        self.master = master

        #frame
        self.top_frame = LabelFrame(master,text='Display', padx=20,pady=20)
        self.bottom_frame = LabelFrame(master, text='user input',padx=20,pady=20,width=50)

        #frame customization 
        self.top_frame.pack(padx=10,pady=10)
        self.bottom_frame.pack(padx=10,pady=10)

        #widgets
        self.text_display = scrolledtext.ScrolledText(self.top_frame,width=95,height=30)
        self.text_display.pack()

        self.user_input = Entry(self.bottom_frame,width=40 )
        self.send = Button(self.bottom_frame,text='Send',command=self.send_data)

        self.user_input.grid(column=0,row=0)
        self.send.grid(column=1,row=0,padx=15)

        self.user_input.bind('<Return>',self.send_data)
       

        #create socket instance
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        add = socket.gethostbyname(socket.gethostname())
        port = 8081
        SELECTION = ''
        #connect to address 
        self.client.connect((add, port))
        #receive data

        #send data
        welcome = '\n[+] Click Y if you would like to go to use the vending machine\n[+] Q to exit\n[+] press "C or c or checkout" Checkout\n[+] press V or View to view cart\n '
        self.text_display.insert('1.0',welcome)
       
        
    def send_data(self,event=None):
        self.message = self.user_input.get() #get user input
        self.user_input.delete(0,END)
        
        try:

            if self.message.lower() != 'q' or 'Q' or 'quit': #exit if one of this input is entered
                if self.message.lower() == 'v' or self.message == 'V' or self.message.lower() == 'view':  #if v is pressed view cart
                        #send user input
                    self.message = self.client.send(bytes(self.message, self.FORMAT))
                    self.recived_msg = self.client.recv(1028)     #receive data from server
                    test = eval(self.recived_msg.decode(self.FORMAT))  #determine what data is send from server , in this case server returns list "cart items" 
                    self.shopping_bag = test
                    
                    self.text_display.insert(END,'\n[+] items in shopping bag:')
                    #iterate through list and print items in cart
                    for i in self.shopping_bag: #
                        self.text_display.insert(END,'\n'+str(i))
                    
                    self.shopping_bag = []
                    self.test = []
                else:
                    #receive data from server and decode to string
                    self.message = self.client.send(bytes(self.message, self.FORMAT))
                    self.text_display.insert(END,self.client.recv(1028).decode(self.FORMAT)+'\n')
                    # print(message.decode(FORMAT))

            else:

                client.close()
                self.master.destroy()
        except ConnectionAbortedError:
            print("Application closed")

def main():
    window = Tk()
    window.title('Vending machine')
    window.resizable(0,0)
    test = client(window)
    window.mainloop()
   

if __name__ == '__main__':
    main()


   