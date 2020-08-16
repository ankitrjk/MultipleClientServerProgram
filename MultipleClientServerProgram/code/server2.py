import socket
import threading
import hashlib
import random
import time

#creating socket
server_socket=socket.socket()
with open("HostName.rtl") as file:
    data=file.read().splitlines()

for line in data:
    if line.split('|')[0]=="server2":
        host=line.split('|')[1]
        port=line.split('|')[2]
server_socket.bind((host,int(port)))
print("socket created with host "+host+" and port "+port)
server_socket.listen(5)

def createSocketForHostA():
    # requesting hostA through new socket
    server_hostA_socket = socket.socket()
    return server_hostA_socket

def createSocketForHostB():
    # requesting hostB through new socket
    server_hostB_socket = socket.socket()
    return server_hostB_socket

def createSocketForHostC():
    # requesting hostC through new socket
    server_hostC_socket = socket.socket()
    return server_hostC_socket

def createSocketForHostD():
    # requesting hostD through new socket
    server_hostD_socket = socket.socket()
    return server_hostD_socket

def callA(username,password,server_hostA_socket):
    with open("HostName.rtl") as file:
        filedata = file.read().splitlines()

    for line in filedata:
        if line.split('|')[0] == "A":
            hostA = line.split('|')[1]
            portA = line.split('|')[2]

    server_hostA_socket.connect((hostA, int(portA)))
    print("Server connected successfully with Host A " + host + " and port " + portA)

    server_hostA_socket.send(username)
    msg1 = server_hostA_socket.recv(1024)
    print(msg1.decode())

    server_hostA_socket.send(password)
    msg2 = server_hostA_socket.recv(1024)
    print(msg2.decode())

    data = server_hostA_socket.recv(1024)
    if data.decode() == "1":
        print("Username and password found on HostA")
        return 1

    return 0



def callB(username,password,server_hostB_socket):
    with open("HostName.rtl") as file:
        filedata = file.read().splitlines()

    for line in filedata:
        if line.split('|')[0] == "B":
            hostB = line.split('|')[1]
            portB = line.split('|')[2]

    server_hostB_socket.connect((hostB, int(portB)))
    print("Server connected successfully with Host B " + host + " and port " + portB)

    server_hostB_socket.send(username)
    msg1 = server_hostB_socket.recv(1024)
    print(msg1.decode())

    server_hostB_socket.send(password)
    msg2 = server_hostB_socket.recv(1024)
    print(msg2.decode())

    data = server_hostB_socket.recv(1024)
    if data.decode() == "1":
        print("Username and password found on HostB")
        return 1

    return 0


def callC(username,password,server_hostC_socket):
    with open("HostName.rtl") as file:
        filedata = file.read().splitlines()

    for line in filedata:
        if line.split('|')[0] == "C":
            hostC = line.split('|')[1]
            portC = line.split('|')[2]

    server_hostC_socket.connect((hostC, int(portC)))
    print("Server connected successfully with Host C " + host + " and port " + portC)

    server_hostC_socket.send(username)
    msg1 = server_hostC_socket.recv(1024)
    print(msg1.decode())

    server_hostC_socket.send(password)
    msg2 = server_hostC_socket.recv(1024)
    print(msg2.decode())

    data = server_hostC_socket.recv(1024)
    if data.decode() == "1":
        print("Username and password found on HostB")
        return 1

    return 0


def callD(username,password,server_hostD_socket):
    with open("HostName.rtl") as file:
        filedata = file.read().splitlines()

    for line in filedata:
        if line.split('|')[0] == "D":
            hostD = line.split('|')[1]
            portD = line.split('|')[2]

    server_hostD_socket.connect((hostD, int(portD)))
    print("Server connected successfully with Host D " + host + " and port " + portD)

    server_hostD_socket.send(username)
    msg1 = server_hostD_socket.recv(1024)
    print(msg1.decode())

    server_hostD_socket.send(password)
    msg2 = server_hostD_socket.recv(1024)
    print(msg2.decode())

    data = server_hostD_socket.recv(1024)
    if data.decode() == "1":
        print("Attendance is greater than or equal to 80%")
        return 1

    return 0


def authenticate(conn,IP,port):
    while True:
        username = conn.recv(1024)
        if username.decode()=="EXIT":
            break

        print("Received username: " + username.decode())
        conn.send("Server 2 received username: ".encode() + username)
        password = conn.recv(1024)
        if password.decode()=="EXIT":
            break

        print("Server 2 received password: " + password.decode())

        server_hostA_socket = createSocketForHostA()
        server_hostB_socket = createSocketForHostB()
        server_hostC_socket = createSocketForHostC()
        server_hostD_socket = createSocketForHostD()

        resultA = callA(username, password,server_hostA_socket)
        resultB = callB(username, password,server_hostB_socket)
        resultC = callC(username, password,server_hostC_socket)
        resultD = callD(username, password,server_hostD_socket)

        if (resultA or resultB or resultC) and resultD:
            print("Username and password found and attendance is greater than or equal to 80%\n")
            conn.send("SUCCESS! Username and password found and attendance is greater than or equal to 80%".encode())
            # receive file data with error checking
            while True:
                frame = conn.recv(1024 * 1024)
                if not frame:
                    break
                myframe = bytearray(frame)
                myframeCopy = bytearray(frame)
                packetdata = myframeCopy[-16:]
                # print(packetdata)
                del myframeCopy[-16:]
                # print(myframe[1:].decode())
                # find Correct host to redirect data
                # adding random delay
                duration = random.randint(200, 1000)
                duration = duration / 1000
                print("Adding a random delay of " + str(duration) + " seconds")
                time.sleep(duration)

                if resultA:
                    server_hostA_socket.send(myframe)
                elif resultB:
                    server_hostB_socket.send(myframe)
                elif resultC:
                    server_hostC_socket.send(myframe)

                if hashlib.md5(myframeCopy[1:]).digest() == packetdata:
                    print("Frame received successfully from the client")
                    conn.send("1".encode())
                else:
                    print("Frame received from the client is corrupted")
                    conn.send("0".encode())
                    frame2 = conn.recv(1024 * 1024)
                    myframe2 = bytearray(frame2)
                    myframe2Copy = bytearray(frame2)
                    packetdata2 = myframe2Copy[-16:]
                    # print(packetdata2)
                    del myframe2Copy[-16:]
                    # print(myframe2[1:].decode())
                    # find Correct host to redirect data
                    # adding random delay
                    duration = random.randint(200, 1000)
                    duration = duration / 1000
                    print("Adding a random delay of " + str(duration) + " seconds")
                    time.sleep(duration)
                    if resultA:
                        server_hostA_socket.send(myframe2)
                    elif resultB:
                        server_hostB_socket.send(myframe2)
                    elif resultC:
                        server_hostC_socket.send(myframe2)

                    if hashlib.md5(myframe2Copy[1:]).digest() == packetdata2:
                        print("Frame received successfully from the client")
                        conn.send("1".encode())
                    else:
                        print("Frame received from the client is again corrupted")
                        conn.send("0".encode())


            if resultA:
                print("All frames delivered successfully to Host A")
            elif resultB:
                print("All frames delivered successfully to Host B")
            elif resultC:
                print("All frames delivered successfully to Host C")

        elif resultA or resultB or resultC:
            print("Username and password found but attendance is less than 80%\n")
            conn.send("FAILURE! Username and password found but attendance is less than 80%".encode())

        else:
            print("Username and password does not exist\n")
            conn.send("FAILURE! Username and password does not exist".encode())

        server_hostA_socket.close()
        server_hostB_socket.close()
        server_hostC_socket.close()
        server_hostD_socket.close()
        break

    print("connection closed with IP " + IP + " and port " + str(port))
    conn.close()



while True:
    conn,address=server_socket.accept()
    print("connected successfully with IP "+address[0]+" and port "+str(address[1]))
    thread1=threading.Thread(target=authenticate,args=(conn,address[0],address[1],))
    thread1.start()






