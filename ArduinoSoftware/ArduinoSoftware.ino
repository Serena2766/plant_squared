//libraries
#include "DHT.h" //temperature and humidity sensor library


//definitions
#define DHTPIN 2     // Digital pin connected to the DHT sensor
#define DHTTYPE DHT11   // DHT 11
#define ledPin 3  //defines pin 3 as pin for LED lights
#define brightnessIncrement 36  //One brightness levl increment. Each brightness level is 36 units, or about 14% duty cycle
#define moisturePin A0 // A0 for moisture sensor data
#define moistureTRS 5 //minimum moisture percentage for plant to be detected
#define waterPin 4  //pin 4 used for watering plant


//initialize DHT 11 temperature and humidity sensor sensor
DHT dht(DHTPIN, DHTTYPE);

//Global variables
int currentLightLevel = 0;
bool isPlantPresent = false;
byte command = 0;

void setup() {

  //begin serial communication
  Serial.begin(9600);

  //set pins
  pinMode(moisturePin, INPUT); 
  pinMode(ledPin,OUTPUT);
  pinMode(waterPin, OUTPUT);
  
  //begin DHT temp and humidity sensor
  dht.begin(); 
  
}

void loop() {

  //this code implements arduino software flow chart on page 17 of design document


 isPlantPresent = isPlantPresentFunc();

  //get and perform command
  if(Serial.available() > 0){
    //There is at least one command available

    command = Serial.read(); //read command and remove byte from buffer. if there is no plant command will be discarded anyway

    //perform command if the plant is present
    if(isPlantPresent){

      //decipher command
      if(command == B01110000){
        //update data: read and send data from all the sensors

        Serial.print("a");
        String serialMessage = "{";
        
        serialMessage += "\"moisture\":" + String(getMoisture(),1) + ",";
        serialMessage += "\"temperature\":" + String(getTemperature(),2) + ",";
        serialMessage += "\"humidity\":" + String(getHumidity(),2) + ",";
        serialMessage += "\"lightLevel\":" + String(currentLightLevel);
        
        serialMessage += "}\n";
        Serial.print(serialMessage);
        
      }else if(command >> 4 == B00000001){
        //water the plant, command = 0001 0+amount(3bits)
        //acknowledgment needed
        
        byte amount = command - B00010000;
        waterPlant(amount);
        Serial.print("a");
        
      }else if(command >> 5 == B00000001){
        //set light level 
        //acknowledgment needed
        
        byte level = command - B00100000;
        setLightLevel(level);
        Serial.print("a");
      }else{
        //command not found
        //Serial.println("{\"error\":command not found} ");
      }
      
    }else{
      //command is received from client Raspberry PI, but the plant is not in the system. 
      //send error message
      Serial.print("{\"error\":command was received but plant is not in the system}\n");
    
    }//end if plant is present
  }//end if serial is available

}//end loop

float getMoisture() {
  //returns a float with 1 decimal representing the moisture percentage

  int sensorRead = analogRead(moisturePin);
  float moisture;
  
  //set maximum to 1000, greater means disconnected
  if(sensorRead >= 1000){
    moisture = 0.00;
  }else{
    moisture = (float)(1000 - sensorRead)/10.00;
  }
  
  return moisture;
}

float getTemperature(){
  //returns the temperature with 2 decimals
  float temp = dht.readTemperature(); //read temperature in celsius

  if(isnan(temp)){
    return -100.00;
  }
  
  return temp;
}

float getHumidity(){
  //returns humidity as a float with 2 decimals
  float humidity = dht.readHumidity();

  if(isnan(humidity)){
    return -100.00;
  }
  
  return humidity;
}

void setLightLevel(byte level){
  //use PWM to set the level of light brightness for LEDs
  //3 left most bytes provide 7 levels
  
  int brightness = 0; // pwm value between 0 to 255 (0% to 100% duty cycle)
  
  if(level > B00000111){
    //if level is more than maximum, set it to the maximum level
    level = B00000111; 
  }

  //set global variable light level
  currentLightLevel = level;
  
  //increase brightness variable
  while(level > 0){
    brightness += brightnessIncrement;
    level--;
  }

  //turn on LED to desired brightness
  analogWrite(ledPin,brightness);
}

bool isPlantPresentFunc(){
  //determines if there is a plant in the box by checking the moisture level
  float moisture = getMoisture();

  if(moisture < moistureTRS){
    //minimum moisture accepted in not met, plant is not connected to the system
    return false;
  }
  
  return true;
}

void waterPlant(byte amount){
  //water the plant of "amount" of seconds
  //amount is between 0 and 7, represented by the left most 3 bits of byte amount

  if(amount == 0){
    return;
  }else if(amount > 7){
    amount = 7; //set maximum to 7
  }


  while(amount > 0){
    digitalWrite(waterPin,HIGH);
    delay(100);
    amount--;
  }

  digitalWrite(waterPin,LOW);
  
}
