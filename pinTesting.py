from machine import Pin, ADC
import utime


pushButtonA = Pin(17, Pin.IN)
pushButtonB = Pin(5, Pin.IN)
pushButtonX = Pin(18, Pin.IN)
pushButtonY = Pin(19, Pin.IN)

pushButtonUp = Pin(16, Pin.IN)
pushButtonDown = Pin(2, Pin.IN)
pushButtonLeft = Pin(4, Pin.IN)
pushButtonRight = Pin(0, Pin.IN)

pushButtonHome = Pin(14, Pin.IN)
pushButtonBack = Pin(27, Pin.IN)
pushButtonPause = Pin(12, Pin.IN)

pushButtonTurbo = Pin(15, Pin.IN)

leftJoystickAxisX = ADC(Pin(35))
leftJoystickAxisY = ADC(Pin(32))
leftJoystickSwitch = Pin(34, Pin.IN)

rightJoystickAxisX = ADC(Pin(25))
rightJoystickAxisY = ADC(Pin(33))
rightJoystickSwitch = Pin(23, Pin.IN)

turboState = False

while True:
    leftXValue = leftJoystickAxisX.read_u16()
    leftYValue = leftJoystickAxisY.read_u16()
    leftSwitch = leftJoystickSwitch.value()
    
    print(leftXValue, leftYValue, leftSwitch)
    
    rightXValue = rightJoystickAxisX.read_u16()
    rightYValue = rightJoystickAxisY.read_u16()
    rightSwitch = rightJoystickSwtich.read_u16()
    
    buttonA = pushButtonA.value()
    buttonB = pushButtonB.value()
    buttonX = pushButtonX.value()
    buttonY = pushButtonY.value()
    
    buttonUp = pushButtonUp.value()
    buttonDown = pushButtonDown.value()
    buttonLeft = pushButtonLeft.value()
    buttonRight = pushButtonRight.value()
    
    buttonHome = pushButtonHome.value()
    buttonBack = pushButtonBack.value()
    buttonPause = pushButtonPause.value()
    
    if pushButtonTurbo.value():
        temp = !turboState
        turboState = temp
        
    


