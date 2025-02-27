// Includes the Servo library
#include <Servo.h>. 
#include "TFMini.h"

// Variables for the duration and the distance
long duration;
int distance;

// Constructor
TFMini::TFMini() { 
  // Empty constructor
}

boolean TFMini::begin(Stream* _streamPtr) {
  // Store reference to stream/serial object
  streamPtr = _streamPtr;

  // Clear state
  distance = -1;
  strength = -1;
  state = READY;
  
  // Set standard output mode
  setStandardOutputMode();
  
  return true;
}


Servo myServo; // Creates a servo object for controlling the servo motor
TFMini tfmini;

void setup() {
 // pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  //pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  Serial.begin(9600);
  myServo.attach(12); // Defines on which pin is the servo motor attached
}
void loop() {
  // rotates the servo motor from 15 to 165 degrees
  for(int i=15;i<=165;i++){  
  myServo.write(i);
  delay(30);
  distance = calculateDistance();// Calls a function for calculating the distance measured by the Ultrasonic sensor for each degree
  
  Serial.print(i); // Sends the current degree into the Serial Port
  Serial.print(","); // Sends addition character right next to the previous value needed later in the Processing IDE for indexing
  Serial.print(distance); // Sends the distance value into the Serial Port
  Serial.print("."); // Sends addition character right next to the previous value needed later in the Processing IDE for indexing
  }
  // Repeats the previous lines from 165 to 15 degrees
  for(int i=165;i>15;i--){  
  myServo.write(i);
  delay(30);
  distance = calculateDistance();
  Serial.print(i);
  Serial.print(",");
  Serial.print(distance);
  Serial.println(".");
  }
}
// Function for calculating the distance measured by the Ultrasonic sensor
int calculateDistance(){ 
  uint16_t dist = tfmini.getDistance();
  return dist;
}
