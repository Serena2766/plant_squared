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
bool wasPlantPresent = true;
byte command = 0;
String serialMessage; //defined as global variable so arduino to reduce allocated memory

void setup() {

  //begin serial communication
  Serial.begin(9600);

  //set A0 to analogue input for moisture sensor output
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
  return false;
}
