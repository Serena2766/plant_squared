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


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = int(2221)
server_address = ('', port)

# Repeat specified number of times
for i in range(5):
    r = 5
    data = str(r)
    s.sendto(data.encode('utf-8'), server_address)
    
