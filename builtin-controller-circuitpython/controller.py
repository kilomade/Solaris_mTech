import digitalio
import analogio
import time
import struct
import micropython
import microcontroller
import busio
import json

dpad_up = digitalio.DigitalInOut(microcontroller.pin.GPIO36)
dpad_up.direction = digitalio.Direction.INPUT
dpad_down = digitalio.DigitalInOut(microcontroller.pin.GPIO39)
dpad_down.direction = digitalio.Direction.INPUT
dpad_left = digitalio.DigitalInOut(microcontroller.pin.GPIO34)
dpad_left.direction = digitalio.Direction.INPUT
dpad_right = digitalio.DigitalInOut(microcontroller.pin.GPIO35)
dpad_right.direction = digitalio.Direction.INPUT
a_button = digitalio.DigitalInOut(microcontroller.pin.GPIO14)
a_button.direction = digitalio.Direction.INPUT
b_button = digitalio.DigitalInOut(microcontroller.pin.GPIO5)
b_button.direction = digitalio.Direction.INPUT
x_button = digitalio.DigitalInOut(microcontroller.pin.GPIO18)
x_button.direction = digitalio.Direction.INPUT
y_button = digitalio.DigitalInOut(microcontroller.pin.GPIO19)
y_button.direction = digitalio.Direction.INPUT
rt_button = analogio.AnalogIn(microcontroller.pin.GPIO2)
rb_button = digitalio.DigitalInOut(microcontroller.pin.GPIO13)
rb_button.direction = digitalio.Direction.INPUT
lt_button = analogio.AnalogIn(microcontroller.pin.GPIO15)
lb_button = digitalio.DigitalInOut(microcontroller.pin.GPIO26)
lb_button.direction = digitalio.Direction.INPUT
ls_x = analogio.AnalogIn(microcontroller.pin.GPIO33)
ls_y = analogio.AnalogIn(microcontroller.pin.GPIO25)
ls_button = digitalio.DigitalInOut(microcontroller.pin.GPIO32)
ls_button.direction = digitalio.Direction.INPUT
rs_x = analogio.AnalogIn(microcontroller.pin.GPIO0)
rs_y = analogio.AnalogIn(microcontroller.pin.GPIO4)
rs_button = digitalio.DigitalInOut(microcontroller.pin.GPIO12)
rs_button.direction = digitalio.Direction.INPUT
start_button = digitalio.DigitalInOut(microcontroller.pin.GPIO21)
start_button.direction = digitalio.Direction.INPUT
back_button = digitalio.DigitalInOut(microcontroller.pin.GPIO22)
back_button.direction = digitalio.Direction.INPUT
home_button = digitalio.DigitalInOut(microcontroller.pin.GPIO23)
home_button.direction = digitalio.Direction.INPUT

signal_pin = digitalio.DigitalInOut(microcontroller.pin.GPIO16)
signal_pin.direction = digitalio.Direction.INPUT
# Define the minimum and maximum values for the joystick axes
joy_min = 0
joy_max = 65535

# MODE DESIGNATOR
debugMode = False
# create a variable to store the last time the home button was pressed
click_time = 0
click_count = 0
Home_Button = False
Mode_Flag = False

# create a variable to indicate whether turbo mode is active
turbo = False



# Helper function to map a value from one range to another
def map_range(value, in_min, in_max, out_min, out_max):
    return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def get_controller_state():
    global a_button, b_button, x_button, y_button, start_button, back_button, lb_button, rb_button, ls_x, ls_y, rs_x, rs_y, lt_button, rt_button, dpad_up, dpad_down, dpad_left, dpad_right, ls_button, rs_button
    # Read button states
    a_button_ = not a_button.value
    b_button_ = not b_button.value
    x_button_ = not x_button.value
    y_button_ = not y_button.value
    start_button_ = not start_button.value
    back_button_ = not back_button.value
    lb_button_ = not lb_button.value
    rb_button_ = not rb_button.value

    # Read joystick and map to range -127 to 127

    ls_x_ = ls_x.value
    ls_y_ = ls_y.value
    rs_x_ = rs_x.value
    rs_y_ = rs_y.value
    
    rs_button_ = not rs_button.value
    ls_button_ = not ls_button.value

    # Read triggers and map to range 0 to 255
    lt = lt_button.value
    rt = rt_button.value

    # Read directional pad and set x and y values accordingly

    dpad = [dpad_up.value, dpad_left.value, dpad_down.value, dpad_right.value]

    dpad_x = 0
    dpad_y = 0

    if (dpad[0] is True) and (dpad[2] is False):
        #UP
        dpad_y = -1
    elif (dpad[0] is False) and (dpad[2] is True):
        #DOWN
        dpad_y = 1

    if (dpad[1] is True) and (dpad[3] is False):
        #LEFT
        dpad_x = -1
    elif (dpad[1] is False) and (dpad[3] is True):
        #RIGHT
        dpad_x = 1

    home_button_ = not home_button.value

    # Pack values into bytearray
    currentMap = {
        "dpad_x": dpad_x,
        "dpad_y": dpad_y,
        "ls_x": ls_x_,
        "ls_y": ls_y_,
        "ls_button": ls_button_,
        "rs_x": rs_x_,
        "rs_y": rs_y_,
        "rs_button": rs_button_,
        "lt": lt,
        "rt": rt,
        "a": a_button_,
        "b": b_button_,
        "x": x_button_,
        "y": y_button_,
        "lb": lb_button_,
        "rb": rb_button_,
        "start": start_button_,
        "back": back_button_,
        "home": home_button_
    }

    return json.dumps(currentMap)

def triggerService():
    # main loop
    while True:
        global debugMode, signal_pin
        while signal_pin.value or debugMode:
        # while True:
            # get the controller state
            state = get_controller_state()

            # send the controller state over serial
            global debugMode

            print(state)

            # wait 50ms
            time.sleep(0.05)
