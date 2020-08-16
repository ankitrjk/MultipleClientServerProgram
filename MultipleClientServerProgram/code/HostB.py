import socket
import csv
import threading
import os
import hashlib

hostB_socket=socket.socket()
with open("HostName.rtl") as file:
    data=file.read().splitlines()

for line in data:
    if line.split('|')[0]=="B":
        host=line.split('|')[1]
        port=line.split('|')[2]

hostB_socket.bind((host,int(port)))
print("socket created with host "+host+" and port "+port)
hostB_socket.listen(5)


def receivedata(connection,IP,Port):
    username = connection.recv(1024)
    print("Received username : " + username.decode())
    connection.send("HostB received username : ".encode() + username)

    password = connection.recv(1024)
    print("Received password : " + password.decode())
    connection.send("HostB received password : ".encode() + password)

    csv_file = csv.reader(open('2.csv', 'r'))
    flag = 0
    for row in csv_file:
        if row[0] == username.decode() and row[1] == password.decode():
            print("SUCCESS! Username and password exists")
            connection.send("1".encode())
            flag = 1
            # receive file
            outfile=open(username.decode()+".txt", "a+",newline='')
            server_no=0
            #file_data = bytearray()
            while True:
                frame = connection.recv(1024*1024)
                if not frame:
                    break
                file_data = bytearray(frame)
                server_no = file_data[:1].decode()
                packetdata = file_data[-16:]
                del file_data[-16:]
                if hashlib.md5(file_data[1:]).digest() != packetdata:
                    print("Frame received from server "+server_no+" is corrupted ")
                else:
                    print("Frame received successfully from server "+server_no)
                    outfile.write(file_data[1:].decode(errors='ignore'))

            if os.stat(username.decode()+".txt").st_size==0:
                print("empty file")
                #connection.send("0".encode())
            else:
                print("All frames received successfully from server "+server_no)
                #connection.send("1".encode())

    if flag == 0:
        print("FAILURE! Username and password does not exist")
        connection.send("0".encode())

    connection.close()


while True:
    connection,address=hostB_socket.accept()
    print("connected successfully with IP " + address[0] + " and port " + str(address[1]))
    thread1 = threading.Thread(target=receivedata, args=(connection, address[0], address[1],))
    thread1.start()
