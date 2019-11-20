

void setup() {
  // put your setup code here, to run once:
  pinMode(3,OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  analogWrite(3,100);
  delay(1000);
  analogWrite(3,200);
  delay(1000);
  analogWrite(3,255);
  delay(1000);
  
}
