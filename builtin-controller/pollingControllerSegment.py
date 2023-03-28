from machine import Pin, ADC, UART
import utime
import time
import micropython
import config

#  
# Do not use EN - this will be wired to the orangepi for the power on/off functionality
# Do not use RX/TX(1,3)  I2C SCL(22/21)
#
controllerModel = "esp32-wroom-32d"

#HID objects - RIGHT HAND
pushButtonHome = Pin(config.buttonMap[controllerModel]["pinmap"]["buttonHome"], Pin.IN)
pushButtonTurbo = Pin(config.buttonMap[controllerModel]["pinmap"]["buttonTurbo"], Pin.IN)
pushButtonPause = Pin(config.buttonMap[controllerModel]["pinmap"]["buttonPause"], Pin.IN)

pushButtonA = Pin(config.buttonMap[controllerModel]["pinmap"]["buttonA"], Pin.IN)
pushButtonB = Pin(config.buttonMap[controllerModel]["pinmap"]["buttonB"], Pin.IN)
pushButtonX = Pin(config.buttonMap[controllerModel]["pinmap"]["buttonX"], Pin.IN)
pushButtonY = Pin(config.buttonMap[controllerModel]["pinmap"]["buttonY"], Pin.IN)

rightJoystickAxisX = ADC(Pin(config.buttonMap[controllerModel]["pinmap"]["axisXRight"]))
rightJoystickAxisY = ADC(Pin(config.buttonMap[controllerModel]["pinmap"]["axisYRight"]))
rightJoystickSwitch = Pin(config.buttonMap[controllerModel]["pinmap"]["buttonJoySwitchRight"], Pin.IN)

# pushButtonRightShoulder = Pin(config.buttonMap[controllerModel]["pinmap"]["buttonRightShoulder"], Pin.IN)
# pushButtonRightTrigger = Pin(config.buttonMap[controllerModel]["pinmap"]["buttonRightTrigger"], Pin.IN)

#HID object - LEFT HAND
pushButtonUp = Pin(config.buttonMap[controllerModel]["pinmap"]["buttonUp"], Pin.IN)
pushButtonDown = Pin(config.buttonMap[controllerModel]["pinmap"]["buttonDown"], Pin.IN)
pushButtonLeft = Pin(config.buttonMap[controllerModel]["pinmap"]["buttonLeft"], Pin.IN)
pushButtonRight = Pin(config.buttonMap[controllerModel]["pinmap"]["buttonRight"], Pin.IN)

leftJoystickAxisX = ADC(Pin(config.buttonMap[controllerModel]["pinmap"]["axisXLeft"]))
leftJoystickAxisY = ADC(Pin(config.buttonMap[controllerModel]["pinmap"]["axisYLeft"]))
leftJoystickSwitch = Pin(config.buttonMap[controllerModel]["pinmap"]["buttonJoySwitchLeft"], Pin.IN)

# pushButtonLeftShoulder = Pin(config.buttonMap[controllerModel]["pinmap"]["buttonLeftShoulder"], Pin.IN)
# pushButtonLeftTrigger = Pin(config.buttonMap[controllerModel]["pinmap"]["buttonLeftTrigger"], Pin.IN)

#HID signal object
outputPollSignal = Pin(config.buttonMap[controllerModel]["signalpin"], Pin.IN)

pollState = False

timingMap = {
    "A": 0,
    "B": 0,
    "X": 0,
    "Y": 0,
    "Up": 0,
    "Down": 0,
    "Left": 0,
    "Right": 0,
    "Home": 0,
    "Back": 0,
    "Pause": 0,
    "LeftSwitch": 0,
    "LeftShoulder": 0,
    "LeftTrigger": 0,
    "RightSwitch": 0,
    "RightShoulder": 0,
    "RightTrigger": 0,
    "Turbo": 0,
    "movement": 0
}

#REGION Communication logic

uart = UART(1, 115200)

def sendCommand(msg):
    global uart
    formattedMsg = "::" + msg + "::"
    print(formattedMsg)

#ENDREGION

#REGION Command interrupts

def buttonA_irq(state):
    global timingMap
    new_time = utime.ticks_ms()
    # if it has been more that 1/5 of a second since the last event, we have a new event
    if (new_time - timingMap["A"]) > config.buttonPressDelay: 
        sendCommand("A")
        timingMap["A"] = new_time

def buttonB_irq(state):
    global timingMap
    new_time = utime.ticks_ms()
    # if it has been more that 1/5 of a second since the last event, we have a new event
    if (new_time - timingMap["B"]) > config.buttonPressDelay: 
        sendCommand("B")
        timingMap["B"] = new_time

def buttonX_irq(state):
    global timingMap
    new_time = utime.ticks_ms()
    # if it has been more that 1/5 of a second since the last event, we have a new event
    if (new_time - timingMap["X"]) > config.buttonPressDelay: 
        sendCommand("X")
        timingMap["X"] = new_time

def buttonY_irq(state):
    global timingMap
    new_time = utime.ticks_ms()
    # if it has been more that 1/5 of a second since the last event, we have a new event
    if (new_time - timingMap["Y"]) > config.buttonPressDelay: 
        sendCommand("Y")
        timingMap["Y"] = new_time

def buttonUp_irq(state):
    global timingMap
    new_time = utime.ticks_ms()
    # if it has been more that 1/5 of a second since the last event, we have a new event
    if (new_time - timingMap["Up"]) > config.buttonPressDelay: 
        sendCommand("Up")
        timingMap["Up"] = new_time

def buttonDown_irq(state):
    global timingMap
    new_time = utime.ticks_ms()
    # if it has been more that 1/5 of a second since the last event, we have a new event
    if (new_time - timingMap["Down"]) > config.buttonPressDelay: 
        sendCommand("Down")
        timingMap["Down"] = new_time

def buttonLeft_irq(state):
    global timingMap
    new_time = utime.ticks_ms()
    # if it has been more that 1/5 of a second since the last event, we have a new event
    if (new_time - timingMap["Left"]) > config.buttonPressDelay: 
        sendCommand("Left")
        timingMap["Left"] = new_time

def buttonRight_irq(state):
    global timingMap
    new_time = utime.ticks_ms()
    # if it has been more that 1/5 of a second since the last event, we have a new event
    if (new_time - timingMap["Right"]) > config.buttonPressDelay: 
        sendCommand("Right")
        timingMap["Right"] = new_time

def buttonHome_irq(state):
    global timingMap
    new_time = utime.ticks_ms()
    # if it has been more that 1/5 of a second since the last event, we have a new event
    if (new_time - timingMap["Home"]) > config.buttonPressDelay: 
        sendCommand("Home")
        timingMap["Home"] = new_time

def buttonBack_irq(state):
    global timingMap
    new_time = utime.ticks_ms()
    # if it has been more that 1/5 of a second since the last event, we have a new event
    if (new_time - timingMap["Back"]) > config.buttonPressDelay: 
        sendCommand("Back")
        timingMap["Back"] = new_time

def buttonPause_irq(state):
    global timingMap
    new_time = utime.ticks_ms()
    # if it has been more that 1/5 of a second since the last event, we have a new event
    if (new_time - timingMap["Pause"]) > config.buttonPressDelay: 
        sendCommand("Pause")
        timingMap["Pause"] = new_time

def buttonTurbo_irq(state):
    global timingMap
    new_time = utime.ticks_ms()
    # if it has been more that 1/5 of a second since the last event, we have a new event
    if (new_time - timingMap["Turbo"]) > config.buttonPressDelay: 
        sendCommand("Turbo State Change")
        timingMap["Turbo"] = new_time

def buttonRightSwitch_irq(state):
    global timingMap
    new_time = utime.ticks_ms()
    # if it has been more that 1/5 of a second since the last event, we have a new event
    if (new_time - timingMap["RightSwitch"]) > config.buttonPressDelay: 
        sendCommand("Right Switch")
        timingMap["RightSwitch"] = new_time

def buttonLeftSwitch_irq(state):
    global timingMap
    new_time = utime.ticks_ms()
    # if it has been more that 1/5 of a second since the last event, we have a new event
    if (new_time - timingMap["LeftSwitch"]) > config.buttonPressDelay: 
        sendCommand("Left Switch")
        timingMap["LeftSwitch"] = new_time

# def triggerReadRightTrigger_irq(state):
#     #TODO implement range read and send
#     pass

# def triggerReadLeftTrigger_irq(state):
#     #TODO implment range read and send
#     pass

# def buttonRightShoulder_irq(state):
#     global timingMap
#     new_time = utime.ticks_ms()
#     # if it has been more that 1/5 of a second since the last event, we have a new event
#     if (new_time - timingMap["RightShoulder"]) > config.buttonPressDelay: 
#         sendCommand("Right Shoulder")
#         timingMap["RightShoulder"] = new_time

# def buttonLeftShoulder_irq(state):
#     global timingMap
#     new_time = utime.ticks_ms()
#     # if it has been more that 1/5 of a second since the last event, we have a new event
#     if (new_time - timingMap["LeftShoulder"]) > config.buttonPressDelay: 
#         sendCommand("Left Shoulder")
#         timingMap["LeftShoulder"] = new_time

# pushButtonA.irq(handler=buttonA_irq, trigger=Pin.IRQ_RISING)
# pushButtonB.irq(handler=buttonB_irq, trigger=Pin.IRQ_RISING)
# pushButtonX.irq(handler=buttonX_irq, trigger=Pin.IRQ_RISING)
# pushButtonY.irq(handler=buttonY_irq, trigger=Pin.IRQ_RISING)

# pushButtonUp.irq(handler=buttonUp_irq, trigger=Pin.IRQ_RISING)
# pushButtonDown.irq(handler=buttonDown_irq, trigger=Pin.IRQ_RISING)
# pushButtonLeft.irq(handler=buttonLeft_irq, trigger=Pin.IRQ_RISING)
# pushButtonRight.irq(handler=buttonRight_irq, trigger=Pin.IRQ_RISING)

pushButtonHome.irq(handler=buttonHome_irq, trigger=Pin.IRQ_RISING)
# pushButtonBack.irq(handler=buttonBack_irq, trigger=Pin.IRQ_RISING)
pushButtonPause.irq(handler=buttonPause_irq, trigger=Pin.IRQ_RISING)
pushButtonTurbo.irq(handler=buttonTurbo_irq, trigger=Pin.IRQ_RISING)

# leftJoystickSwitch.irq(handler=buttonLeftSwitch_irq, trigger=Pin.IRQ_RISING)
# rightJoystickSwitch.irq(handler=buttonRightSwitch_irq, trigger=Pin.IRQ_RISING)



# pushButtonRightShoulder.irq(handler=buttonRightShoulder_irq, trigger=Pin.IRQ_RISING)
# pushButtonLeftShoulder.irq(handler=buttonLeftShoulder_irq, trigger=Pin.IRQ_RISING)

# pushButtonRightTrigger.irq(handler=triggerReadRightTrigger_irq, trigger=Pin.IRQ_RISING|Pin.IRQ_FALLING)
# pushButtonLeftTrigger.irq(handler=triggerReadLeftTrigger_irq, trigger=Pin.IRQ_RISING|Pin.IRQ_FALLING)

#ENDREGION

def pollMovement():
    movementMap = {
    "leftXValue": leftJoystickAxisX.read_u16(),
    "leftYValue": leftJoystickAxisY.read_u16(),
    "rightXValue": rightJoystickAxisX.read_u16(),
    "rightYValue": rightJoystickAxisY.read_u16()
    }

    movementPayload = "Movement -- {} {} {} {}"
    sendCommand(movementPayload.format(movementMap["leftXValue"], movementMap["leftYValue"]), movementMap["rightXValue"], movementMap["rightYValue"])

while outputPollSignal.value() == 0:
    sendCommand("Awaiting polling request")

sendCommand("Sending commands")

while True:
    while outputPollSignal.value() == 1:
        pollMovement()

        new_time = utime.ticks_ms()
        # if it has been more that 1/5 of a second since the last event, we have a new event
        if (new_time - timingMap["A"]) > config.buttonPressDelay: 
            sendCommand("A")
            timingMap["A"] = new_time
        
        pollMovement()

        new_time = utime.ticks_ms()
        # if it has been more that 1/5 of a second since the last event, we have a new event
        if (new_time - timingMap["B"]) > config.buttonPressDelay: 
            sendCommand("B")
            timingMap["B"] = new_time
        
        pollMovement()

        new_time = utime.ticks_ms()
        # if it has been more that 1/5 of a second since the last event, we have a new event
        if (new_time - timingMap["X"]) > config.buttonPressDelay: 
            sendCommand("X")
            timingMap["X"] = new_time
        
        pollMovement()

        new_time = utime.ticks_ms()
        # if it has been more that 1/5 of a second since the last event, we have a new event
        if (new_time - timingMap["Y"]) > config.buttonPressDelay: 
            sendCommand("Y")
            timingMap["Y"] = new_time
        
        pollMovement()

        new_time = utime.ticks_ms()
        # if it has been more that 1/5 of a second since the last event, we have a new event
        if (new_time - timingMap["Up"]) > config.buttonPressDelay: 
            sendCommand("Up")
            timingMap["Up"] = new_time
        
        pollMovement()

        new_time = utime.ticks_ms()
        # if it has been more that 1/5 of a second since the last event, we have a new event
        if (new_time - timingMap["Down"]) > config.buttonPressDelay: 
            sendCommand("Down")
            timingMap["Down"] = new_time
        
        pollMovement()

        new_time = utime.ticks_ms()
        # if it has been more that 1/5 of a second since the last event, we have a new event
        if (new_time - timingMap["Left"]) > config.buttonPressDelay: 
            sendCommand("Left")
            timingMap["Left"] = new_time
        
        pollMovement()

        new_time = utime.ticks_ms()
        # if it has been more that 1/5 of a second since the last event, we have a new event
        if (new_time - timingMap["Right"]) > config.buttonPressDelay: 
            sendCommand("Right")
            timingMap["Right"] = new_time
        
        pollMovement()

        new_time = utime.ticks_ms()
        # if it has been more that 1/5 of a second since the last event, we have a new event
        if (new_time - timingMap["Back"]) > config.buttonPressDelay: 
            sendCommand("Back")
            timingMap["Back"] = new_time
        
        pollMovement()

        new_time = utime.ticks_ms()
        # if it has been more that 1/5 of a second since the last event, we have a new event
        if (new_time - timingMap["Pause"]) > config.buttonPressDelay: 
            sendCommand("Pause")
            timingMap["Pause"] = new_time

        pollMovement()

        new_time = utime.ticks_ms()
        # if it has been more that 1/5 of a second since the last event, we have a new event
        if (new_time - timingMap["RightSwitch"]) > config.buttonPressDelay: 
            sendCommand("Right Switch")
            timingMap["RightSwitch"] = new_time
        
        pollMovement()

        new_time = utime.ticks_ms()
        # if it has been more that 1/5 of a second since the last event, we have a new event
        if (new_time - timingMap["LeftSwitch"]) > config.buttonPressDelay: 
            sendCommand("Left Switch")
            timingMap["LeftSwitch"] = new_time
        
        # pollMovement()

        # new_time = utime.ticks_ms()
        # # if it has been more that 1/5 of a second since the last event, we have a new event
        # if (new_time - timingMap["RightShoulder"]) > config.buttonPressDelay: 
        #     sendCommand("Right Shoulder")
        #     timingMap["RightShoulder"] = new_time
        
        # pollMovement()

        # new_time = utime.ticks_ms()
        # # if it has been more that 1/5 of a second since the last event, we have a new event
        # if (new_time - timingMap["LeftShoulder"]) > config.buttonPressDelay: 
        #     sendCommand("Left Shoulder")
        #     timingMap["LeftShoulder"] = new_time

