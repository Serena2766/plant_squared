# plant_squared
This is a picture of our project:)
![demo](https://github.com/Serena2766/plant_squared/blob/master/demo.jpg)
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
  python server_requestHandler.py
  python server_voice_control.py
  ```
