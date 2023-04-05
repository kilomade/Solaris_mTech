import uinput
import time
import config
import serialCoupler
import threading
import asyncio

# Define the virtual Xbox controller's capabilities
gamepad = uinput.Device([
    uinput.BTN_A,
    uinput.BTN_B,
    uinput.BTN_X,
    uinput.BTN_Y,
    uinput.BTN_TL,
    uinput.BTN_TR,
    uinput.BTN_THUMBL,
    uinput.BTN_THUMBR,
    uinput.ABS_X + (-32768, 32767, 0, 0),
    uinput.ABS_Y + (-32768, 32767, 0, 0),
    uinput.ABS_RX + (-32768, 32767, 0, 0),
    uinput.ABS_RY + (-32768, 32767, 0, 0),
    uinput.ABS_HAT0X + (-1, 1, 0, 0),
    uinput.ABS_HAT0Y + (-1, 1, 0, 0),
    uinput.BTN_MODE
])

# Define the button and axis mappings for the virtual Xbox controller
buttons = {
    'A': uinput.BTN_A,
    'B': uinput.BTN_B,
    'X': uinput.BTN_X,
    'Y': uinput.BTN_Y,
    'LB': uinput.BTN_TL,
    'RB': uinput.BTN_TR,
    'LS': uinput.BTN_THUMBL,
    'RS': uinput.BTN_THUMBR,
    'START': uinput.BTN_START,
    'SELECT': uinput.BTN_SELECT,
    'BACK': uinput.BTN_BACK,
    'HOME': uinput.BTN_MODE
}

axes = {
    'LS_X': uinput.ABS_X,
    'LS_Y': uinput.ABS_Y,
    'RS_X': uinput.ABS_RX,
    'RS_Y': uinput.ABS_RY,
    'DPAD_X': uinput.ABS_HAT0X,
    'DPAD_Y': uinput.ABS_HAT0Y,
}

# Helper function to update the state of a button on the virtual Xbox controller
def update_button(button, state):
    gamepad.emit(buttons[button], state)

# Helper function to update the state of an axis on the virtual Xbox controller
def update_axis(axis, value):
    gamepad.emit(axes[axis], int(value))

def pushHome():
    global gamepad

    gamepad.emit(uinput.BTN_SELECT, 1)
    time.sleep(config.buttonDelay)
    gamepad.emit(uinput.BTN_SELECT, 0)

def pushStart():
    global gamepad

    gamepad.emit(uinput.BTN_START, 1)
    time.sleep(config.buttonDelay)
    gamepad.emit(uinput.BTN_START, 0)

def pushBack():
    global gamepad

    gamepad.emit(uinput.BTN_BACK, 1)
    time.sleep(config.buttonDelay)
    gamepad.emit(uinput.BTN_BACK, 0)

def pushButton(buttonCode):
    global gamepad

    if buttonCode == "A":
        gamepad.emit(uinput.BTN_A, 1)
        time.sleep(config.buttonDelay)
        gamepad.emit(uinput.BTN_A, 0)
    elif buttonCode == "B":
        gamepad.emit(uinput.BTN_B, 1)
        time.sleep(config.buttonDelay)
        gamepad.emit(uinput.BTN_B, 0)
    elif buttonCode == "Y":
        gamepad.emit(uinput.BTN_Y, 1)
        time.sleep(config.buttonDelay)
        gamepad.emit(uinput.BTN_Y, 0)
    elif buttonCode == "X":
        gamepad.emit(uinput.BTN_X, 1)
        time.sleep(config.buttonDelay)
        gamepad.emit(uinput.BTN_X, 0)
    elif buttonCode == "Right Switch":
        gamepad.emit(uinput.BTN_THUMBR, 1)
        time.sleep(config.buttonDelay)
        gamepad.emit(uinput.BTN_THUMBR, 0)
    elif buttonCode == "Left Switch":
        gamepad.emit(uinput.BTN_THUMBL, 1)
        time.sleep(config.buttonDelay)
        gamepad.emit(uinput.BTN_THUMBL, 0)
    else:
        print("Key not implemented")

def checkMovement():
    print("updating movement")
    for key, value in serialCoupler.movement_map.items():
        print("{} {}".format(key, value))
        update_axis(key, value)

    for key in serialCoupler.movement_map.keys():
        serialCoupler.movement_map[key] = 0

def checkHomeBackPause():
    if serialCoupler.special_button_map["HOME"]:
        print("Home detected")
        pushHome()

    serialCoupler.special_button_map["HOME"] = False

    if serialCoupler.special_button_map["BACK"]:
        print("Back detected")
        pushBack()

    serialCoupler.special_button_map["BACK"] = False

    if serialCoupler.special_button_map["START"]:
        print("Start detected")
        pushStart()

    serialCoupler.special_button_map["START"] = False

asyncio.run(serialCoupler.handleInputFeed())
print(gamepad)
while True:

    for key, value in serialCoupler.button_activity_map.items():
        checkMovement()
        checkHomeBackPause()

        if value is True:
            pushButton(key)

    key_list = serialCoupler.button_activity_map.keys()

    for i in key_list:
        serialCoupler.button_activity_map[i] = False

