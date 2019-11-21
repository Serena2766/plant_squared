import socket, sys, time



# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# port = int(2002)
# server_address = ('localhost', port)
# s.bind(server_address)
# client_address = ('localhost', 2004)
# while True:

    # print ("Waiting to receive on port %d : press Ctrl-C or Ctrl-Break to stop " % port)

    # buf, address = s.recvfrom(port)
  
    # if not len(buf):
        # break
    # print ("Received %s bytes from %s %s: " % (len(buf), address, buf ))
WATER_COMMAND = '0001'
LIGHT_COMMAND = '0010'
PLANTID_COMMAND = '0100'
UPDATE_COMMAND = '0111'
ACK = '01100001'
NACK = '01101110'

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = int(9003)
client_address = ('localhost', port)
s.bind(client_address)

server_address = ('localhost', int(8001))
i = 0
cnt1 = 0
cnt2 = 0 
while True:
    i=i+1
    print ("\nListening on port %d : press Ctrl-C to stop " % port)
    if i == 1:
        print ('Client: Sent valid plant id')
        data = '01000010'
    if i == 2:
        print ('Client:Sent invalid plant id')
        data = '01000111'
    if i == 3:
        print ('App: Sent valid water amount')
        data = '00010001'
    if i == 4:
        print ('App: Sent invalid water amount')
        data = '00010111'
    if i == 5:
        print ('Client: Sent an empty message')
        data = ''
    receive_ACK = False
    receive_NACK = False
    timeout = False     
    if i < 6 or cnt2 == 2:
        s.sendto(data.encode('utf-8'), server_address)
        cnt = 0
        while not receive_ACK and not receive_NACK and not timeout:     
            data, address = s.recvfrom(1024)
            cnt = cnt +1
            if data == ACK:
                print('Received ACK from the server')
                receive_ACK = True
            elif data == NACK:
                print('Received NACK from the server')
                receive_NACK = True
            elif cnt == 100:
                timeout = True
    if i == 10:
        break
    try:
        if not receive_NACK:
            data, address = s.recvfrom(1024)        
            ip,port = address
            if data[:4] == WATER_COMMAND:
                print('Client: Received water command.')
                time.sleep(2)
                s.sendto(ACK.encode('utf-8'), server_address)
            elif data[:4] == LIGHT_COMMAND:
                cnt1 = cnt1 +1 
                print('Received light command.')   
                time.sleep(2)  
                if cnt1 == 2:
                    s.sendto(ACK.encode('utf-8'), server_address)
            elif data[:4] == UPDATE_COMMAND:
                cnt2 = cnt2 + 1
                print('Received update command.')
                time.sleep(2)
                if cnt2 == 2:
                    s.sendto(data.encode('utf-8'), server_address)
                    print('Client: Sent updated info to server')
                
            elif data[:4] == PLANTID_COMMAND:   
                print('App: Received plant id command.')
                time.sleep(2)
                s.sendto(ACK.encode('utf-8'), server_address)
        #print ("Received %s bytes from %s %s: " % (len(data), address, data ))

    except (KeyboardInterrupt,SystemExit):
        print('Exit the system.')
        raise
    
s.close()