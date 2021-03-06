import serial
import time
import io

class ArduinoPlant:
    MAX_WATER_LEVEL = 5
    MAX_LIGHT_LEVEL = 5
    MIN_LEVEL = 0
    MIN_MESSAGE_LENGTH = 50
    
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self.serialConnection = serial.Serial(
            port=port,
            baudrate = baudrate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        self.sio = io.TextIOWrapper(io.BufferedRWPair(self.serialConnection, self.serialConnection))


    def waterPlant(self, amount):
        #sends command to arduino to water the plant
        #amount has to be between 0 and 5
        if amount == 0:
            return True
        
        amount = ArduinoPlant.check_and_convert_amount(amount,ArduinoPlant.MIN_LEVEL, ArduinoPlant.MAX_WATER_LEVEL)
        intCommand = 16 + amount
        command = bytes([intCommand])
        return self.sendCommandWaitAck(command)
    
    
    def setLightLevel(self, amount):
        #sends command to arduino to set the light level
        #amount has to be between 0 and 5
        
        amount = ArduinoPlant.check_and_convert_amount(amount,ArduinoPlant.MIN_LEVEL, ArduinoPlant.MAX_WATER_LEVEL)
        intCommand = 32 + amount
        command = bytes([intCommand])
        return self.sendCommandWaitAck(command)
    
    
   
   
    def updateData(self, numTries = 5):
        self.emptyBuffer()
        
        #send command and wait for ack
        commandReceived = False
        tries = numTries
        while(tries > 0 and commandReceived == False):
            self.serialConnection.write(b'\x70')
            time.sleep(1)
            if self.serialConnection.in_waiting > 0:
                if self.serialConnection.read() == b'a':
                    commandReceived = True
            tries -= 1
            
        #self.emptyBuffer()
        #if arduino sent ack, read line
        tries = numTries
        if(commandReceived):         
            for i in range(tries):
                if self.serialConnection.in_waiting < ArduinoPlant.MIN_MESSAGE_LENGTH:
                    time.sleep(5)
                    
            if self.serialConnection.in_waiting > ArduinoPlant.MIN_MESSAGE_LENGTH:
                message = ""
                while(self.serialConnection.in_waiting > 0):
                    nextByte = self.serialConnection.read().decode()
                    if(nextByte == '{'):
                        message += "{"
                        message += self.serialConnection.readline().decode()
                        return message

        return "error"

        
    
    def sendCommandWaitAck(self, command, numTries = 10):
        #tries to send the command to the arduino
        #
        #After command is sent,
        #if ack is received, function returns
        #if ack is not received, try again up to numTries
        #returns true if ack was received, fase if all tries failed
        #try the command up to 10 times
        
        self.emptyBuffer()
        isAckFound = False
        for i in range(numTries):
            self.serialConnection.write(command)
            time.sleep(1)
            
            if self.serialConnection.in_waiting > 0:
                response = self.serialConnection.read()
                if response == b'a':
                    isAckFound = True
        
        self.emptyBuffer()
        return isAckFound
        
    
    
    
    def check_and_convert_amount(amount, minimum, maximum):
        #checks that the amount is minimum <= amount <= maximum
        #if amount is less than minimum, amount is set to minimum
        #if amount is more thann maximum, amount set to maximum
        if amount < minimum:
            amount = minimum
        elif amount > maximum:
            amount = maximum
        
        return amount


    def emptyBuffer(self):
        while(self.serialConnection.in_waiting > 0):
            self.serialConnection.read()
        return

if __name__ == "__main__":
    arduino = ArduinoPlant("/dev/ttyACM0",9600)
    
    print("watering plant...")
    if arduino.waterPlant(5):
        print("plant watered")
         
    print("setting light level...")
    if arduino.setLightLevel(5):
        print("light level set")
     
    
    print("getting updated data...")
    response = arduino.updateData()
    print(response)
        
        
