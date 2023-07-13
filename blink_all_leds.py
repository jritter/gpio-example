#
# This simple Python script switches on and off 3 GPIO pins one by one. 
# These pins can drive LEDs for example.
#
# On RHEL and Fedora, the dependencies can be installed as follows:
#   dnf install python3-libgpiod
#


import gpiod
import time
import sys

# This constant defines which gpiochip will
# be used to drive the GPIOs.
#
# There should be a corresponding character
# device in /dev
GPIO_CHIP = 'gpiochip0'

# This defines the pin numbers to which
# the LEDs are wired up
RED_LED_OFFSET = 0
YELLOW_LED_OFFSET = 1
GREEN_LED_OFFSET = 2

# This constant defines the pin that
# is connected to the button
BUTTON_OFFSET = 3


if __name__ == '__main__':

    # Initialize the GPIO chip
    with gpiod.Chip(GPIO_CHIP) as chip:
        # get a reference to all the leds
        red = chip.get_line(RED_LED_OFFSET)
        yellow = chip.get_line(YELLOW_LED_OFFSET)
        green = chip.get_line(GREEN_LED_OFFSET)

        # Allocate the pins and configure them as output
        red.request(
            consumer=sys.argv[0], type=gpiod.LINE_REQ_DIR_OUT, default_val=0)
        yellow.request(
            consumer=sys.argv[0], type=gpiod.LINE_REQ_DIR_OUT, default_val=0)
        green.request(
            consumer=sys.argv[0], type=gpiod.LINE_REQ_DIR_OUT, default_val=0)

        try:
            while True:
                # Switch on and off the LEDs one by one
                red.set_value(1)
                time.sleep(0.2)
                red.set_value(0)
                yellow.set_value(1)
                time.sleep(0.2)
                yellow.set_value(0)
                green.set_value(1)
                time.sleep(0.2)
                green.set_value(0)
        except KeyboardInterrupt:
            sys.exit(0)
