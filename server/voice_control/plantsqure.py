import snowboydecoder
import sys, socket, time
import signal

#listening 3 hotword commands at the same time

interrupted = False
client_ip = '127.0.0.1' # to be changed to image pi 
sendport = 2002

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted

def send_command(command_num):
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_address = (client_ip, sendport)
    data = str(command_num)
    send_socket.sendto(data.encode('utf-8'), client_address)
    print("Command has been sent!\n")

def water_the_plant():
    print("=====Detected: water the plant=====")
    send_command(1);

def turn_on_the_light():
    print("=====Detected: turn on the light=====")
    send_command(2);

def turn_off_the_light():
    print("=====Detected: turn off the light=====")
    send_command(3);

models = ['resources/water_the_plant.pmdl', 'resources/turn_on_the_light.pmdl', 'resources/turn_off_the_light.pmdl']

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

sensitivity = [0.5]*len(models)
detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)

commands = [water_the_plant,turn_on_the_light,turn_off_the_light]
print('Listening... Press Ctrl+C to exit')


# main loop
# make sure you have the same numbers of callbacks and model
detector.start(detected_callback=commands,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()
