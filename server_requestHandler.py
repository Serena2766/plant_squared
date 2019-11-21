import socket, sys, time, datetime

WATER_COMMAND = '0001'
LIGHT_COMMAND = '0010'
PLANTID_COMMAND = '0100'
UPDATE_COMMAND = '0111'
ACK = '01100001'
NACK = '01101110'
bit1 = '0001'
bit2 = '0010'
bit3 = '0011'
bit4 = '0100'
bit5 = '0101'

SIZE = 1024
client_ip = 'localhost'
client_port = int(9003)
app_ip = 'localhost'
app_port = int(9003)
listen_port = 8001
listen_host = ''
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((listen_host,listen_port))
client_address = (client_ip, client_port)
app_address = (app_ip, app_port)

def valid_amount(cmd):
    if cmd[4:] == bit1 or cmd[4:] == bit2 or cmd[4:] == bit3 or cmd[4:] == bit4 or cmd[4:] == bit5:
        return True
    else:
        return False
        
def server_timeout(s):
        receive_ACK = False
        receive_NACK = False
        timeout = False    
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
                elif data[:4] == UPDATE_COMMAND:
                    print('Received updated info, send back ACK')
                    server_socket.sendto(ACK.encode('utf-8'),address)
                    receive_ACK = True
            except :
                timeout = True               
                break
        s.settimeout(None)
        return timeout

time_to_light = 0    

while True:
    time_to_light = time_to_light + 1
    
    if time_to_light == 6:
        cnt = 0
        data = LIGHT_COMMAND + bit1
        print('Auto send light command')
        server_socket.sendto(data.encode('utf-8'),client_address)
        while server_timeout(server_socket) and cnt < 3:
            cnt = cnt + 1
            print('Server timeouts, resend the message')
            time.sleep(2)
            server_socket.sendto(data.encode('utf-8'),client_address)
            if cnt == 3:
                print('Something wrong wiht the client')
        #next test case
        cnt =0
        data = UPDATE_COMMAND + bit1
        print('Auto send update command')
        server_socket.sendto(data.encode('utf-8'),client_address)
        while server_timeout(server_socket) and cnt < 3:
            cnt = cnt + 1
            print('Server timeouts, resend the message')
            time.sleep(2)
            server_socket.sendto(data.encode('utf-8'),client_address)
            if cnt == 3:
                print('Something wrong wiht the client')
    #listen on the port            
    try:       
        print ("\nListening on port %d : press Ctrl-C to stop " % listen_port)
        data, address = server_socket.recvfrom(SIZE)
        #print ("Received %s bytes from %s %s: " % (len(data), address, data ))
        ip,port = address
        if len(data) is not 8: 
            server_socket.sendto(NACK.encode('utf-8'),address)
            #print("Received invalid packet, send NACK to {}" .format(address))
            print("Received invalid packet, send NACK to where it's from ")
        else:
            if data[:4] == WATER_COMMAND:
                print('Received water command.')                
                if valid_amount(data):
                    print('Valid water amount, send back ACK')
                    server_socket.sendto(ACK.encode('utf-8'),address)
                    time.sleep(2)
                    server_socket.sendto(data.encode('utf-8'),client_address)
                    while server_timeout(server_socket):
                        server_socket.sendto(data.encode('utf-8'),client_address)                    
                else:
                    print('Invalid water amount, send back NACK')
                    server_socket.sendto(NACK.encode('utf-8'),address)         
            elif data[:4] == LIGHT_COMMAND:
                print('Received light command.')           
                if valid_amount(data):
                    print('Valid light amount, send back ACK')
                    server_socket.sendto(ACK.encode('utf-8'),address)
                    time.sleep(2)
                    server_socket.sendto(data.encode('utf-8'),client_address)
                    while server_timeout(server_socket):
                        server_socket.sendto(data.encode('utf-8'),client_address)
                else:
                    print('Invalid light amount, send back NACK')
                    server_socket.sendto(NACK.encode('utf-8'),address)                  
            elif data[:4] == UPDATE_COMMAND:
                print('Received update command.')
                server_socket.sendto(ACK.encode('utf-8'),address)
                print('Sent to the client')
                time.sleep(2)
                server_socket.sendto(data.encode('utf-8'),client_address)
                server_timeout(server_socket)                
            elif data[:4] == PLANTID_COMMAND:
                print('Received plant id command.')
                if data[4:] == bit1 or data[4:] == bit2 or data[4:] == bit3:
                    server_socket.sendto(ACK.encode('utf-8'),address)
                    time.sleep(2)
                    server_socket.sendto(data.encode('utf-8'),address) 
                    print('Valid plant id, send to App')
                    print('Data updated')
                    while server_timeout(server_socket):
                        server_socket.sendto(data.encode('utf-8'),address)                    
                else:
                    print('Invalid plant id, send back NACK')
                    server_socket.sendto(NACK.encode('utf-8'),address)
   
    except (KeyboardInterrupt,SystemExit):
        print('Exit the system.')
        raise       
server_socket.close()
server_socket.shutdown(1)

















