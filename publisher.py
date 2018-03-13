from socket import socket, AF_INET, SOCK_STREAM
import sys

MAX_BUF = 2048
SERV_PORT = 50000

addr = ('127.0.0.1', SERV_PORT)
s = socket(AF_INET, SOCK_STREAM)
s.connect(addr)
s.send("publisher".encode('utf-8'))
command = ['topic','publish','cancel','quit']
while True:
    print ('publisher> ', end='') 
    sys.stdout.flush()
    txtout = sys.stdin.readline().strip()
    input = txtout.split(" ")
    if input[0] in command:    
        if input[0] == command[0] or input[0] == command[2]:
            if int(len(input)) == 2:
                s.send(txtout.lower().encode('utf-8'))
                modifiedMsg = s.recv(2048)
                print (modifiedMsg.decode('utf-8'))
            else:
                print("Wrong format")
        elif input[0] == command[1]:
            if int(len(input)) > 1:
                s.send((input[0].lower()+ ' ' + " ".join(input[1:len(input)])).encode('utf-8'))
                modifiedMsg = s.recv(2048)
                print (modifiedMsg.decode('utf-8'))
            else:
                print("Wrong format")
        else: 
            if int(len(input))==1:
                s.send(b'quit')
                break
            else:
                print("Wrong format")
    else:
        print("No command")
s.close()
