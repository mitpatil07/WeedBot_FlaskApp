// =============================================
//   4WD Rover - BTS7960 + HC-05 Bluetooth
//   Arduino Mega
// =============================================

// --- Left Motor Driver (BTS7960 #1) ---
#define L_RPWM  2     // Forward PWM
#define L_LPWM  3     // Backward PWM
#define L_R_EN  22    // Right Enable
#define L_L_EN  23    // Left Enable

// --- Right Motor Driver (BTS7960 #2) ---
#define R_RPWM  4     // Forward PWM
#define R_LPWM  5     // Backward PWM
#define R_R_EN  24    // Right Enable
#define R_L_EN  25    // Left Enable

// --- Speed (0–255) ---
int driveSpeed  = 50;   // Straight driving speed
int turnSpeed   = 100;   // Turning speed

void setup() {
  // Enable pins
  pinMode(L_R_EN, OUTPUT); pinMode(L_L_EN, OUTPUT);
  pinMode(R_R_EN, OUTPUT); pinMode(R_L_EN, OUTPUT);

  // PWM pins
  pinMode(L_RPWM, OUTPUT); pinMode(L_LPWM, OUTPUT);
  pinMode(R_RPWM, OUTPUT); pinMode(R_LPWM, OUTPUT);

  // Activate both drivers
  digitalWrite(L_R_EN, HIGH); digitalWrite(L_L_EN, HIGH);
  digitalWrite(R_R_EN, HIGH); digitalWrite(R_L_EN, HIGH);

  // Start stopped
  stopMotors();

  // HC-05 on Serial1 (pins 18/19)
  Serial1.begin(9600);
  Serial.begin(9600); // Optional: USB debug monitor
}

void loop() {
  // Listen for Bluetooth commands
  if (Serial1.available()) {
    char cmd = (char)Serial1.read();
    processCommand(cmd);
  }
  
  // Listen for USB Cable commands
  if (Serial.available()) {
    char cmd = (char)Serial.read();
    processCommand(cmd);
  }
}

void processCommand(char cmd) {
    Serial.print("CMD USB/BT: "); Serial.println(cmd);

    switch (cmd) {
      case 'F': moveForward();  break;
      case 'B': moveBackward(); break;
      case 'L': turnLeft();     break;
      case 'R': turnRight();    break;
      case 'S': stopMotors();   break;
      default:  break; // ignore unknown commands
    }
}

// =============================================
//   Motor Control Functions
// =============================================

// Both sides forward
void moveForward() {
  analogWrite(L_RPWM, driveSpeed); analogWrite(L_LPWM, 0);
  analogWrite(R_RPWM, driveSpeed); analogWrite(R_LPWM, 0);
}

// Both sides backward
void moveBackward() {
  analogWrite(L_RPWM, 0); analogWrite(L_LPWM, driveSpeed);
  analogWrite(R_RPWM, 0); analogWrite(R_LPWM, driveSpeed);
}

// Left side backward, right side forward -> pivot left
void turnLeft() {
  analogWrite(L_RPWM, 0);         analogWrite(L_LPWM, turnSpeed);
  analogWrite(R_RPWM, turnSpeed); analogWrite(R_LPWM, 0);
}

// Left side forward, right side backward -> pivot right
void turnRight() {
  analogWrite(L_RPWM, turnSpeed); analogWrite(L_LPWM, 0);
  analogWrite(R_RPWM, 0);         analogWrite(R_LPWM, turnSpeed);
}

// All stop
void stopMotors() {
  analogWrite(L_RPWM, 0); analogWrite(L_LPWM, 0);
  analogWrite(R_RPWM, 0); analogWrite(R_LPWM, 0);
}
