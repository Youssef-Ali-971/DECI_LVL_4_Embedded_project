from joystick import Joystick
from time import sleep
from machine import Pin
from servo import Servo


slide_switch = Pin(25, Pin.IN)
led1 = Pin(26, Pin.OUT, value=0)
led2 = Pin(27, Pin.OUT, value=0)


servo1 = Servo(23)
servo2 = Servo(22)
servo3 = Servo(15)
servo4 = Servo(13)


joystick = Joystick(35, 34, 'interrupt', 32)
step = 1

def valid_message(message):
    """Check if the user input is a valid number (1-10)."""
    return message.isdigit() and 1 <= int(message) <= 10

def get_servo_step():
    """Prompt the user for servo step value (1-10)."""
    while True:
        message = input("Please Enter servo step (1-10): ")
        if valid_message(message):
            return int(message)
        print("Invalid input! Please enter a number between 1 and 10.")

def move_servo(camera_active, direction, step):
    """Move the corresponding servo based on joystick direction."""
    servo_map = {
        "U": (servo1 if camera_active else servo3, "left"),
        "D": (servo1 if camera_active else servo3, "right"),
        "R": (servo2 if camera_active else servo4, "right"),
        "L": (servo2 if camera_active else servo4, "left"),
    }

    if direction in servo_map:
        servo, action = servo_map[direction]
        getattr(servo, action)(step)

while True:
    place, pressed_value = joystick.read()
    print(f"Joystick: {place}, Button Pressed: {pressed_value}")

    if pressed_value:
        step = get_servo_step()

    camera_active = slide_switch.value() == 1  

    led1.value(camera_active)
    led2.value(not camera_active)

    move_servo(camera_active, place, step)

    sleep(0.1)
