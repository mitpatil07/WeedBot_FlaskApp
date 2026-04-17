import time
from utils import get_arduino_serial

class MotorController:
    def __init__(self):
        self.arduino = get_arduino_serial()
        self.current_speed = 100

    def forward(self, speed=None):
        if speed is not None: self.current_speed = speed
        self._send_command('FWD', self.current_speed)

    def backward(self, speed=None):
        if speed is not None: self.current_speed = speed
        self._send_command('BWD', self.current_speed)

    def left(self, speed=None):
        if speed is not None: self.current_speed = speed
        self._send_command('LFT', self.current_speed)

    def right(self, speed=None):
        if speed is not None: self.current_speed = speed
        self._send_command('RGT', self.current_speed)

    def stop(self):
        self._send_command('STP', 0)
        
    def set_speed(self, speed):
        self.current_speed = speed
        # Most commands apply speed immediately, so we don't necessarily need a separate STP/START cycle

    def _send_command(self, direction, speed):
        command = f"M:{direction}:{speed}\n"
        from utils import safe_write_serial
        safe_write_serial(command.encode())

    def cleanup(self):
        self.stop()
