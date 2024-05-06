from socket import *
import tcp_transport
import snw_transport
import time
import sys
import os
if __name__ == "__main__":
    serverPort = int(sys.argv[1])
    serverSocket_tcp = socket(AF_INET,SOCK_STREAM) # Create a TCP socket for the server
    serverSocket_udp=socket(AF_INET,SOCK_DGRAM)     
    serverSocket_tcp.bind(('169.226.225.155',serverPort))
    serverSocket_udp.bind(('169.226.225.155',serverPort))
    serverSocket_tcp.listen(1)
    print('Server is Listening')# Print a message to indicate that the server is now listening

    while True:
        connectionSocket, addr = serverSocket_tcp.accept() # Accept an incoming TCP connection and get the connection socket and address
        print("connection accepted")
        if(sys.argv[2]=='tcp'):
            sentence = connectionSocket.recv(1024).decode()
        else:
            dat, client_address = serverSocket_udp.recvfrom(1024)
            sentence=dat.decode()

        
        
        cmd=sentence[:3]
        file_name=sentence[4:]
        base_path=r'r'/home1/s/s/sv926877/CCNP/server_files/'
        file_path=os.path.join(base_path,file_name)
        if(cmd=='put'):
            print("server is in accepting mode")
            if(sys.argv[2]=='tcp'):
                tcp_transport.receive_file(file_path,connectionSocket) # If it's TCP, receive a file from the client and store it at 'file_path'
            #time.sleep(1)
                time.sleep(2)
                connectionSocket.send("File successfully uploaded".encode()) # Send a message to the client to indicate that the file is successfully uploaded
                connectionSocket.close()
            else:
                snw_transport.receive_file(file_path,serverSocket_udp,client_address[0],client_address[1])
                time.sleep(2)
                connectionSocket.send("File successfully uploaded".encode())
                connectionSocket.close() # Close the connection socket
            
            
        else:
            print("server is in delivering mode")
            if(sys.argv[2]=='tcp'):
                 tcp_transport.send_file(file_path,connectionSocket)
                 time.sleep(2)
                 connectionSocket.send("sent from server".encode())
                 connectionSocket.close()
            else:
                snw_transport.send_file(file_path,serverSocket_udp,client_address[0],client_address[1])
                #time.sleep(2)
                #connectionSocket.send("sent from server".encode())
                connectionSocket.close()