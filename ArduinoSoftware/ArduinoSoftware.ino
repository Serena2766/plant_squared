//libraries
#include "DHT.h" //DHT library


//PIN definitions
#define DHTPIN 2     // Digital pin connected to the DHT sensor
#define DHTTYPE DHT22   // DHT 22  (AM2302), AM2321

//initialize DHT 11 temperature and humidity sensor sensor
DHT dht(DHTPIN, DHTTYPE);

//Global variables
int currentLightLevel;
bool isPlantPresent = false;
bool wasPlantPresent = false;
byte command = 0;
String serialMessage; //defined as global variable so arduino to reduce allocated memory

void setup() {

  //begin serial communication
  Serial.begin(9600);

  //set A0 to analogue input for moisture sensor data
  pinMode(A0, INPUT); 

  //begin DHT readings
  dht.begin(); 
  
}

void loop() {

  //code implements arduino software flow chart on page 17 of design document

 //recognize if plant is present and set isPlant Present variable
 isPlantPresent = isPlantPresentFunc();

 if(isPlantPresent != wasPlantPresent){
  //state of plant has changesd (either the plant was added or removed from system)
  
  //send isPlantPresdent to client raspberry Pi
  serialMessage = String("{\"isPlantPresent\" : ") + String(isPlantPresent) + String("}");
  Serial.println(serialMessage);

  //set wasPlantPresent to current value of isPlantPresent
  wasPlantPresent = isPlantPresent;
 }

 
  //get and perform command
  if(Serial.available() > 0){
    //command available

    command = Serial.read(); //read command and remove byte from buffer. if there is no plant command will be discarded anyway

    //perform command if the plant is present
    if(isPlantPresent){

      //decipher command
      if(command == B01110000){
        
        //read and send data from all the sensors
        Serial.println("all data");
        
      }else if(command >> 4 == B00000001){
        
        //water the plant command = 0001 0+amount(3bits)
        byte amount = command - B00010000;
         
        Serial.print("water plant ");
        Serial.println(amount);
        
      }else if(command >> 5 == B00000001){
        
        //set light level 
        byte amount = command - B00100000;
        
        Serial.print("set light level ");
        Serial.println(amount);
      }else{
        //command not found
        Serial.print("{\"error\":command not found} ");
      }

      Serial.print("command: ");
      Serial.println(command);
      
    }else{
      //command is received from client Raspberry PI, but the plant is not in the system. 
      //send error message
      Serial.println("{\"error\":command was received but plant is not in the system}");
    }
  }

}


double getMoisture() {
  return 0;
}

double getTemperature(){
  return 0;
}

double getHumidity(){
 return 0;
}


int getLightLevel(){
  return 0;
}

void setLightLevel(int level){
  
}

bool isPlantPresentFunc(){
  return true;
}

void waterPlant(){
  
}
