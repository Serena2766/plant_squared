import snowboydecoder
import sys, socket, time
import signal
import speech_recognition as sr 

interrupted = False
client_ip = '127.0.0.1' # to be changed to image pi 
sendport = 2002
box_name = ['box one', 'my lovely flower']

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted
    
def active_google_s2t():
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
            print("Could not understand audio")
            return 0
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            return 0

def send_command(command_num, amount):
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_address = (client_ip, sendport)
    data = str(command_num + amount)
    send_socket.sendto(data.encode('utf-8'), client_address)
    print("Command has been sent!\n")

def water_the_plant():
    print("=====Detected: water the plant=====")
    if active_google_s2t():
        send_command('0001','0001')
    else:
        print('Cannot find the box')
    
def turn_on_the_light():
    print("=====Detected: turn on the light=====")
    if active_google_s2t():
        send_command('0010','0001')
    else:
        print('Cannot find the box')

def turn_off_the_light():
    print("=====Detected: turn off the light=====")
    if active_google_s2t():
        send_command('0010','0000')
    else:
        print('Cannot find the box')

models = ['resources/water_the_plant.pmdl', 'resources/turn_on_the_light.pmdl', 'resources/turn_off_the_light.pmdl']

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

sensitivity = [0.5]*len(models)
detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)

commands = [water_the_plant,turn_on_the_light,turn_off_the_light]
print('\nListening... Press Ctrl+C to exit')
print('Please say one of the following command to active the plant square')
print('-Water the plant')
print('-Turn on the light')
print('-Turn off the light')

# main loop
# if detected one of the commands then call the respective callback function
detector.start(detected_callback=commands,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()
