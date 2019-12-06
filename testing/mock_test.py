#author Xinrui Zhang
import socket, sys, time

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
        print('Test case %d'%i)
        print ('Client: Sent valid plant id')
        data = '01000010'
    if i == 2:
        print('Test case %d'%i)
        print ('Client:Sent invalid plant id')
        data = '01000111'
    if i == 3:
        print('Test case %d'%i)
        print ('App: Sent valid water amount')
        data = '00010001'
    if i == 4:
        print('Test case %d'%i)
        print ('App: Sent invalid water amount')
        data = '00010111'
    if i == 5:
        print('Test case %d'%i)
        print ('Client: Sent an empty message')
        data = ''
    receive_ACK = False
    receive_NACK = False
    timeout = False     
    if i < 6 or cnt2 == 2:
        s.sendto(data.encode('utf-8'), server_address)           
        s.settimeout(5)
        while not receive_ACK and not receive_NACK and not timeout:                    
            try :
                data, address = s.recvfrom(1024)
                if data == ACK:
                    print('Received ACK')
                    receive_ACK = True
                elif data == NACK:
                    print('Received NACK')
                    receive_NACK = True                
            except :
                timeout = True               
                break
        s.settimeout(None)
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
                if cnt1 == 1:
                    print('Test case 6')
                print('Received light command.')   
                time.sleep(2)  
                if cnt1 == 2:
                    s.sendto(ACK.encode('utf-8'), server_address)
            elif data[:4] == UPDATE_COMMAND:
                cnt2 = cnt2 + 1
                if cnt2 == 1:
                    print('Test case 7')
                print('Received update command.')
                time.sleep(2)
                if cnt2 == 2:
                    s.sendto(data.encode('utf-8'), server_address)
                    print('Client: Sent updated info to server')              
            elif data[:4] == PLANTID_COMMAND:   
                print('App: Received plant id command.')
                time.sleep(2)
                s.sendto(ACK.encode('utf-8'), server_address)
    except (KeyboardInterrupt,SystemExit):
        print('Exit the system.')
        raise   
s.close()

