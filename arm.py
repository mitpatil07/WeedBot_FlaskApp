import time
from utils import get_arduino_serial

class ArmController:
    def __init__(self):
        self.arduino = get_arduino_serial()
        self.current_angle = 90  # Start at center

    def set_angle(self, angle):
        if angle < 0: angle = 0
        if angle > 180: angle = 180
        
        self.current_angle = angle
        command = f"A:{angle}\n"
        self.arduino.write(command.encode())

    def move_left(self, step=10):
        self.set_angle(self.current_angle + step)

    def move_right(self, step=10):
        self.set_angle(self.current_angle - step)

    def target_weed(self, x_coordinate, frame_width=640):
        # Map x_coordinate (0 to frame_width) to angle (0 to 180)
        target_angle = 180 - int((x_coordinate / frame_width) * 180)
        self.set_angle(target_angle)

    def reset_position(self):
        self.set_angle(90)
        
    def cleanup(self):
        pass # Arduino handles pins
