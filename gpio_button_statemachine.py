#
# This simple python script implements a state machine
# which can be controlled by a push button attached
# to a GPIO chip.
# The outputs of the state machine are attached
# to GPIO outputs.
#
# On RHEL and Fedora, the dependencies can be installed as follows:
#   dnf install python3-libgpiod python3-Automat python3-notify2
#
# On RHEL, python3-Automat and python3-notify2 are avaialble in EPEL:
#   https://docs.fedoraproject.org/en-US/epel/
#


import gpiod
import time
import sys
import notify2
from automat import MethodicalMachine

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

# This class implements a state machine for handling all the events for our
# Demo project


class GPIODemo(object):

    # Documentation:
    # https://github.com/glyph/Automat

    _machine = MethodicalMachine()

    def __init__(self):

        # Initialize the Chip
        self.chip = gpiod.Chip(GPIO_CHIP)

        # Initialize the 3 LEDs pins as outputs
        self.red = self.chip.get_line(RED_LED_OFFSET)
        self.yellow = self.chip.get_line(YELLOW_LED_OFFSET)
        self.green = self.chip.get_line(GREEN_LED_OFFSET)

        self.red.request(consumer=sys.argv[0],
                         type=gpiod.LINE_REQ_DIR_OUT, default_val=0)
        self.yellow.request(consumer=sys.argv[0],
                            type=gpiod.LINE_REQ_DIR_OUT, default_val=0)
        self.green.request(
            consumer=sys.argv[0], type=gpiod.LINE_REQ_DIR_OUT, default_val=0)

    @_machine.input()
    def gpio_button(self):
        "The user pressed the GPIO button."

    @_machine.output()
    def turn_on_red_led(self):
        "Turn on the Red LED"
        self.red.set_value(1)
        n = notify2.Notification("Red",
                                 "Red",
                                 "notification-message-IM")
        n.show()

    @_machine.output()
    def turn_on_yellow_led(self):
        "Turn on the Yellow LED"
        self.yellow.set_value(1)
        n = notify2.Notification("Yellow",
                                 "Yellow",
                                 "notification-message-IM")
        n.show()

    @_machine.output()
    def turn_on_green_led(self):
        "Turn on the Green LED"
        self.green.set_value(1)
        n = notify2.Notification("Green",
                                 "Green",
                                 "notification-message-IM")
        n.show()

    @_machine.output()
    def turn_off_red_led(self):
        "Turn off the Red LED"
        self.red.set_value(0)

    @_machine.output()
    def turn_off_yellow_led(self):
        "Turn off the Yellow LED"
        self.yellow.set_value(0)

    @_machine.output()
    def turn_off_green_led(self):
        "Turn off the Green LED"
        self.green.set_value(0)

    @_machine.state(initial=True)
    def red(self):
        "Red LED is on"

    @_machine.state()
    def yellow(self):
        "Yellow LED is on"

    @_machine.state()
    def green(self):
        "Green LED is on"

    # This section wires up the state transitions of the state machine
    # red -> yellow -> green -> red
    red.upon(gpio_button, enter=yellow, outputs=[
             turn_on_yellow_led, turn_off_red_led, turn_off_green_led])
    yellow.upon(gpio_button, enter=green, outputs=[
                turn_on_green_led, turn_off_red_led, turn_off_yellow_led])
    green.upon(gpio_button, enter=red, outputs=[
               turn_on_red_led, turn_off_yellow_led, turn_off_green_led])


if __name__ == '__main__':

    # Initialize the notify system
    notify2.init(sys.argv[0])

    # Initialize the state machine
    gpiodemo = GPIODemo()

    # Initialize the GPIO chip for the button
    with gpiod.Chip(GPIO_CHIP) as chip:

        # configure the Button pin as input
        button = chip.get_line(BUTTON_OFFSET)
        button.request(consumer=sys.argv[0], type=gpiod.LINE_REQ_DIR_IN)

        try:
            # Read the initial value
            prev_value = button.get_value()

            # Read the button state in a loop
            while True:
                new_value = button.get_value()
                # If the value is different from the previous value we know
                # that the button has been pressed
                if new_value != prev_value:
                    prev_value = new_value
                    # We only want to react when the button is pressed
                    if new_value == 1:
                        gpiodemo.gpio_button()

                time.sleep(0.01)
        except KeyboardInterrupt:
            sys.exit(0)
