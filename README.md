# plant_squared
This is a picture of our project:)
![demo](https://github.com/Serena2766/plant_squared/blob/master/demo.jpg)

## Directories
Each part of this project was worked on in a different branch. Though there was some work done by others on those branches, each part was largely maintained by a single person, and can be considered a catalogue of thier contributions.
*Note: The app was developed in the FlutterApp branch, but due to a github issue, it could not be merged onto master. Please review the FlutterApp branch for the commit history of the app development.
## Authors
- Xinrui Zhang          - Serena2766
- Juan Pablo Contreras  - juanpablocontreras
- Jerry Xiong           - Jerry Xiong
- Xander May            - xmaayy         
## OpenCV
OpenCV needs to be installed on both the server and client Pi. There is no pre-built binary for this, so you're going to need to compile it yourself from source. The guide I followed can be found [here](https://www.pyimagesearch.com/2018/09/26/install-opencv-4-on-your-raspberry-pi/), though there are many faster ways to do it that take advantage of cross-compilation (build it on a normal computer for use on a pi). This build process can take upwards of 3-4 hours on a Pi4, so I'd recommend a good movie. 

## On the server pi:
#### Prepare to run the voice recognition
- run the follwing for [snowboy](http://docs.kitt.ai/snowboy/#running-on-raspberry-pi):
  ``` 
  sudo apt-get install libatlas-base-dev
  sudo apt-get install python-pyaudio python3-pyaudio sox
  pip install pyaudio
  sudo pip3 install --upgrade speechrecognition
  ```
- run the following for google speech to text API:
  ```
  git clone http://people.csail.mit.edu/hubert/git/pyaudio.git
  cd pyaudio
  sudo python setup.py install
  sudo apt-get installl libportaudio-dev
  sudo apt-get install python-dev
  sudo apt-get install libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev
  sudo pip install SpeechRecognition 
  sudo apt-get install flac
  ```
  
 
#### Ready to run
  ```
  python server/server_requestHandler.py
  python server/server_voice_control.py
  python ImageProcessing/stream_client.py
  ```
  
## On the client pi:
### Prepping
The client Pi requires PySerial, tqdm, numpy, and PyTorch be installed on it. The first three can be installed via:
```
pip install pyserial numpy tqdm
```
Pytorch must, at the time of my writing this, be built for your pi. I used the guide found [here](https://gist.github.com/fgolemo/b973a3fa1aaa67ac61c480ae8440e754) to do this, though I'm sure any guide for installing PyTorch would work. There are also some repositories which offer pre-built binaries, but because they are unofficial and unreliable I will not mention them here.

### Ready to run
```
python ImageProcessing/server.py
```

## On App:
  ```
The app could be run on Android Studio, but needs the Flutter plugin installed.
Note that for setting up the UDP connect, the values for the ports and IP addresses must be consistent with the Server.
The app can display
  -The Plant Type
  -A Main Image of the Plant based on Type
  -Ideal Conditions (Water level, Humidity, Temperature)
  -Current Conditions (Water level, Humidity, Temperature)
The app can execute
  -Data Update Requests (by clicking on the main image)
  -Water Commands (5 levels)
  -Light Commands (5 levels)
  -Data Reset
    ```
