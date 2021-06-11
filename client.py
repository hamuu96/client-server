import socket

FORMAT = 'utf-8'

#create socket instance
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
add = socket.gethostbyname(socket.gethostname())
port = 8081
buffer = b''
#connect to address 
client.connect((add, port))
#receive data

#send data
print('[+] Click Y if you would like to go to use the vending machine or Q to exit ')
while True:
    message = input('->: ')

    if message != 'Q':
        client.send(bytes(message, FORMAT))

        message = client.recv(1028)
        print(message.decode(FORMAT))

    else:
        client.close()
        print('Thank you!')
        break