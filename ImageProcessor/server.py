import socket, sys, time, datetime, json, cv2, pickle, zlib, struct
from pathlib import Path
from ImageProcessor import ImageProcessor
from Camera import Camera
from ArduinoPlant import ArduinoPlant


class ImageServer:
    """image server is responsible for sending data to both the servers
    plant management database as well as the video streaming service
    """
    WATER_COMMAND = '0001'
    LIGHT_COMMAND = '0010'
    PLANTID_COMMAND = '0100'
    UPDATE_COMMAND = '0111'
    ACK = '01100001'
    NACK = '01101110'
    IDEN_INTERVAL = 30
    RETRIES = 5
    ENCODING = [int(cv2.IMWRITE_JPEG_QUALITY), 90] # Quality affects stream rate

    def __init__(self, send, recv, stream=1337, ard_port="/dev/ttyACM0", baud=9600):
        print("Binding Server Ports ... ")
        self.send_port = send
        self.recv_port = recv
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        print("Binding video streaming service")
        self.stream_port = stream
        self.stream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.stream.connect(("localhost", self.stream_port))
        self.connection = self.stream.makefile("wb")

        # Start listening
        my_address = ('localhost', recv)
        self.s.bind(my_address)

        self.server_address = ('localhost', send)

        print("Setting up image processor ... ")
        # Set up image processing
        #self.cam = Camera(True, Path("./data/imgs/plants/1/1-cc-0.jpg"))
        self.cam = Camera()
        self.identifier = ImageProcessor(Path("./plant_model.pth"))

        print("Binding camera ... ")
        assert self.identifier._assign_camera(self.cam)

        print("Connecting to arduino ... ")
        try:
            self.arduino = ArduinoPlant(ard_port, baud)
        except:
            print("Arduino not found")
            self.arduino = None


    def stream_frame(self) -> int:
        """Encodes and streams one frame to the client
        
        :return: The time it took to encode and stream the frame in s
        """
        start_time = time.time()
        frame = self.cam.requestData()
        res, frame = cv2.imencode(".jpg", frame, self.ENCODING)
        frame_data = pickle.dumps(frame, 0)
        size = len(frame_data) # We need this to tell the client how far to read

        self.stream.sendall(struct.pack(">L", size) + frame_data)
        return time.time() - start_time
    

    def run_server(self):
        """
        The main server loop
        """
        print("Running Server")
        self.s.setblocking(0)
        last_checked_id = int(time.time())
        last_checked_conditions = int(time.time())
        last_cmd = int(time.time())
        while True:
            try:
                data, address = self.s.recvfrom(1024)
                if self.process_command(data.decode()):
                    self.s.sendto(self.ACK.encode("utf-8"), self.server_address)
                else:
                    self.s.sendto(self.NACK.encode("utf-8"), self.server_address)
            except BlockingIOError:
                pass


            if (int(time.time()) - last_cmd) > self.IDEN_INTERVAL: # Space cmds by 60 s
                if (int(time.time()) - last_checked_id) >= ((time.time()) - last_checked_conditions):
                    print("Re-identifying plant")
                    last_checked_id = int(time.time())
                    is_new = self.re_identify()
                    if is_new:
                        self.update_plant_id()
                else:
                    print("Sending condition update to server")
                    self.update_server()
                    last_checked_conditions = int(time.time())
                    
                last_cmd = int(time.time())
            
            self.stream_frame()


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
            print(data)
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
        print("Done updating plant id")
        return True


    def re_identify(self) -> bool:
        current_plant = self.identifier.currentPlant()
        self.identifier.resetDetected()
        return current_plant != self.identifier.currentPlant()


    def update_server(self) -> bool:
        """
        Called to update server with up to date data
        """
        try:
            conditions = self.arduino.updateData()
        except:
            print("Update server could not access arduino")
            return False
        print(conditions)
        if conditions == "error":
            print("Could not get updated data from arduino")
            return False
        else:
            for i in range(self.RETRIES):
                self.s.sendto(conditions.encode("utf-8"),
                              self.server_address)
                if self.wait_ack():
                    break
                print(f"Retrying ... {self.RETRIES - i}")
            else:
                print("Max update retried exceeded ...")
                return False
        print("Done updating server")
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
            light_set = self.arduino.setLightLevel(int(data[4:], 2))
            if light_set:
                self.s.sento(self.ACK.encode("utf-8"), self.server_address)
            else:
                self.s.sento(self.NACK.encode("utf-8"), self.server_address)
        
        return False


if __name__ == "__main__":
    RECV_PORT = 9003
    SEND_PORT = 8001
    server = ImageServer(SEND_PORT, RECV_PORT)
    server.run_server()