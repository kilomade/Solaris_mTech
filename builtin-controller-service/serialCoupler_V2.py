import json
import signal
import uinput
import serial
import util
import config
import time
import wiringpi
from wiringpi import GPIO
import re
import systemStateMonitor

serialHandler = None

# Define the virtual Xbox controller's capabilities
gamepad = uinput.Device([
    uinput.BTN_A,
    uinput.BTN_B,
    uinput.BTN_X,
    uinput.BTN_Y,
    uinput.BTN_TL,    #Left Trigger
    uinput.BTN_TR,    #Right Trigger
    uinput.BTN_THUMBL,   #Left Thumb
    uinput.BTN_THUMBR,   #Right Thumb
    uinput.ABS_X + (-32768, 32767, 0, 0),
    uinput.ABS_Y + (-32768, 32767, 0, 0),
    uinput.ABS_RX + (-32768, 32767, 0, 0),
    uinput.ABS_RY + (-32768, 32767, 0, 0),
    uinput.ABS_HAT0X + (-1, 1, 0, 0),  #DPAD
    uinput.ABS_HAT0Y + (-1, 1, 0, 0),  #DPAD
    uinput.BTN_MODE,
    uinput.BTN_BACK,
    uinput.BTN_SELECT,
    uinput.ABS_Z + (0, 255, 0, 0),      #Left Trigger
    uinput.ABS_RZ + (0, 255, 0, 0)      #Right Trigger
])

axes = {
    'LS_X': uinput.ABS_X,
    'LS_Y': uinput.ABS_Y,
    'RS_X': uinput.ABS_RX,
    'RS_Y': uinput.ABS_RY,
    'DPAD_X': uinput.ABS_HAT0X,
    'DPAD_Y': uinput.ABS_HAT0Y,
}

button_activity_map = {
    "X": False,
    "Y": False,
    "A": False,
    "B": False,
    "Right Switch": False,
    "RB": False,
    "RT": False,
    "Left Switch": False,
    "LB": False,
    "LT": False
}

special_button_map = {
    "START": False,
    "BACK": False,
    "HOME": False
}

movement_map = {
    "LS_X": 0,
    "LS_Y": 0,
    "RS_X": 0,
    "RS_Y": 0
}

dpad_map = {
    "DPAD_X": 0,
    "DPAD_Y": 0
}


def gpioConfiguration():
    wiringpi.wiringPiSetup()
    wiringpi.pinMode(config.resetPin, GPIO.OUTPUT)
    wiringpi.pinMode(config.pollingSignalPin, GPIO.OUTPUT)


def resetControllerModule():
    print("Cycle submodule")
    wiringpi.digitalWrite(config.pollingSignalPin, GPIO.LOW)
    wiringpi.digitalWrite(config.resetPin, GPIO.LOW)
    time.sleep(5)
    wiringpi.digitalWrite(config.resetPin, GPIO.HIGH)

def enableControllerSignalling():
    print("Start polling")
    wiringpi.digitalWrite(config.pollingSignalPin, GPIO.HIGH)

def disableControllerSignalling():
    print("Stop Polling")
    wiringpi.digitalWrite(config.pollingSignalPin, GPIO.LOW)

def keyboardInterruptHandler(signal, frame):
    disableControllerSignalling()
    serialHandler.close()
    # wiringpi.cleanup()
    exit(0)

#REGION game pad logic
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

def pushTrigger(identifier, value):
    if identifier == 'L':
        gamepad.emit(uinput.ABS_Z, int(value))
    elif identifier == 'R':
        gamepad.emit(uinput.ABS_RZ, int(value))

def pushButton(buttonCode):
    global gamepad

    if buttonCode == "a":
        gamepad.emit(uinput.BTN_A, 1)
        time.sleep(config.buttonDelay)
        gamepad.emit(uinput.BTN_A, 0)
    elif buttonCode == "b":
        gamepad.emit(uinput.BTN_B, 1)
        time.sleep(config.buttonDelay)
        gamepad.emit(uinput.BTN_B, 0)
    elif buttonCode == "y":
        gamepad.emit(uinput.BTN_Y, 1)
        time.sleep(config.buttonDelay)
        gamepad.emit(uinput.BTN_Y, 0)
    elif buttonCode == "x":
        gamepad.emit(uinput.BTN_X, 1)
        time.sleep(config.buttonDelay)
        gamepad.emit(uinput.BTN_X, 0)
    elif buttonCode == "rs_button":
        gamepad.emit(uinput.BTN_THUMBR, 1)
        time.sleep(config.buttonDelay)
        gamepad.emit(uinput.BTN_THUMBR, 0)
    elif buttonCode == "ls_button":
        gamepad.emit(uinput.BTN_THUMBL, 1)
        time.sleep(config.buttonDelay)
        gamepad.emit(uinput.BTN_THUMBL, 0)
    elif buttonCode == "rb":
        gamepad.emit(uinput.BTN_TR, 1)
        time.sleep(config.buttonDelay)
        gamepad.emit(uinput.BTN_TR, 0)
    elif buttonCode == "lb":
        gamepad.emit(uinput.BTN_TL, 1)
        time.sleep(config.buttonDelay)
        gamepad.emit(uinput.BTN_TL, 0)
    else:
        print("Key not served")

#ENDREGIOn

signal.signal(signal.SIGINT, keyboardInterruptHandler)
def handleInputFeed():
    global serialHandler, button_activity_map, movement_map, dpad_map, special_button_map

    serialHandler = serial.Serial(config.serialPort, config.serialBaudRate)
    resetControllerModule()
    enableControllerSignalling()

    # Loop indefinitely
    while True:
        # Wait for data to be available on the serial port
        while serialHandler.in_waiting == 0:
            pass


        inbound = str(serialHandler.readline().decode('utf-8')).rstrip()
        commandLoad = json.loads(inbound)
        print(commandLoad)

        if commandLoad["home"]:
            pushHome()

        if commandLoad["start"]:
            pushStart()

        if commandLoad["back"]:
            pushBack()

        update_axis('LS_X', commandLoad['ls_x'])
        update_axis('LS_Y', commandLoad['ls_y'])
        update_axis('RS_X', commandLoad['rs_x'])
        update_axis('RS_Y', commandLoad['rs_y'])
        update_axis('DPAD_X', commandLoad['dpad_x'])
        update_axis('DPAD_Y', commandLoad['dpad_y'])

        pushTrigger('L', commandLoad['lt'])
        pushTrigger('R', commandLoad['rt'])

        for i in commandLoad.keys():
            if not commandLoad[i]:
                pushButton(buttonCode=i)


gpioConfiguration()
handleInputFeed()