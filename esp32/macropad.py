    # MicroPython Human Interface Device library
# Copyright (C) 2021 H. Groefsema
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


# Implements a BLE HID keyboard
import time
from machine import SoftSPI, Pin
from hid_services import Keyboard

class Device:
    def __init__(self):
    
        # Define state
        self.key0 = 0x00
        self.key1 = 0x00
        self.key2 = 0x00
        self.key3 = 0x00

        # Define buttons
        self.pin_forward = Pin(14, Pin.IN, Pin.PULL_UP)
        self.pin_reverse = Pin(23, Pin.IN, Pin.PULL_UP)
        self.pin_right = Pin(19, Pin.IN, Pin.PULL_UP)
        self.pin_left = Pin(18, Pin.IN, Pin.PULL_UP)

        # Create our device
        self.keyboard = Keyboard("LosTastaturos")
        # Set a callback function to catch changes of device state
        self.keyboard.set_state_change_callback(self.keyboard_state_callback)
        # Start our device
        self.keyboard.start()
        self.keyboard.start_advertising()

    # Function that catches device status events
    def keyboard_state_callback(self):
        if self.keyboard.get_state() is Keyboard.DEVICE_IDLE:
            return
        elif self.keyboard.get_state() is Keyboard.DEVICE_ADVERTISING:
            return
        elif self.keyboard.get_state() is Keyboard.DEVICE_CONNECTED:
            return
        else:
            return


    def advertise(self):
        self.keyboard.start_advertising()

    def stop_advertise(self):
        self.keyboard.stop_advertising()

    # Main loop
    def start(self):
        prev_key0 = 0x00

        while True:
            # Read pin values
            if not self.pin_forward.value():
                self.key0 = 0x1A  # W
            else:
                self.key0 = 0x00

            if self.keyboard.get_state() == Keyboard.DEVICE_CONNECTED:
                # Only send a report when state actually changes
                if self.key0 != prev_key0:
                    self.keyboard.set_keys(self.key0)
                    self.keyboard.notify_hid_report()
                    prev_key0 = self.key0

            elif self.keyboard.get_state() is Keyboard.DEVICE_IDLE:
                if self.key0 != 0x00:  # only advertise if a key is being pressed
                    self.keyboard.start_advertising()
                    i = 10
                    while i > 0 and self.keyboard.get_state() is Keyboard.DEVICE_ADVERTISING:
                        time.sleep(3)
                        i -= 1
                    if self.keyboard.get_state() is Keyboard.DEVICE_ADVERTISING:
                        self.keyboard.stop_advertising()

            if self.keyboard.get_state() is Keyboard.DEVICE_CONNECTED:
                time.sleep_ms(20)
            else:
                time.sleep(2)           
'''

'''

if __name__ == "__main__":
    d = Device()
    d.start()
