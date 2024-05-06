from socket import *
def send_f():
    print("hello Mastary")
def start_server():# Function to start the server
    serverPort = 12000
    serverSocket_tcp = socket(AF_INET,SOCK_STREAM)
    serverSocket_tcp.bind(('localhost',serverPort))
    serverSocket_tcp.listen(1)
    print('Server is Listening')

def send_file(file_path,rsocket):# Function to send a file over a socket
    with open(file_path,'rb') as file:# Open the file for reading in binary mode
        data=file.read(1024)
        while data:
            #print(data)
            rsocket.send(data)
            data=file.read(1024)

def receive_file(file_path,rsocket):# Function to receive a file over a socket
    with open(file_path,'wb') as file:
        data= rsocket.recv(1024)
        while data:
            decoded_data= data.decode('utf-8')
            #print(decoded_data)
            if(decoded_data=='sent from server'or decoded_data=='File delivered from Cache'):
                print(decoded_data)
                break
            file.write(data) # Write the received data to the file
            data=rsocket.recv(1024)
            
    print("File reception over")
