import serial
import util
import config
import time
import wiringpi
from wiringpi import GPIO
import re

serialHandler = None

def gpioConfiguration():
    wiringpi.wiringPiSetup()
    wiringpi.pinMode(config.resetPin, GPIO.OUTPUT)
    wiringpi.pinMode(config.pollingSignalPin, GPIO.OUTPUT)

def resetControllerModule():
    print("Resetting controller module")
    wiringpi.digitalWrite(config.resetPin, GPIO.LOW)
    time.sleep(3)
    wiringpi.digitalWrite(config.resetPin, GPIO.HIGH)
    print("Controller active")


def enableControllerSignalling():
    print("Start Polling")
    wiringpi.digitalWrite(config.pollingSignalPin, GPIO.HIGH)

def disableControllerSignalling():
    print("Stop Polling")
    wiringpi.digitalWrite(config.pollingSignalPin, GPIO.LOW)

ser = serial.Serial("/dev/ttyS1")

def handleInputFeed():
    global serialHandler

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

                print("Inbound command: " + str(newCommand))
            else:
                print("Unexpected Input")
                print(command)
                disableControllerSignalling()
                resetControllerModule()
                enableControllerSignalling()