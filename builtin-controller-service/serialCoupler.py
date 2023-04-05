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

#ENDREGIOn

signal.signal(signal.SIGINT, keyboardInterruptHandler)
def handleInputFeed():
    global serialHandler, button_activity_map, movement_map, dpad_map, special_button_map

    serialHandler = serial.Serial(config.serialPort, config.serialBaudRate)
    resetControllerModule()
    enableControllerSignalling()

    while True:
        if serialHandler.in_waiting > 0:
            command = serialHandler.readline().decode().rstrip('\r\n')
            print("Raw command --> {}".format(command))

            commandValidationRegex = "::(.*)::"
            commandValidationCheck = re.match(commandValidationRegex, command)

            if commandValidationCheck is not None:
                newCommand = commandValidationCheck.group(1)

                # print("Inbound command: " + str(newCommand))

                movementRegex = r"Movement -- ([0-9]+) ([0-9]+) ([0-9]+) ([0-9]+)"
                dpadRegex = r"(DPAD_[XY]) -- ([01])"
                movementCheck = re.match(movementRegex, newCommand)
                dpadRegexCheck = re.match(dpadRegex, newCommand)

                if movementCheck is not None:
                    leftX = int(movementCheck.group(1))
                    leftY = int(movementCheck.group(2))
                    rightX = int(movementCheck.group(3))
                    rightY = int(movementCheck.group(4))

                    # print("[LEFT]: Y: {}  X: {}     [RIGHT]: Y: {}   X: {}".format(leftY, leftX, rightY, rightX))
                    update_axis('LS_X', leftX)  # Move the left joystick to the right
                    update_axis('LS_Y', leftY)  # Move the left joystick up
                    update_axis('RS_X', rightX)  # Move the right joystick to the left
                    update_axis('RS_Y', rightY)  # Move the right joystick down
                    #
                    #   Controller value mapping
                    #                      0
                    #     65535 <---|--->  0
                    #                    65535
                    #

                    # Controller.postLeftJoystick(lx=leftX, ly=leftY)
                    # Controller.postRightJoystick(rx=rightX, ry=rightY)
                elif dpadRegexCheck is not None:
                    update_axis(dpadRegexCheck.group(1), int(dpadRegexCheck.group(2)))
                    # dpad_map[dpadRegexCheck.group(1)] = int(dpadRegexCheck.group(2))
                elif newCommand == "TURBO":
                    #change cpu governor mode
                    systemStateMonitor.changeSystemMode()
                    pass
                elif newCommand == "HOME":
                    pushHome()
                elif newCommand == "BACK":
                    pushBack()
                elif newCommand == "PAUSE":
                    pushStart()
                else:
                    pushButton(newCommand)

            else:
                print("Unexpected Input")
                print(command)
                # serialHandler.close()
                # resetControllerModule()
                # serialHandler = serial.Serial(config.serialPort, config.serialBaudRate)
                # serialHandler.close()
                # serialHandler.open()
                # enableControllerSignalling()

gpioConfiguration()
handleInputFeed()