import socket, sys, time, datetime, json
import sqlite3
from sqlite3 import Error

#define communication protocol constant
WATER_COMMAND = '0001'
LIGHT_COMMAND = '0010'
PLANTID_COMMAND = '0100'
UPDATE_COMMAND = '0111'
ACK = '01100001'
NACK = '01101110'
bit_list = ['0001','0010','0011','0100','0101']
#define plant info 
DEFAULT = 0
current_plant_id = DEFAULT
#list: moisture, light_level, temperature, humidity
current_condition = [0,0,0,0]
ideal_condition =[0,0,0,0]
#define client address
client_ip = 'localhost'
client_port = int(9003)
client_address = (client_ip, client_port)
#define app address
app_ip = 'localhost'
app_port = int(9003)
app_address = (app_ip, app_port)
#define server address
SIZE = 1024
server_ip = 'localhost'
server_port = 8001
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((server_ip,server_port))

def is_valid(cmd, list):    
    """ check if the amount is valid in the receving data
    :param cmd: receive data
    :param list: valid amount
    :return: True or False
    """
    if cmd[4:] in list:
        return True
    else:
        return False
        
def valid_current_info(buf,current_condition):
    """ check and update the current condition 
        if the json is valid in the receving data
    :param buf: receive data
    :return: True or False
    """
    json_obj = json.loads(buf) 
    curr_moisture = json_obj.get('moisture')
    curr_light_level = json_obj.get('lightLevel')
    curr_temperature = json_obj.get('temperature')
    curr_humidity = json_obj.get('humidity')
    
    if curr_humidity or curr_light_level or curr_moisture or curr_temperature is None:
        return False
    else:
        current_condition.insert(0,curr_moisture)
        current_condition.insert(1,curr_light_level)
        current_condition.insert(2,curr_temperature)
        current_condition.insert(3,curr_humidity)
        return True        
        
def set_plant_id(i):
    switcher={
        bit_list[1]:1,
        bit_list[2]:2,
        bit_list[3]:3           
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
        print('Current plant id is %d'%row[0])
        print('Ideal moisture:%3.2f' %row[2])
        ideal_condition.insert(0,row[2])
        print('Ideal light_level:%d' %row[3])
        ideal_condition.insert(1,row[3])
        print('Ideal humidity:%3.2f' %row[4])
        ideal_condition.insert(2,row[4])
        print('Ideal temperature:%3.2f' %row[5])
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
            except :
                timeout = True               
                break
        s.settimeout(None)
        return timeout

def handle_timeout(s, addr, data):
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
    #listen on the port            
    try:       
        print ("\nListening on port %d : press Ctrl-C to stop " % server_port)
        data, address = server_socket.recvfrom(SIZE)
        rcv_ip,rcv_port = address
        if not len(data):
            server_socket.sendto(NACK.encode('utf-8'),address)
            print("Received invalid packet, send NACK to where it's from ")
        else:
            if data[:4] == WATER_COMMAND:
                print('Received water command.')                
                if is_valid(data,bit_list):
                    print('Valid water amount, send back ACK')
                    server_socket.sendto(ACK.encode('utf-8'),address)
                    time.sleep(2)
                    server_socket.sendto(data.encode('utf-8'),client_address)
                    handle_timeout(server_socket, client_address, data)                
                else:
                    print('Invalid water amount, send back NACK')
                    server_socket.sendto(NACK.encode('utf-8'),address)   
                    
            elif data[:4] == LIGHT_COMMAND:
                print('Received light command.')           
                if is_valid(data,bit_list):
                    print('Valid light amount, send back ACK')
                    server_socket.sendto(ACK.encode('utf-8'),address)
                    time.sleep(2)
                    server_socket.sendto(data.encode('utf-8'),client_address)
                    handle_timeout(server_socket, client_address, data)
                else:
                    print('Invalid light amount, send back NACK')
                    server_socket.sendto(NACK.encode('utf-8'),address)   
                    
            elif data[:4] == UPDATE_COMMAND:
                print('Received update request.')
                server_socket.sendto(ACK.encode('utf-8'),address)
                #send current conditions in json to the app 
                msg = { }
                msg['moisture'] = current_condition[0]
                msg['lightLevel'] = current_condition[1]
                msg['temperature']= current_condition[2]
                msg['humidity']= current_condition[3]
                msg['plant_id'] = current_plant_id
                json_data = json.dumps(msg)
                json_str = str(json_data)
                time.sleep(2)
                server_socket.sendto(json_str.encode('utf-8'),app_address)                 
                handle_timeout(server_socket, app_address, json_str)  
                
            elif data[:4] == PLANTID_COMMAND:
                print('Received plant id command.')
                if is_valid(data[4:], bit_list):
                    server_socket.sendto(ACK.encode('utf-8'),address)
                    time.sleep(2)
                    server_socket.sendto(data.encode('utf-8'),app_address) 
                    print('Valid plant id, send to App')
                    current_plant_id = set_plant_id(data[4:])
                    print('Data updated, current plant id is %d'%current_plant_id)
                    #fetch data in the database
                    database = 'plants.db'
                    conn = create_connection(database)
                    #update ideal conditions
                    update_id_info(conn,current_plant_id)                
                    handle_timeout(server_socket, app_address, data)          
                else:
                    print('Invalid plant id, send back NACK')
                    server_socket.sendto(NACK.encode('utf-8'),address)
            else:
                if valid_current_info(data, current_condition):
                    server_socket.sendto(ACK.encode('utf-8'),address)
                    print('Current conditions updated.')
                    print('Current moisture:%3.2f' %current_condition[0])
                    print('Current light_level:%d' %current_condition[1])
                    print('Current humidity:%3.2f' %current_condition[2])
                    print('Current temperature:%3.2f' %current_condition[3])
                    server_socket.sendto(data.encode('utf-8'),app_address) 
                    handle_timeout(server_socket, app_address, data)   
                else:
                    print('Invalid current updates, send back NACK')
                    server_socket.sendto(NACK.encode('utf-8'),address)
    except (KeyboardInterrupt,SystemExit):
        print('Exit the system.')
        raise       
server_socket.close()
server_socket.shutdown(1)