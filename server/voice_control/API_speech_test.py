#author Xinrui Zhang

#short testing code
import speech_recognition as sr 
box_name = ['box one', 'lovely']

r = sr.Recognizer() 
    
with sr.Microphone() as source:
    try:
        print("Please say the box name:")                                                                                  
        audio = r.listen(source) 
        text = r.recognize_google(audio)
        print("You said " + text)
        if text in box_name:
            print('Please say a command you want to send to'+ text)        
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
