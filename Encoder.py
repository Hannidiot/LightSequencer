from pyfirmata2.pyfirmata2 import Pin
import time

class Encoder:
    def __init__(self, red_pin: Pin, green_pin: Pin, blue_pin: Pin):
        self.red_pin = red_pin
        self.green_pin = green_pin
        self.blue_pin = blue_pin
        self.pulse_delay = 0.1
        self._signal_duration_map = {
            "1": 0.1,
            "0": 0.05
        }

    def rgb(self, red, green, blue):
        self.red_pin.write(red)
        self.green_pin.write(green)
        self.blue_pin.write(blue)

    def encode(self, data: str):
        """
        turn zero-one sequence to signals emited by LED light

        INIT and TERMINATE duration: 200ms
        VALUE ONE duration: 100ms
        VALUE ZERO duration: 50ms
        """
        # INIT
        self._send_signal(0.2)
        
        # encode the sequence to light signals
        for c in data:
            if c in self._signal_duration_map.keys():
                self._send_signal(self._signal_duration_map[c])
        
        # TERMINATE
        self._send_signal(0.2)

    def _send_signal(self, length):
        self.rgb(1, 1, 1)
        time.sleep(length)
        self.rgb(0, 0, 0)
        time.sleep(self.pulse_delay)
