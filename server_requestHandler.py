import socket, sys, time

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
app_ip = ' '
app_port = int(9003)
listen_port = 8000
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
        
while True:
    try:
        print ("\nListening on port %d : press Ctrl-C to stop " % listen_port)

        data, address = server_socket.recvfrom(SIZE)
        #print ("Received %s bytes from %s %s: " % (len(data), address, data ))
        ip,port = address
        if len(data) is not 8: 
            server_socket.sendto(NACK.encode('utf-8'),address)
            print("Received invalid packet, send NACK to {}" .format(address))
        else:
            if data[:4] == WATER_COMMAND:
                print('Received water command.')                
                if valid_amount(data):
                    print('Received valid water setting command, send back ACK')
                    server_socket.sendto(data.encode('utf-8'),address)
                    time.sleep(5)
                    server_socket.sendto(ACK.encode('utf-8'),address)
                else:
                    print('Undefined water amount, send back NACK')
                    server_socket.sendto(NACK.encode('utf-8'),address)
                
            elif data[:4] == LIGHT_COMMAND:
                print('Received light command.')           
                if valid_amount(data):
                    print('Received valid light setting command, send back ACK')
                    server_socket.sendto(data.encode('utf-8'),address)
                    time.sleep(5)
                    server_socket.sendto(ACK.encode('utf-8'),address)
                else:
                    print('Undefined light amount, send back NACK')
                    server_socket.sendto(NACK.encode('utf-8'),address)
                    
            elif data[:4] == UPDATE_COMMAND:
                print('Received update command.')
                server_socket.sendto(data.encode('utf-8'),address)
                print('Sent to the client')
                time.sleep(5)
                server_socket.sendto(ACK.encode('utf-8'),address)
                
            elif data[:4] == PLANTID_COMMAND:
                print('Received plant id command.')
                if data[4:] == bit1 or data[4:] == bit2 or data[4:] == bit3:
                    server_socket.sendto(ACK.encode('utf-8'),address)
                    time.sleep(5)
                    server_socket.sendto(data.encode('utf-8'),address)               
                    print('Received valid plant id, data updated.')
                else:
                    print('Invalid plant id, send back NACK')
                    server_socket.sendto(NACK.encode('utf-8'),address)
                    
            elif data == ACK:
                print('Received ACK')
            
    except (KeyboardInterrupt,SystemExit):
        print('Exit the system.')
        raise
        
        
    # print ("Received %s bytes from %s %s: " % (len(data), address, data ))
server_socket.close()
server_socket.shutdown(1)

















