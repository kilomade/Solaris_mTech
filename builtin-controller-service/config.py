serialPort = "/dev/ttyS1"
serialBaudRate = 115200
commandFile=None

#These are wiringPi pin listing
#   'gpio readall'
serialRx = 0   #device is /dev/ttyS1
serialTx = 1
resetPin = 2
pollingSignalPin = 5

buttonDelay = 0.025