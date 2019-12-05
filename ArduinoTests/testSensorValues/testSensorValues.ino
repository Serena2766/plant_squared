#define moisturePin A0 // A0 for moisture sensor data

int sensorRead = 0;

void setup() {
  // put your setup code here, to run once:
  pinMode(moisturePin,INPUT);

  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  
  sensorRead = analogRead(moisturePin);
  
  Serial.print("sensor value: ");
  Serial.println(sensorRead);
  delay(1000);
  
}


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
