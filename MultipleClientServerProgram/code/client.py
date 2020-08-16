import socket
import random
import hashlib

def createSocketForServer1():
    server1_client_socket=socket.socket()
    with open("HostName.rtl") as file:
        data = file.read().splitlines()
    for line in data:
        if line.split('|')[0] == "server1":
            host1 = line.split('|')[1]
            port1 = line.split('|')[2]
    server1_client_socket.connect((host1, int(port1)))
    print("connected successfully with " + host1 + " and port " + port1)
    return server1_client_socket

def createSocketForServer2():
    server2_client_socket=socket.socket()
    with open("HostName.rtl") as file:
        data = file.read().splitlines()
    for line in data:
        if line.split('|')[0] == "server2":
            host1 = line.split('|')[1]
            port1 = line.split('|')[2]
    server2_client_socket.connect((host1, int(port1)))
    print("connected successfully with " + host1 + " and port " + port1)
    return server2_client_socket


def authenticateUsernameOnServer1(username,server1_client_socket,server2_client_socket):
    server1_client_socket.send(username.encode())
    if username == "EXIT":
        server2_client_socket.send(username.encode())
        print("connection closed successfully with server 1\n")
        return False
    data = server1_client_socket.recv(1024)
    print(data.decode())
    return True


def authenticatePasswordOnServer1(password,server1_client_socket,server2_client_socket):
    server1_client_socket.send(password.encode())
    if password == "EXIT":
        server2_client_socket.send(password.encode())
        print("connection closed successfully with server 1\n")
        return False
    msg = server1_client_socket.recv(1024)
    print(msg.decode()+'\n')

    if msg.decode().find('SUCCESS')!=-1:
        print("Authorised to send file to the server 1\n")
    else:
        print("Can't send file to the server 1 because you are not authorised\n")
        print("connection closed successfully with server 1\n")
        server1_client_socket.send("EXIT".encode())
        return False

    return True

def authenticateUsernameOnServer2(username,server1_client_socket,server2_client_socket):
    server2_client_socket.send(username.encode())
    if username == "EXIT":
        server1_client_socket.send(username.encode())
        print("connection closed successfully with server 2\n")
        return False
    data = server2_client_socket.recv(1024)
    print(data.decode())
    return True


def authenticatePasswordOnServer2(password,server1_client_socket,server2_client_socket):
    server2_client_socket.send(password.encode())
    if password == "EXIT":
        server1_client_socket.send(password.encode())
        print("connection closed successfully with server 2\n")
        return False
    msg = server2_client_socket.recv(1024)
    print(msg.decode()+'\n')

    if msg.decode().find('SUCCESS')!=-1:
        print("Authorised to send file to the server 2\n")
    else:
        print("Can't send file to the server 2 because you are not authorised\n")
        print("connection closed successfully with server 2\n")
        server2_client_socket.send("EXIT".encode())
        return False

    return True


def corruptframe(newframe,probability):
    probability=probability*100
    number=random.randint(1,100)
    #print("probability number : "+str(number))
    if 1<=int(number)<=probability:
        del newframe[-4:]
    return newframe


def sendThrough1(data,probability,server1_client_socket):
    checksum=hashlib.md5(data).digest()
    #print(checksum)
    frame1=bytearray("1".encode())
    frame2=bytearray(data)
    frame3=bytearray(checksum)
    frame=frame1+frame2+frame3;
    newframe=bytearray(frame)
    corruptedframe=corruptframe(newframe,probability)
    server1_client_socket.send(corruptedframe)
    print("sending frame to server 1")
    response=server1_client_socket.recv(10)
    if response.decode()=="1":
        print("server 1 received frame successfully")
    elif response.decode()=="0":
        print("server 1 received corrupted frame")
        server1_client_socket.send(frame)
        print("Resending frame to server 1")
        response2 = server1_client_socket.recv(10)
        if response2.decode() == "1":
            print("server 1 received frame successfully")
        elif response2.decode() == "0":
            print("error occured")

def sendThrough2(data,probability,server2_client_socket):
    checksum = hashlib.md5(data).digest()
    # print(checksum)
    frame1 = bytearray("2".encode())
    frame2 = bytearray(data)
    frame3 = bytearray(checksum)
    frame = frame1 + frame2 + frame3;
    newframe = bytearray(frame)
    corruptedframe = corruptframe(newframe, probability)
    server2_client_socket.send(corruptedframe)
    print("sending frame to server 2")
    response = server2_client_socket.recv(10)
    if response.decode() == "1":
        print("server 2 received frame successfully")
    elif response.decode() == "0":
        print("server 2 received corrupted frame")
        server2_client_socket.send(frame)
        print("Resending frame to server 2")
        response2 = server2_client_socket.recv(10)
        if response2.decode() == "1":
            print("server 2 received frame successfully")
        elif response2.decode() == "0":
            print("error occured")


def sendFile(server1_client_socket,server2_client_socket):
    frame_size=input("Enter the size of Frame in KB: ")
    if frame_size=="":
        frame_size=100
    else:
        frame_size=int(frame_size)

    probability = input("Enter the probability of Frame corruption : ")
    if probability == "":
        probability = 0.1
    else:
        probability = float(probability)

    print("Initializing data upload ..............................................")

    myfile=open("Sample1.txt","rb")
    data=myfile.read(1024*frame_size)
    counter = 1
    while data:
        #send frame
        if counter%2==1:
            sendThrough1(data,probability,server1_client_socket)
        else:
            sendThrough2(data,probability,server2_client_socket)

        counter+=1
        data=myfile.read(1024*frame_size)
    myfile.close()




while True:
    server1_client_socket=createSocketForServer1()
    server2_client_socket=createSocketForServer2()
    username = input("Enter username")
    #choice=random.randint(1,2)
    a=authenticateUsernameOnServer1(username,server1_client_socket,server2_client_socket)
    b=authenticateUsernameOnServer2(username,server1_client_socket,server2_client_socket)
    if (not a) or (not b):
        server1_client_socket.close()
        server2_client_socket.close()
        break
    password = input("Enter password")
    c=authenticatePasswordOnServer1(password,server1_client_socket,server2_client_socket)
    d=authenticatePasswordOnServer2(password,server1_client_socket,server2_client_socket)
    if (not c):
        server1_client_socket.close()
    if (not d):
        server2_client_socket.close()
        break
    sendFile(server1_client_socket,server2_client_socket)
    print("File submitted successfully")
    server1_client_socket.close()
    print("connection closed successfully with server 1\n")
    server2_client_socket.close()
    print("connection closed successfully with server 2\n")
    break



