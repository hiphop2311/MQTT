from socket import * 
from threading import Thread, Lock
import os,sys

lock = Lock()

SERV_PORT = 50000
topic = {}
dataTopic = {}
topicPub = {}

def handle_wordDel():
	while True:
		tp = topic.copy()
		for key,value in tp.items():
			ls = list(dataTopic[key])
			for key2 in ls:
				dataTopic[key][key2].sort()
				topic[key].sort()
				print('del ' + str(dataTopic[key][key2]))
				print('del ' + str(topic[key]))
				if dataTopic[key][key2] == topic[key]:
					del dataTopic[key][key2]

	# ls = list(dataTopic[topicPub[ip+':'+port][0]])
 #    	for key in ls:
 #        	dataTopic[topicPub[ip+':'+port][0]][key].sort()
 #            topic[topicPub[ip+':'+port][0]].sort()
 #            if dataTopic[topicPub[ip+':'+port][0]][key] == topic[topicPub[ip+':'+port][0]]:
 #            	del dataTopic[topicPub[ip+':'+port][0]][key]

def handle_subscriber(s,ip,port):

  txtin = ''

  try:
    # Subscriber send topic
    txtinput = s.recv(1024)
    txtinp = (txtinput).decode('utf-8')
    txtin = txtinp.split(" ")

    tp = topic.copy()
    for key, value in tp.items():
      if key in txtin:
        topic[key].append(ip+':'+port)

    while True:
      subTopic = []
      checkValue = 0
      key = ''
      value = ''
      dataToPrint = ''
      tp = topic.copy();
      for key, value in tp.items():
        if key in txtin:
          checkValue = 1
          subTopic.append(key)

      tp = topic.copy()
      for key, value in tp.items():
      	if key in txtin:
      	  if ip+':'+port not in topic[key]:
            topic[key].append(ip+':'+port)
            print('sub ' + str(topic[key]))

      if checkValue == 1:
        for sub in subTopic:
          dataC = dataTopic[sub].copy()
          for word, subscribe in dataC.items():
            if ip+':'+port not in subscribe:
              dataToPrint = sub + ' ' + word 
              s.send(dataToPrint.encode('utf-8'))
              print('insub '+str(sub))
              print('insub '+str(word))
              print('insub '+str(dataTopic))
              dataTopic[sub][word].append(ip+':'+port) 

    subTopic = []
    checkValue = 0
    key = ''
    value = ''

    tp = topic.copy()
    for key, value in tp.items():
      if key in txtin:
        checkValue = 1
        subTopic.append(key)

    tp = topic.copy()
    for key, value in tp.items():
      if ip+':'+port in tp[key]:
        topic[key].remove(ip+':'+port) 

    for sub in subTopic:
      dataC = dataTopic[sub].copy()
      for word, subscribe in dataC.items():
        if ip+':'+port in subscribe:
          dataTopic[sub][word].remove(ip+':'+port) 

    s.close()
    return

  except error:

    subTopic = []
    checkValue = 0
    key = ''
    value = ''
    tp = topic.copy()
    for key, value in tp.items():
      if key in txtin:
        checkValue = 1
        subTopic.append(key)

    tp = topic.copy()
    for key, value in tp.items():
      if ip+':'+port in tp[key]:
        topic[key].remove(ip+':'+port) 

    for sub in subTopic:
      dataC = dataTopic[sub].copy()
      for word, subscribe in dataC.items():
        if ip+':'+port in subscribe:
          dataTopic[sub][word].remove(ip+':'+port) 
    
    s.close()
    print('error in socket (' + ip + ':' + port + '). close socket')
    return

def handle_publisher(s,ip,port):
  try:
    topicPub[ip+':'+port] = []

    while True:
      txtinput = s.recv(1024)
      txtinput = (txtinput).decode('utf-8')
      # Split string
      txtin = txtinput.split(" ")
      # Join all text
      if txtin[0] != 'quit':
        txtin[1] = " ".join(txtin[1:])
        txtin = txtin[:2]

      txtout = ''

      if len(txtin) == 2:
        if txtin[0] == 'publish':
          print(dataTopic)
          key = ''
          value = ''

          # Publish
          if len(topicPub[ip+':'+port]) == 1:
            
            if len(dataTopic[topicPub[ip+':'+port][0]]) == 0:
              buff = {}
              buff[txtin[1]] = []
              dataTopic[topicPub[ip+':'+port][0]] = buff
              print(dataTopic)
            else:
              dataTopic[topicPub[ip+':'+port][0]][txtin[1]] = []
            txtout = 'Broker > publish ' + txtin[1]
          elif len(topicPub[ip+':'+port]) == 0:
            txtout = 'Broker > there is no topic to publish'
          else:
            txtout = 'Broker > error in publish' 
        
        elif txtin[0] == 'cancel':
          print(topic)
          print(topicPub)
          print(txtin[1])
          if len(topicPub[ip+':'+port]) == 0:
            txtout = 'Broker > there is no topic to cancel'
          elif len(topicPub[ip+':'+port]) == 1:
            if txtin[1] in topicPub[ip+':'+port]:
              del topic[topicPub[ip+':'+port][0]]  
              topicPub[ip+':'+port] = []
              txtout = 'Broker > cancel success'    
            else:
              txtout = 'Broker > wrong topic'       
          else:
            txtout = 'Broker > error in cancel'

        elif txtin[0] == 'topic':
          print(topicPub)
          print(txtin)
          # Check topic name is use or not
          isThereAnyTopic = 0;

          tp = topic.copy()
          for key, value in tp.items():
            if key == txtin[1]:
              topic[key].append(ip+':'+port)
              isThereAnyTopic = 1;
              txtout = 'Broker > there already has topic name ' + txtin[1] + ' in server'

          if isThereAnyTopic == 0:
            if len(topicPub[ip+':'+port]) ==0:
              topicPub[ip+':'+port] = []
              topicPub[ip+':'+port].append(txtin[1])
              dataTopic[txtin[1]] = {}
              topic[txtin[1]] = []
              txtout = 'Broker > topic ' + txtin[1] 
            else: 
              txtout = 'Broker > publisher already has topic'

      elif txtin[0] == 'quit':
        print('Broker > publisher ' + ' (' + ip + ':' + port + ')' + ' disconnected ...')
        break

      else:
        txtout = 'Broker > unknown format'

      print(txtout+' ('+ip+':'+port+')')
      s.send(txtout.encode('utf-8'))

    if len(topicPub[ip+':'+port]) != 0:
      del topic[topicPub[ip+':'+port][0]]
      del topicPub[ip+':'+port]
    s.close()
    return
  except error:
    print('error in socket (' + ip + ':' + port + '). close socket')
    del topic[topicPub[ip+':'+port][0]]
    del topicPub[ip+':'+port]
    s.close()
    return

def handle_wrong(s,ip,port):
  print ('Unknown client connected from ... ' + ip + ':' + port + 'Termanate connection')
  s.close()
  return

def main():
  addr = ('127.0.0.1', SERV_PORT)
  s = socket(AF_INET, SOCK_STREAM)
  s.bind(addr)
  s.listen(5)
  print ('TCP threaded server started ...')

  Thread(target=handle_wordDel).start()

  while True:
    sckt, addr = s.accept()
    ip, port = str(addr[0]), str(addr[1]) 
  
    try:
      who = sckt.recv(1024)
      if who == b'publisher':
        print ('New publisher connected from ... ' + ip + ':' + port)
        Thread(target=handle_publisher, args=(sckt, ip, port)).start()
      elif who == b'subscriber':
        print ('New subcriber connected from ... ' + ip + ':' + port)
        Thread(target=handle_subscriber, args=(sckt, ip, port)).start()
      else:
        Thread(target=handle_wrong, args=(sckt, ip, port)).start()
    except:
      print("Cannot start thread ...")
      import traceback
      trackback.print_exc()

  s.close()

if __name__ == '__main__':
   try:
     main()
   except KeyboardInterrupt:
     print ('Interrupted ..')
     try:
       sys.exit(0)
     except SystemExit:
       os._exit(0)
