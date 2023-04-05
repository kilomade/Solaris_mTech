import machine
import utime
from micropython import const
import config
import time
import struct

controllerModel = "esp32-wroom-32d"

# Define the pins to be used for the Xbox controller buttons
A_BUTTON = None
B_BUTTON = None
X_BUTTON = None
Y_BUTTON = None
LB_BUTTON = None
RB_BUTTON = None
BACK_BUTTON = None
START_BUTTON = None
LS_BUTTON = None
RS_BUTTON = None
HOME_BUTTON = None
# Define the pins to be used for the Xbox controller joystick axes
LX_AXIS = None
LY_AXIS = None
RX_AXIS = None
RY_AXIS = None

#Define Triggers
LT_ANA = None
RT_ANA = None

# Define the pins for the directional button pad
button_up = None
button_down = None
button_left = None
button_right = None
button_home = 0

signalPin = None

# Define the maximum and minimum values for the joystick axes
MAX_AXIS_VALUE = const(65535)
MIN_AXIS_VALUE = const(0)

home_button_count = 0
turbo_mode=False
uart1 = None
# Define the ESP32 GPIO pins to be used for the Xbox controller buttons and axes
button_pins = None
axis_pins = None
button_objects = None

# Initialize the GPIO pins as ADC pins
adcL_x = None
adcL_y = None
adcR_x = None
adcR_y = None
adcLT = None
adcRT = None

last_button_state = 0 # Assumes 15 buttons on the controller

def configPins():
    global A_BUTTON, B_BUTTON, X_BUTTON, Y_BUTTON, LB_BUTTON, RB_BUTTON, BACK_BUTTON, START_BUTTON, LS_BUTTON, RS_BUTTON, HOME_BUTTON, LX_AXIS, LY_AXIS
    global RX_AXIS, RY_AXIS, LT_ANA, RT_ANA, button_down, button_up, button_left, button_right, button_home, signalPin, MAX_AXIS_VALUE, MIN_AXIS_VALUE
    global home_button_count, turbo_mode, uart1, axis_pins, adcL_x, adcL_y, adcR_x, adcR_y, last_button_state
    # Define the pins to be used for the Xbox controller buttons
    A_BUTTON = config.buttonMap[controllerModel]["pinmap"]["buttonA"]
    B_BUTTON = config.buttonMap[controllerModel]["pinmap"]["buttonB"]
    X_BUTTON = config.buttonMap[controllerModel]["pinmap"]["buttonX"]
    Y_BUTTON = config.buttonMap[controllerModel]["pinmap"]["buttonY"]
    LB_BUTTON = config.buttonMap[controllerModel]["pinmap"]["buttonLeftShoulder"]
    RB_BUTTON = config.buttonMap[controllerModel]["pinmap"]["buttonRightShoulder"]
    BACK_BUTTON = config.buttonMap[controllerModel]["pinmap"]["buttonBack"]
    START_BUTTON = config.buttonMap[controllerModel]["pinmap"]["buttonPause"]
    LS_BUTTON = config.buttonMap[controllerModel]["pinmap"]["buttonJoySwitchLeft"]
    RS_BUTTON = config.buttonMap[controllerModel]["pinmap"]["buttonJoySwitchRight"]
    HOME_BUTTON = config.buttonMap[controllerModel]["pinmap"]["buttonHomeTurbo"]
    # Define the pins to be used for the Xbox controller joystick axes
    LX_AXIS = config.buttonMap[controllerModel]["pinmap"]["axisXLeft"]
    LY_AXIS = config.buttonMap[controllerModel]["pinmap"]["axisYLeft"]
    RX_AXIS = config.buttonMap[controllerModel]["pinmap"]["axisXRight"]
    RY_AXIS = config.buttonMap[controllerModel]["pinmap"]["axisYRight"]

    #Define Triggers
    LT_ANA = config.buttonMap[controllerModel]["pinmap"]["buttonLeftTrigger"]
    RT_ANA = config.buttonMap[controllerModel]["pinmap"]["buttonRightTrigger"]

    # Define the pins for the directional button pad
    button_up = machine.Pin(config.buttonMap[controllerModel]["pinmap"]["buttonUp"], machine.Pin.IN, machine.Pin.PULL_UP)
    button_down = machine.Pin(config.buttonMap[controllerModel]["pinmap"]["buttonDown"], machine.Pin.IN, machine.Pin.PULL_UP)
    button_left = machine.Pin(config.buttonMap[controllerModel]["pinmap"]["buttonLeft"], machine.Pin.IN, machine.Pin.PULL_UP)
    button_right = machine.Pin(config.buttonMap[controllerModel]["pinmap"]["buttonRight"], machine.Pin.IN, machine.Pin.PULL_UP)
    button_home = 0

    signalPin = machine.Pin(config.buttonMap[controllerModel]["signalpin"], machine.Pin.IN)

    home_button_count = 0
    turbo_mode=False
    uart1 = machine.UART(0, 115200, tx=3, rx=1)
    uart1.init()
    # uart1 = machine.UART(1, baudrate=115200, tx=int(config.buttonMap[controllerModel]["tx"]), rx=int(config.buttonMap[controllerModel]["rx"]))
    # uart1.init(baudrate=115200, bits=8, parity=None, stop=1, tx=config.buttonMap[controllerModel]["tx"], rx=config.buttonMap[controllerModel]["rx"])
    # Define the ESP32 GPIO pins to be used for the Xbox controller buttons and axes
    button_pins = [A_BUTTON, B_BUTTON, X_BUTTON, Y_BUTTON, LB_BUTTON, RB_BUTTON, BACK_BUTTON, START_BUTTON, LS_BUTTON,
                RS_BUTTON, HOME_BUTTON]
    axis_pins = [LX_AXIS, LY_AXIS, RX_AXIS, RY_AXIS]
    button_objects = []

    # Initialize the GPIO pins as input pins
    for pin in button_pins:
        temp = machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP)
        button_objects.append(temp)

    # Initialize the GPIO pins as ADC pins
    adcL_x = machine.ADC(machine.Pin(LX_AXIS))
    adcL_x.atten(machine.ADC.ATTN_11DB)
    adcL_y = machine.ADC(machine.Pin(LY_AXIS))
    adcL_y.atten(machine.ADC.ATTN_11DB)
    adcR_x = machine.ADC(machine.Pin(RX_AXIS))
    adcR_x.atten(machine.ADC.ATTN_11DB)
    adcR_y = machine.ADC(machine.Pin(RY_AXIS))
    adcR_y.atten(machine.ADC.ATTN_11DB)
    adcLT = machine.ADC(machine.Pin(LT_ANA))
    adcLT.atten(machine.ADC.ATTN_11DB)
    adcRT = machine.ADC(machine.Pin(RT_ANA))
    adcRT.atten(machine.ADC.ATTN_11DB)

    last_button_state = 0 # Assumes 15 buttons on the controller

# Define the map_range function
def map_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# Define the function to retrieve the Xbox controller state
def get_controller_state():
    global adcL_y, adcL_x, adcR_y, adcR_x, button_up, button_down, button_left, button_right, button_objects, home_button_count, turbo_mode
    # Read the values of the joystick axes
    x_axis = adcL_x.read()
    y_axis = adcL_y.read()

    # Read the values of the Right Stick axes
    rx_axis = adcR_x.read()
    ry_axis = adcR_y.read()

    # Read the state of the directional button pad
    button_up_state = not button_up.value()
    button_down_state = not button_down.value()
    button_left_state = not button_left.value()
    button_right_state = not button_right.value()

    # Read the values of the buttons
    button_states = []

    for i in button_objects:
        button_states.append(not i.value())

    if button_objects[10].value() == False:
        if turbo_mode == False:
            home_button_count += 1
            if home_button_count == 1:
                button_states[10] = True
            elif home_button_count == 2:
                button_states[10] = True
                turbo_mode = True
                print("TurboMode enabled!")
        else:
            button_states[10] = True
    else:
        home_button_count = 0

    # Invert the values of the axes to match the Xbox controller
    x_axis = 1023 - x_axis
    y_axis = y_axis
    rx_axis = 1023 - rx_axis
    ry_axis = ry_axis

    return x_axis, y_axis, rx_axis, ry_axis, button_states, button_up_state, button_down_state, button_left_state, button_right_state

def emulate_xbox_controller_v2():
    global last_button_state, home_button_count, turbo_mode, uart1
    # Get the joystick axes, button states, and state of the directional button pad
    x_axis, y_axis, rx_axis, ry_axis, button_states, button_up_state, button_down_state, button_left_state, button_right_state = get_controller_state()

    x_value = map_range(x_axis, config.buttonMap[controllerModel]["hardware_specs"]["Joystick"]["MIN"], config.buttonMap[controllerModel]["hardware_specs"]["Joystick"]["MIN"], -32768, 32767)
    y_value = map_range(y_axis, config.buttonMap[controllerModel]["hardware_specs"]["Joystick"]["MIN"], config.buttonMap[controllerModel]["hardware_specs"]["Joystick"]["MIN"], 32767, -32768)
    rx_value = map_range(rx_axis, config.buttonMap[controllerModel]["hardware_specs"]["Joystick"]["MIN"], config.buttonMap[controllerModel]["hardware_specs"]["Joystick"]["MIN"], -32768, 32767)
    ry_value = map_range(ry_axis, config.buttonMap[controllerModel]["hardware_specs"]["Joystick"]["MIN"], config.buttonMap[controllerModel]["hardware_specs"]["Joystick"]["MIN"], 32767, -32768)
    
    # Get the state of the left and right triggers
    left_trigger = int(map_range(adcLT.read(), config.buttonMap[controllerModel]["hardware_specs"]["Trigger"]["MIN"], config.buttonMap[controllerModel]["hardware_specs"]["Trigger"]["MIN"], 0, 255))
    right_trigger = int(map_range(adcRT.read(), config.buttonMap[controllerModel]["hardware_specs"]["Trigger"]["MIN"], config.buttonMap[controllerModel]["hardware_specs"]["Trigger"]["MIN"], 0, 255))

    a_button = button_states[0]
    b_button = button_states[1]
    x_button = button_states[2]
    y_button = button_states[3]
    lb_button = button_states[4]
    rb_button = button_states[5]
    back_button = button_states[6]
    start_button = button_states[7]  # added START_BUTTON
    ls_button = button_states[8]  # added LS_BUTTON
    rs_button = button_states[9]  # added RS_BUTTON

    # Map directional button pad states to Xbox controller values
    d_pad_up = button_up_state
    d_pad_down = button_down_state
    d_pad_left = button_left_state
    d_pad_right = button_right_state

    

    # Set the TurboMode flag if it is enabled
    if turbo_mode:
        a_button = b_button = x_button = y_button = lb_button = rb_button = False

    # Handle HOME button press
    # Set the value of the HOME button based on the current state
    home_button = last_button_state > 0



    # Create the bytearray to send over serial
    controller_state = bytearray(struct.pack('hhhhBBBBBBBBB', x_value, y_value, rx_value, ry_value,
                                             a_button, b_button, x_button, y_button, lb_button, rb_button,
                                             back_button, start_button, ls_button, rs_button,
                                             d_pad_up, d_pad_down, d_pad_left, d_pad_right, turbo_mode, home_button, left_trigger, right_trigger))

    # Send the bytearray over serial
    uart1.write(controller_state)

    # Sleep for a short period to avoid sending data too quickly
    time.sleep(0.01)

def triggerService():
    configPins()

    global signalPin
    while True:
        while signalPin.value():
            emulate_xbox_controller_v2()