int rightTriggerPIN = 13;
int rightEchoPIN = 12;
//right^

//left v
int leftTriggerPIN = 3;
int leftEchoPIN = 2;
void setup(){
  pinMode(rightTriggerPIN,OUTPUT);
  pinMode(rightEchoPIN,INPUT);
  pinMode(leftTriggerPIN,OUTPUT);
  pinMode(leftEchoPIN,INPUT);
  Serial.begin(9600); 
  }
void loop(){  
  digitalWrite(rightTriggerPIN,LOW);
  delayMicroseconds(2);
  digitalWrite(rightTriggerPIN,HIGH);
  delayMicroseconds(2);
  digitalWrite(rightTriggerPIN,LOW);
  long timedelay = pulseIn(rightEchoPIN,HIGH);
  int distance1 = 0.0343 * (timedelay/2);
  //Serial.print("Sensor 1 : ");
  //Serial.print(distance1);
  delayMicroseconds(2);
  digitalWrite(leftTriggerPIN,LOW);
  delayMicroseconds(2);
  digitalWrite(leftTriggerPIN,HIGH);
  delayMicroseconds(2);
  digitalWrite(leftTriggerPIN,LOW);
  long td = pulseIn(leftEchoPIN,HIGH);
  int distance2 = 0.0343 * (td/2);
  Serial.print("Left: ");
  Serial.print(distance2);
  Serial.print(" Right: ");
  Serial.print(distance1);
  Serial.println(" ");
}
