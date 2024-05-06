import tcp_transport
import snw_transport
import socket
import time
import sys
import os
if __name__ == "__main__":
   
    nfile="put abcd.txt"
    serverName = sys.argv[1] 
    serverPort = int(sys.argv[2])
    cacheIp= sys.argv[3]
    cachePort=int(sys.argv[4])
    clientSocket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a TCP socket for the client
    clientSocket_udp= socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # Create a UDP socket for the client
    #clientSocket_udp.bind(('localhost',21104))
    #clientSocket_tcp.bind(('localhost',21104))
    command = input('Enter Command ')  # Get the user's input for a command
    while True:
        if(command=='quit'):
            print('Exiting Program')
            break
        cmd=command[:3]    # Extract the command and file name from the user's input
        file_name=command[4:]
        base_path=r'C:\Users\saket\Downloads\SakethFinal-1\SakethFinal\client_files'
        file_path=os.path.join(base_path,file_name)
        if(cmd=='get'and sys.argv[5]=='tcp'):
            clientSocket_tcp.connect((cacheIp,cachePort))
            clientSocket_tcp.send(command.encode()) # Send the user's command to the cache
            time.sleep(1)
            tcp_transport.receive_file(file_path,clientSocket_tcp) # Receive a file from the cache and store it at 'file_path'
            #s=clientSocket_tcp.recv(1024).decode()
            #print(s)
        elif(cmd=='put' and sys.argv[5]=='tcp'):
            clientSocket_tcp.connect((serverName,serverPort))
            clientSocket_tcp.send(command.encode())  # Send the user's command to the server
            time.sleep(1)
            tcp_transport.send_file(file_path,clientSocket_tcp)
            time.sleep(2)
            clientSocket_tcp.send("sent from server".encode())
            #time.sleep(1)
            s=clientSocket_tcp.recv(1024).decode()   # Receive a response from the server
            print(s)
        elif(cmd=='get' and sys.argv[5]=='snw'):
            clientSocket_tcp.connect((cacheIp,cachePort))
           # clientSocket_tcp.send(command.encode())
            clientSocket_udp.sendto(command.encode(),(cacheIp,(cachePort+1)))   # Send the user's command to the cache using UDP
            time.sleep(1)
            snw_transport.receive_file(file_path,clientSocket_udp,cacheIp,cachePort)
            time.sleep(2)
            message=clientSocket_tcp.recv(1024).decode()
            print(message)
        else:
            clientSocket_tcp.connect((serverName,serverPort))
           # clientSocket_tcp.send(command.encode())
            clientSocket_udp.sendto(command.encode(),(serverName,serverPort))    # Send the user's command to the server using UDP
            time.sleep(1)
            snw_transport.send_file(file_path,clientSocket_udp,serverName,serverPort)
            message=clientSocket_tcp.recv(1024).decode()   # Receive a message from the server using TCP
            print(message)
        
        command = input('Enter Command ')   # Prompt the user for another command


        clientSocket_tcp.close()    # Close the TCP socket for the client



    
    
   
    
   
