
#include <Servo.h>

// L298N Motor Driver Pins
const int MOTOR_IN1 = 2;
const int MOTOR_IN2 = 3;
const int MOTOR_IN3 = 4;
const int MOTOR_IN4 = 5;
const int MOTOR_ENA = 6;
const int MOTOR_ENB = 7;

// Servo Pin
const int SERVO_PIN = 9;
Servo roboticArm;

void setup() {
  Serial.begin(115200);
  
  // Setup Motor Pins
  pinMode(MOTOR_IN1, OUTPUT);
  pinMode(MOTOR_IN2, OUTPUT);
  pinMode(MOTOR_IN3, OUTPUT);
  pinMode(MOTOR_IN4, OUTPUT);
  pinMode(MOTOR_ENA, OUTPUT);
  pinMode(MOTOR_ENB, OUTPUT);
  
  // Setup Servo
  roboticArm.attach(SERVO_PIN);
  roboticArm.write(90); // Center position
  
  Serial.println("WeedBot Arduino Ready");
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    parseCommand(command);
  }
}

void parseCommand(String cmd) {
  cmd.trim();
  if (cmd.length() == 0) return;

  char type = cmd.charAt(0);
  
  if (type == 'M') {
    // Format M:DIR:SPD
    int firstColon = cmd.indexOf(':');
    int secondColon = cmd.indexOf(':', firstColon + 1);
    
    if (firstColon != -1 && secondColon != -1) {
      String dir = cmd.substring(firstColon + 1, secondColon);
      int speed = cmd.substring(secondColon + 1).toInt();
      controlMotors(dir, speed);
    }
  } 
  else if (type == 'A') {
    // Format A:ANGLE
    int colon = cmd.indexOf(':');
    if (colon != -1) {
      int angle = cmd.substring(colon + 1).toInt();
      roboticArm.write(angle);
    }
  }
}

void controlMotors(String dir, int speed) {
  int pwm = map(speed, 0, 100, 0, 255);
  
  if (dir == "FWD") {
    digitalWrite(MOTOR_IN1, HIGH); digitalWrite(MOTOR_IN2, LOW);
    digitalWrite(MOTOR_IN3, HIGH); digitalWrite(MOTOR_IN4, LOW);
  } else if (dir == "BWD") {
    digitalWrite(MOTOR_IN1, LOW);  digitalWrite(MOTOR_IN2, HIGH);
    digitalWrite(MOTOR_IN3, LOW);  digitalWrite(MOTOR_IN4, HIGH);
  } else if (dir == "LFT") {
    digitalWrite(MOTOR_IN1, LOW);  digitalWrite(MOTOR_IN2, HIGH);
    digitalWrite(MOTOR_IN3, HIGH); digitalWrite(MOTOR_IN4, LOW);
  } else if (dir == "RGT") {
    digitalWrite(MOTOR_IN1, HIGH); digitalWrite(MOTOR_IN2, LOW);
    digitalWrite(MOTOR_IN3, LOW);  digitalWrite(MOTOR_IN4, HIGH);
  } else { // STP or any other
    digitalWrite(MOTOR_IN1, LOW); digitalWrite(MOTOR_IN2, LOW);
    digitalWrite(MOTOR_IN3, LOW); digitalWrite(MOTOR_IN4, LOW);
    pwm = 0;
  }
  
  analogWrite(MOTOR_ENA, pwm);
  analogWrite(MOTOR_ENB, pwm);
}
