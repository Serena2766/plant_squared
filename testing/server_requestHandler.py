#author Xinrui Zhang
import socket, sys, time, datetime
import sqlite3
from sqlite3 import Error

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

DEFAULT = 0
current_plant_id = DEFAULT
current_condition = [1,1,20.3,31.5]
ideal_condition =[]
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
        
def set_plant_id(i):
    switcher={
        bit1:1,
        bit2:2,
        bit3:3           
        }
    return switcher.get(i,DEFAULT)

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return conn
 
def update_id_info(conn, id):
    """
    Query all rows in the tasks table
    :param conn: the fonnection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM plants WHERE id=?",(id,))
 
    rows = cur.fetchall()
 
    for row in rows:
        print('Ideal conditions updated.')
        print('Ideal water_level:%d' %row[2])
        ideal_condition.insert(0,row[2])
        print('Ideal light_level:%d' %row[3])
        ideal_condition.insert(1,row[3])
        print('Ideal humidity:%3.2f' %row[4])
        ideal_condition.insert(2,row[4])
        print('Ideal temperture:%3.2f' %row[5])
        ideal_condition.insert(3,row[5])
    
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
                    print('Received updated id info, send back ACK')
                    current_plant_id = set_plant_id(data[4:])
                    database = 'demo.db'
                    conn = create_connection(database)
                    update_id_info(conn,current_plant_id)
                    print('Data updated, current plant id is %d'%current_plant_id)
                    server_socket.sendto(ACK.encode('utf-8'),address)
                    receive_ACK = True
            except :
                timeout = True               
                break
        s.settimeout(None)
        return timeout

time_to_light = 0    

def handle_timeout(s, addr):
    cnt = 0
    while server_timeout(s) and cnt < 3:
        cnt = cnt + 1
        print('Server timeouts, resend the message')
        time.sleep(1)
        server_socket.sendto(data.encode('utf-8'),addr)     
        if cnt == 3:
            if addr[0] == app_ip:
                print('Something wrong with the app')
            elif addr[0] == client_ip:
                print('Something wrong with the server')



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
        print('\nAuto send update ID request')
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
        ip,port = address
        if len(data) is not 8: 
            server_socket.sendto(NACK.encode('utf-8'),address)
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
                print('Received update request.')
                server_socket.sendto(ACK.encode('utf-8'),address)
                if time_to_light < 5:
                    print('Sent the update request to client')
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
                    current_plant_id = set_plant_id(data[4:])
                    #fetch data in the database
                    database = 'demo.db'
                    conn = create_connection(database)
                    update_id_info(conn,current_plant_id)
                    print('Data updated, current plant id is %d'%current_plant_id)
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
