from socket import socket, AF_INET, SOCK_STREAM

MAX_BUF = 2048
SERV_PORT = 50000

addr = ('127.0.0.1', SERV_PORT)
s = socket(AF_INET, SOCK_STREAM)
s.connect(addr)
s.send("subscriber".encode('utf-8'))

topic = input('Enter topics:')
topic = topic.lower().strip()
print ('Topic is', topic)
s.send(topic.encode('utf-8'))

print('start recieving...')
while True:  
    data = s.recv(MAX_BUF)
    data = data.decode('utf-8')
    print('Broker>' + data)
s.close()
