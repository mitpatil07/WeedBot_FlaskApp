import time
from utils import get_arduino_serial

class MotorController:
    def __init__(self):
        self.arduino = get_arduino_serial()
        self.current_speed = 100

    def forward(self, speed=None):
        if speed is not None: self.current_speed = speed
        self._send_command('F')

    def backward(self, speed=None):
        if speed is not None: self.current_speed = speed
        self._send_command('B')

    def left(self, speed=None):
        if speed is not None: self.current_speed = speed
        self._send_command('L')

    def right(self, speed=None):
        if speed is not None: self.current_speed = speed
        self._send_command('R')

    def stop(self):
        self._send_command('S')
        
    def set_speed(self, speed):
        self.current_speed = speed
        # The Arduino code handles speed internally, but we can store it here just in case.

    def _send_command(self, cmd_char):
        from utils import safe_write_serial
        safe_write_serial(cmd_char.encode())

    def cleanup(self):
        self.stop()
