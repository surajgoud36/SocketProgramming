import socket
import os
def send_f():
    print("hello Mastary")
def start_server():
    serverPort = 12000
    serverSocket_tcp = socket.socket(socket.AF_INET,socket.SOCK_STREAM)# Create a TCP socket for the server
    serverSocket_tcp.bind(('localhost',serverPort))
    serverSocket_tcp.listen(1)
    print('Server is Listening')

def send_file(file_path,Ssocket,host,port):# Function to send a file over a socket
    size=os.path.getsize(file_path)
    result="LEN:"+str(size)
    Ssocket.sendto(result.encode(),(host,port))

    with open(file_path,'rb') as file:
        data=file.read(1024)
        
        while data:
            #print(data)
            Ssocket.sendto(data,(host,port))
            Ssocket.settimeout(2)
            try:
                data,server_address=Ssocket.recvfrom(1024)
                #if(data.decode()=='ACK'):
                    #print("")
            except socket.timeout:
                print("Did not receive ACK terminating")
                break
            data=file.read(1024)
        Ssocket.sendto("FIN".encode(),(host,port))
    


def receive_file(file_path,rsocket,host,port):# Function to receive a file over a socket
    data, client_address = rsocket.recvfrom(1024) #len
    #print(f"Received data from {client_address}: {data.decode()}")
    with open(file_path,'wb') as file:
        rsocket.settimeout(2)
        try:

            data, client_address = rsocket.recvfrom(1024)
            while True:
                file.write(data)   # Write received data to the file
                response="ACK"
                rsocket.sendto(response.encode(),client_address)
                rsocket.settimeout(1)
                try:
                    data, client_address = rsocket.recvfrom(1024)
                    if(data.decode()=='FIN'):
                        break
                except socket.timeout:
                    print("Data Transmission terminated Prematurely")
                    break   


        except socket.timeout:
            print("Did not receive data terminataing")

       
