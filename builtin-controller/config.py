movementPollingRate = 100
buttonPressDelay = 250

latchingMsgSleepDelay = 5

#Button mappings
#
#  Will always map to OrangePi UART1 for communication
#


buttonMap = {
    "esp-wroom-32": {
        "Reference": "https://lastminuteengineers.com/esp32-pinout-reference/",
        "pinmap": {
            "buttonHome": 23,
            "buttonTurbo": 22,
            "buttonPause": 21,
            "buttonA": 17,
            "buttonB": 5,
            "buttonX": 18,
            "buttonY": 19,
            "buttonJoySwitchRight": 16,
            "axisXRight": 2,
            'axisYRight': 4,
            "buttonRightShoulder": 15,
            "buttonRightTrigger": 13,
            "buttonUp": 32,
            "buttonDown": 35,
            "buttonLeft": 33,
            "buttonRight": 34,
            "buttonJoySwitchLeft": 26,
            "axisXLeft": 25,
            "axisYLeft": 27,
            "buttonLeftShoulder": 12,
            "buttonLeftTrigger": 14
        },
        "signalpin": None
    },
    "esp32-wroom-32d": {
        "Reference": "https://docs.espressif.com/projects/esp-idf/en/latest/esp32/_images/esp32-devkitC-v4-pinout.png",
        "pinmap": {
            "buttonHome": 23,
            "buttonTurbo": 22,
            "buttonPause": 21,
            "buttonA": 17,
            "buttonB": 5,
            "buttonX": 18,
            "buttonY": 19,
            "buttonJoySwitchRight": 16,
            "axisXRight": 0,
            'axisYRight': 4,
            # "buttonRightShoulder": 7,
            # "buttonRightTrigger": 2,
            "buttonUp": 36,
            "buttonDown": 39,
            "buttonLeft": 34,
            "buttonRight": 35,
            "buttonJoySwitchLeft": 32,
            "axisXLeft": 33,
            "axisYLeft": 25,
            # "buttonLeftShoulder": 26,
            # "buttonLeftTrigger": 27
        },
        "signalpin": 26
    }
}