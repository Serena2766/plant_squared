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


//initialize DHT 11 temperature and humidity sensor
DHT dht(DHTPIN, DHTTYPE);

//Global variables
int currentLightLevel = 0;
bool isPlantPresent = false;
bool wasPlantPresent = false;
byte command = 0;

//testing variables
int moistureValues[4] = {1020, 736, 322, 154};
int moistureValuesLength = 4;
int testNumber = 0; //determines the test that is to be performed
int iteration = 0; //current iteration of a test (tests are performed with each of the moisture values)

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

  //code implements arduino software flow chart on page 17 of design document

 /////////////////
 //// Tests //////
 /////////////////
 
 
 if(testNumber == 0){
  //test if plant is present
  Serial.println("Test name: testPlantDetectionWithStub");
  Serial.println("Testing the detection of a plant using a stub for the moisture sensor");
  
  bool expectedOutputs[4] = {false,true,true,true};  //Expected outputs of isPlantPresentFunc
  bool output;
  iteration = 0;
  
  while(iteration < moistureValuesLength){
   output = isPlantPresentFunc();
   Serial.print("input: ");
   Serial.print(moistureValues[iteration]);
   Serial.print("    Expected output: ");
   Serial.print(expectedOutputs[iteration]);
   Serial.print("     Output: ");
   Serial.print(output);

   if(output == expectedOutputs[iteration]){
    Serial.println("     SUCCESS");
   }else{
    Serial.println("     FAIL");
   }
   
   iteration++;
  }

  Serial.println("");
  Serial.println("");
  testNumber++; //increase test number so that next test is performed in next iteration of loop function
 }else if(testNumber == 1){
  //test moisture level reading
  float expectedOutputs[4] = {0.0, 26.4, 67.8, 84.6}; 
  float output;
  Serial.println("Test name: testMoistureLevelWithStub");
  Serial.println("Test reading and  calculating moisture levels using stub sensor values");
  iteration = 0;

  while(iteration < moistureValuesLength){
    output = getMoisture();
   Serial.print("input: ");
   Serial.print(moistureValues[iteration]);
   Serial.print("    Expected output: ");
   Serial.print(expectedOutputs[iteration]);
   Serial.print("     Output: ");
   Serial.print(output);

   if(output == expectedOutputs[iteration]){
    Serial.println("     SUCCESS");
   }else{
    Serial.println("     FAIL");
   }
   
   iteration++;
  }

  Serial.println("");
  Serial.println("");
  testNumber++; //increase test number so that next test is performed in next iteration of loop function
 }else if (testNumber == 2){
  //test command UpdateData with stub values

  Serial.println("Test name: testUpdateDataCommandWithStubs");
  Serial.println("Test commmand: updateData. Stub used for moisture sensor. Success/failure determined only by moisture value");
  float expectedOutputs[4] = {0.0, 26.4, 67.8, 84.6}; 
  
  iteration = 0;
  while(iteration < moistureValuesLength){
    isPlantPresent = true; //isPlantPresentFunc(); //set plant detected to true for the tests

    //get and perform command
    if(true/*Serial.available() > 0*/){ //commands are always available when testing
      //There is at least one command available
  
      command = B01110000;//Serial.read(); //replace reading from serial to stub value
  
      //perform command if the plant is present
      if(isPlantPresent){
  
        //decipher command
        if(command == B01110000){
          //update data: read and send data from all the sensors
          String serialMessage = "{";
          String expectedMessage = "{";
          
          //expected message
          expectedMessage += "\"moisture\":" + String(expectedOutputs[iteration],1) + ",";
          expectedMessage += "\"temperature\":" + String(getTemperature(),2) + ",";
          expectedMessage += "\"humidity\":" + String(getHumidity(),2) + ",";
          expectedMessage += "\"lightLevel\":" + String(currentLightLevel);
          expectedMessage += "}";
          
          //output message
          float moisture = getMoisture();
          serialMessage += "\"moisture\":" + String(moisture,1) + ",";
          serialMessage += "\"temperature\":" + String(getTemperature(),2) + ",";
          serialMessage += "\"humidity\":" + String(getHumidity(),2) + ",";
          serialMessage += "\"lightLevel\":" + String(currentLightLevel);
          serialMessage += "}";
          
          Serial.print("input: ");
          Serial.println(moistureValues[iteration]);
          Serial.print("Expected output: ");
          Serial.println(expectedMessage);
          Serial.print("output:          ");
          Serial.println(serialMessage);
          

          if(moisture == expectedOutputs[iteration]){
            Serial.println("SUCCESS");
           }else{
            Serial.println("FAIL");
           }
          Serial.println("");
          
        }else if(command >> 4 == B00000001){
          //water the plant, command = 0001 0+amount(3bits)
          //acknowledgment needed
          
          byte amount = command - B00010000;
          waterPlant(amount);
          Serial.println("a");
          
        }else if(command >> 5 == B00000001){
          //set light level 
          //acknowledgment needed
          
          byte level = command - B00100000;
          setLightLevel(level);
          Serial.println("a");
        }else{
          //command not found
          //Serial.println("{\"error\":command not found} ");
        }
        
      }else{
        //command is received from client Raspberry PI, but the plant is not in the system. 
        //send error message
        Serial.println("{\"error\":command was received but plant is not in the system}");
      
      }//end if plant is present
    }//end if serial is available

    iteration++;
  }
  
  testNumber++; //increase test number so that next test is performed in next iteration of loop function
 }else {
  Serial.println("No more tests to perform using a stub");
  delay(60000);
 }

}//end loop



////////////////////////
/////// Functions  /////
////////////////////////

float getMoisture() {
  //Stub for moisture sensor
  
  int sensorRead; //= analogRead(moisturePin); //commented out to serve as stub
  
  switch (iteration){
    case 0:
      sensorRead = moistureValues[0];
      break;
    case 1:
      sensorRead = moistureValues[1];
      break;
    case 2:
      sensorRead = moistureValues[2];
      break;
    case 3:
      sensorRead = moistureValues[3];
      break;  
    default:
      sensorRead = 1000;
      break;  
  }

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
    delay(1000);
    amount--;
  }

  digitalWrite(waterPin,LOW);
  
}
