import socket
import csv

hostD_socket=socket.socket()
with open("HostName.rtl") as file:
    data=file.read().splitlines()

for line in data:
    if line.split('|')[0]=="D":
        host=line.split('|')[1]
        port=line.split('|')[2]

hostD_socket.bind((host,int(port)))
print("socket created with host "+host+" and port "+port)
hostD_socket.listen(5)

while True:
    connection,address=hostD_socket.accept()
    print("connected successfully with IP " + address[0] + " and port " + str(address[1]))

    username=connection.recv(1024)
    print("Received username : "+username.decode())
    connection.send("HostD received username : ".encode()+username)

    password=connection.recv(1024)
    print("Received password : " + password.decode())
    connection.send("HostD received password : ".encode() + password)

    csv_file = csv.reader(open('attendance.csv', 'r'))
    flag = 0
    count=0
    for row in csv_file:
        if row[1] == username.decode():
            for i in range(2,len(row)):
                if row[i]=="Done":
                    count+=1

    if count/8>=0.8:
        flag=1
        print("SUCCESS! Attendance is greater than or equal to 80%")
        connection.send("1".encode())

    if flag == 0:
        print("FAILURE! Attendance is less than 80%")
        connection.send("0".encode())

    connection.close()