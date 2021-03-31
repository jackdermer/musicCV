int prev = HIGH;

void setup() {
   pinMode(5, OUTPUT);
   pinMode(6, OUTPUT);
   pinMode(7, OUTPUT);
   pinMode(A0, INPUT);
   Serial.begin(9600);
}
 

void loop() {
  int state = digitalRead(A0);
  if(state==1) {
    Serial.print(state);
     analogWrite(5, 255);
  } else {
    analogWrite(5, 0);
  }
  
//  analogWrite(5, 255);
//  delay(200);
//  analogWrite(5, 0);
//  analogWrite(6, 255);
//  delay(200);
//  analogWrite(6, 0);
//  analogWrite(7, 255);
//  delay(200);
//  analogWrite(7, 0);
}
