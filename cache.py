from socket import *
import tcp_transport
import snw_transport
import os
import time
import sys
if __name__ == "__main__":
    cachePort = int(sys.argv[1])  # Retrieve the cache port number as a command-line argument
    cacheSocket_tcp = socket(AF_INET,SOCK_STREAM)# Create a TCP socket for cache communication
    cacheSocket_udp = socket(AF_INET,SOCK_DGRAM) # Create a UDP socket for cache communication
    cacheSocket_tcp.bind(('localhost',cachePort))# Bind the TCP socket to the localhost and the specified cachePort
    cacheSocket_udp.bind(('localhost',(cachePort+1)))
    cacheSocket_udp1=socket(AF_INET,SOCK_DGRAM)# Create UDP socket 
    cacheSocket_tcp.listen(1)
    print('cache is Listening')

    while True:                   # Accept an incoming TCP connection and get the connection socket and address
        connectionSocket, addr = cacheSocket_tcp.accept()
        print("connection accepted")
        if(sys.argv[4]=='tcp'):
            sentence = connectionSocket.recv(1024).decode() # Receive data from the TCP connection  and decode it
        else:
            dat,client_address=cacheSocket_udp.recvfrom(1024) # Receive data from the UDP socket and get the client address
            sentence=dat.decode()

        
        cmd=sentence[:3]
        file_name=sentence[4:]
        base_path=r'C:\Users\saket\Downloads\SakethFinal-1\SakethFinal\cache_files'
        file_path=os.path.join(base_path,file_name)
        if(cmd=='get'):
            if os.path.exists(file_path):
                print(f"The file '{file_name}' exists in the current directory.")
                if(sys.argv[4]=='tcp'):
                    tcp_transport.send_file(file_path,connectionSocket)
                    time.sleep(2) # Wait for 2 seconds 
                    s="File delivered from Cache"
                    connectionSocket.send(s.encode())  # Send the message to the connected client by encoding it to bytes
                    connectionSocket.close()
                else:
                    snw_transport.send_file(file_path,cacheSocket_udp,client_address[0],client_address[1])
                    time.sleep(2) #wait for 2 seconds
                    s="File delivered from Cache"
                    connectionSocket.send(s.encode())
                    connectionSocket.close()


                

            else:                 # Check if the file at 'file_path' does not exist in the current directory
                print(f"The file '{file_name}' does not exist in the current directory.")
                to_server=socket(AF_INET, SOCK_STREAM)
                #to_server.bind(('localhost',cachePort))
                serverName = sys.argv[2]   # Get the server name from sys.argv[2] and the server port from sys.argv[3]
                serverPort = int(sys.argv[3])
                to_server.connect((serverName,serverPort))    # Establish a connection to the server using the serverName and serverPort
                if(sys.argv[4]=='tcp'):
                    to_server.send(sentence.encode())
                else:
                    cacheSocket_udp1.sendto(sentence.encode(),(serverName,serverPort))
                    
                time.sleep(1)
                if(sys.argv[4]=='tcp'):
                    tcp_transport.receive_file(file_path,to_server) # If the protocol is TCP, receive a file from the server and store it at 'file_path'
                    #time.sleep(1)
                    to_server.close()
                    tcp_transport.send_file(file_path,connectionSocket)
                    time.sleep(2)
                    connectionSocket.send("sent from server".encode())   # Send a message to the connected client to indicate file transfer completion
                    connectionSocket.close()
                else:
                    
                    snw_transport.receive_file(file_path,cacheSocket_udp1,serverName,serverPort)  # If the protocol is not TCP, assume it's UDP, and receive a file using Udp socket
                    time.sleep(2)
                    to_server.close()
                    snw_transport.send_file(file_path,cacheSocket_udp,client_address[0],client_address[1])
                    time.sleep(2)
                    connectionSocket.send("sent from server".encode())
                    connectionSocket.close()  # Close the connection to the client

                

          
    


