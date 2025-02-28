from machine import Pin, ADC, Timer

class Joystick:
    MID_VALUE = 2048  # Joystick ADC midpoint (center position)
    
    def __init__(self, xaxis: int, yaxis: int, mode: str, button: int):
        self.xAxis = ADC(Pin(xaxis))
        self.yAxis = ADC(Pin(yaxis))
        self.button = Pin(button, Pin.IN, Pin.PULL_UP)
        self.mode = mode

        # Last recorded values (for interrupt mode)
        self.last_horizontal = self.MID_VALUE
        self.last_vertical = self.MID_VALUE
        self.last_button_state = 1  # Button default state (not pressed)

        # Configure timer for interrupt mode
        if self.mode == 'interrupt':
            self.timer = Timer(-1)
            self.timer.init(mode=Timer.PERIODIC, period=50, callback=self._update_values)

    def _update_values(self, _):
        """Update joystick readings in interrupt mode."""
        self.last_horizontal = self.xAxis.read()
        self.last_vertical = self.yAxis.read()
        self.last_button_state = self.button.value()

    def read(self):
        """Read joystick state: L (Left), R (Right), U (Up), D (Down), M (Middle)."""
        if self.mode == 'polling':
            horizontal = self.xAxis.read()
            vertical = self.yAxis.read()
            button_state = self.button.value()
        else:
            horizontal = self.last_horizontal
            vertical = self.last_vertical
            button_state = self.last_button_state

        # Determine direction
        direction = 'M'  # Default to middle
        if abs(horizontal - self.MID_VALUE) > abs(vertical - self.MID_VALUE):
            direction = 'R' if horizontal < self.MID_VALUE else 'L'
        elif abs(vertical - self.MID_VALUE) > abs(horizontal - self.MID_VALUE):
            direction = 'U' if vertical > self.MID_VALUE else 'D'

        return direction, button_state == 0  # Return True if button is pressed
