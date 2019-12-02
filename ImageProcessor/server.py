import socket, sys, time, datetime, json
from pathlib import Path
from ImageProcessor import ImageProcessor
from Camera import Camera
from ArduinoPlant import ArduinoPlant


class ImageServer:
    WATER_COMMAND = '0001'
    LIGHT_COMMAND = '0010'
    PLANTID_COMMAND = '0100'
    UPDATE_COMMAND = '0111'
    ACK = '01100001'
    NACK = '01101110'
    IDEN_INTERVAL = 5
    RETRIES = 5
    def __init__(self, send, recv, ard_port, baud=9600):
        print("Binding Server ... ")
        self.send_port = send
        self.recv_port = recv
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Start listening
        my_address = ('localhost', recv)
        self.s.bind(my_address)

        self.server_address = ('localhost', send)

        print("Setting up image processor ... ")
        # Set up image processing
        self.cam = Camera(True, Path("./data/imgs/plants/1/1-cc-0.jpg"))
        self.identifier = ImageProcessor(Path("./plant_model.pth"))
        print("Binding camera ... ")
        assert self.identifier._assign_camera(self.cam)

        print("Connecting to arduino ... ")
        self.arduino = ArduinoPlant(ard_port, baud)
    

    def run_server(self):
        """
        The main server loop
        """
        self.s.setblocking(0)
        last_checked_id = int(time.time())
        last_checked_conditions = int(time.time())
        while True:
            try:
                data, address = self.s.recv(1024)
                if self.process_command(data.decode()):
                    self.s.sento(self.ACK.encode("utf-8"), self.server_address)
                else:
                    self.s.sento(self.NACK.encode("utf-8"), self.server_address)
            except BlockingIOError:
                pass

            # Every n seconds we try to re-identify the plant, update the server when required
            if (int(time.time()) - last_checked_id) > self.IDEN_INTERVAL:
                last_checked_id = int(time.time())
                is_new = self.re_identify()
                if is_new:
                    self.update_plant_id()
            
            if (int(time.time()) - last_checked_conditions) > self.IDEN_INTERVAL:
                self.update_server()


    def wait_ack(self):
        # Set blocking and wait for ack before continuing, bad
        # practice but python cant do futures
        print("Waiting for ack")
        self.s.setblocking(1)
        data = self.s.recv(1024)
        self.s.setblocking(0)
        if data.decode() == self.NACK:
            print(f"NACK found ...")
            return False
        elif data.decode() == self.ACK:
            print("Got ack ...")
            return True
        else:
            print("Unkown return while waiting for ack")
            return False


    def update_plant_id(self) -> bool:
        """
        When the image processor detects a change in the current plant, we need
        to update the server
        """
        # Encode and send plant string
        print("Plant changed, updating server")
        plant_id_str = str(bin(self.identifier.currentPlant()))[2:].zfill(4)
        for i in range(self.RETRIES):
            self.s.sendto((self.UPDATE_COMMAND + plant_id_str).encode("utf-8"),
                            self.server_address)

            # Set blocking and wait for ack before continuing, bad
            # practice but python cant do futures
            if self.wait_ack():
                break
            print(f"Retrying {self.RETRIES-i}")
        else:
            return False

        return True


    def re_identify(self) -> bool:
        current_plant = self.identifier.currentPlant()
        self.identifier.resetDetected()
        return current_plant != self.identifier.currentPlant()


    def update_server(self) -> bool:
        """
        Called to update server with up to date data
        """
        conditions = self.arduino.updateData()
        if conditions == "error":
            print("Could not get updated data from arduino")
            return False
        else:
            for i in range(self.RETRIES):
                self.s.sento(conditions.encode("utf-8"),
                             self.server_address)
                if self.wait_ack():
                    break
                print(f"Retrying ... {self.RETRIES - i}")
            else:
                print("Max update retried exceeded ...")
                return False
        return True


    def process_command(self, data) -> bool:
        """
        Responsible for executing the commands recieved from the server
        """
        if data[:4] == self.WATER_COMMAND:
            print('Received water command.')  
            watered = self.arduino.waterPlant(int(data[4:], 2))
            if watered:
                self.s.sento(self.ACK.encode("utf-8"), self.server_address)
            else:
                self.s.sento(self.NACK.encode("utf-8"), self.server_address)        
                
        elif data[:4] == self.LIGHT_COMMAND:
            print('Received light command.')  
            light_set self.arduino.setLightLevel(int(data[4:], 2))
            if light_set:
                self.s.sento(self.ACK.encode("utf-8"), self.server_address)
            else:
                self.s.sento(self.NACK.encode("utf-8"), self.server_address)
        
        return False


if __name__ == "__main__":
    RECV_PORT = 9003
    SEND_PORT = 8001
    server = ImageServer(SEND_PORT, RECV_PORT)
    server.update_plant_id()