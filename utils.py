# utils.py
import sys

# Mock RPi.GPIO if not on a Raspberry Pi (e.g., Windows development)
try:
    import RPi.GPIO as GPIO
except (ImportError, RuntimeError):
    import mock_gpio as GPIO
    print("WARNING: Using mock GPIO because RPi.GPIO is not available.")

# Configuration
FLASK_PORT = 5000
FLASK_HOST = "0.0.0.0"

# Arduino Serial Configuration
# For Linux (Pi): '/dev/ttyACM0' or '/dev/ttyUSB0'
# For Windows: 'COM3', 'COM4', etc.
SERIAL_PORT = '/dev/ttyACM0' 
BAUD_RATE = 115200 # Higher baud rate for responsive controls

# Motor GPIO Pins (L298N)
MOTOR_IN1 = 17
MOTOR_IN2 = 27
MOTOR_IN3 = 22
MOTOR_IN4 = 23
MOTOR_ENA = 18
MOTOR_ENB = 24

# Servo GPIO Pin (Robotic Arm)
SERVO_PIN = 25

# Setup function
def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    # Setup motor pins
    for pin in [MOTOR_IN1, MOTOR_IN2, MOTOR_IN3, MOTOR_IN4, MOTOR_ENA, MOTOR_ENB]:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
        
    # Setup servo pin
    GPIO.setup(SERVO_PIN, GPIO.OUT)

def cleanup_gpio():
    GPIO.cleanup()

# Serial Communication Helpers
import serial
import threading

_arduino_lock = threading.Lock()
_arduino_serial = None

def get_arduino_serial():
    global _arduino_serial
    with _arduino_lock:
        if _arduino_serial is None:
            try:
                _arduino_serial = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
                import time
                time.sleep(2) # Wait for Arduino to reset
            except Exception as e:
                # For development on Windows without Arduino, mock the serial object
                class MockSerial:
                    def write(self, data): pass
                    def close(self): pass
                _arduino_serial = MockSerial()
        return _arduino_serial

def safe_write_serial(data):
    """Thread-safe writing to Arduino serial port"""
    arduino = get_arduino_serial()
    with _arduino_lock:
        try:
            if hasattr(arduino, 'write'):
                arduino.write(data)
        except Exception as e:
            print(f"Serial write error: {e}")
