#author Xinrui Zhang
import snowboydecoder
import sys, socket, time
import signal
import speech_recognition as sr
ACK = '01100001'
NACK = '01101110'
interrupted = False
server_ip = '127.0.0.1'
server_port = int(8001)
server_address = (server_ip,server_port)
my_port = int(8888)
my_ip = 'localhost'
my_address = (my_ip, my_port)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
box_name = ['box one', 'my lovely flower','cauliflower']
s.bind(my_address)

def instruction():
    '''print out instructions'''
    print('Please say one of the following command to active the plant squared')
    print('-Water the plant')
    print('-Turn on the light')
    print('-Turn off the light\n')

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted

def active_google_s2t():
    '''active google speech API to identify the box name'''
    print("---Google speech2text activated---")
    # Activate Google speech recognize
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            print("Please say the box name:")
            audio = r.listen(source)
            text = r.recognize_google(audio)
            print("You said " + text)
            #send the command only if the box exists
            if text in box_name:
                print('Processing to send to '+ text)
                return 1
            return 0
        except sr.UnknownValueError:
            print("Could not understand audio\n")
            return 0
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            return 0

def send_command(command_num, amount):
    #to be test
    # send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # address = (server_ip, server_port)
    # data = command_num + amount
    # send_socket.sendto(data.encode('utf-8'), address)
    ''' send respective commands to the server system
        para command_num: the command code
        para amount: the amount in bits
    '''
    data = command_num + amount
    s.sendto(data.encode('utf-8'), server_address)
    print("Send to the server!")
    s.settimeout(8)
    try :
        data, address = s.recvfrom(1024)
        if data == ACK:
            print('Received ACK')
        elif data == NACK:
                print('Received NACK')
    except :
        print('Something wrong with the server')
    s.settimeout(None)


def water_the_plant():
    '''water the plant callback function'''
    print("=====Detected: water the plant=====")
    if active_google_s2t():
        send_command('0001','0001')
    else:
        print('Cannot find the box\n')
        instruction()

def turn_on_the_light():
    '''turn on the light callback function'''
    print("=====Detected: turn on the light=====")
    if active_google_s2t():
        send_command('0010','0001')
    else:
        print('Cannot find the box\n')
        instruction()

def turn_off_the_light():
    '''turn off the light callback function'''
    print("=====Detected: turn off the light=====")
    if active_google_s2t():
        send_command('0010','0000')
    else:
        print('Cannot find the box\n')
        instruction()

models = ['resources/water_the_plant.pmdl', 'resources/turn_on_the_light.pmdl', 'resources/turn_off_the_light.pmdl']
# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)
sensitivity = [0.5]*len(models)
#initialize a snowboy detector with specified models
detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)
commands = [water_the_plant,turn_on_the_light,turn_off_the_light]
print('\nListening... Press Ctrl+C to exit')
instruction()

# main loop
# if detected one of the commands then call the respective callback function
detector.start(detected_callback=commands,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()
