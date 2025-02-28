from machine import Pin, PWM
from time import sleep

class Servo:
    def __init__(self, pin: int, min_us=550, max_us=2400):
        self.pwm = PWM(Pin(pin, Pin.OUT), freq=50)  # 50Hz PWM for servos
        self.min_us = min_us
        self.max_us = max_us
        self.min_angle = 0
        self.max_angle = 180
        self.current_angle = 90  # Default to center position
        self.motor_speed = 600  # 60° per 0.1s → 600° per second

        self.goto(self.current_angle)  # Move servo to starting position

    def _calculate_duty(self, angle):
        """Convert angle to duty cycle for servo control."""
        pulse_time = self.min_us + (angle / 180) * (self.max_us - self.min_us)
        duty_cycle = int((pulse_time / 20000) * 1023)  # Convert to duty value
        return duty_cycle

    def move(self, angle):
        """Move servo to a specified angle with speed control."""
        if not self.min_angle <= angle <= self.max_angle:
            return  # Ignore invalid angles

        duty = self._calculate_duty(angle)
        self.pwm.duty(duty)  # Apply duty cycle

        # Calculate movement delay based on angle change
        delta_angle = abs(angle - self.current_angle)
        sleep_time = max(delta_angle / self.motor_speed, 0.02)  # Ensure a minimum delay
        sleep(sleep_time)

        self.current_angle = angle  # Update position

    def goto(self, angle):
        """Move the servo to a specific angle."""
        self.move(angle)

    def left(self, angle):
        """Move the servo left by a specified angle."""
        self.goto(max(self.min_angle, self.current_angle - angle))

    def right(self, angle):
        """Move the servo right by a specified angle."""
        self.goto(min(self.max_angle, self.current_angle + angle))
