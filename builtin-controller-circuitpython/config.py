movementPollingRate = 100
buttonPressDelay = 350
holdButtonDelay = 250

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
            "buttonHomeTurbo": 23,
            "buttonBack": 22,
            "buttonPause": 21,
            "buttonA": 14,
            "buttonB": 5,
            "buttonX": 18,
            "buttonY": 19,
            "buttonJoySwitchRight": 12,
            "axisXRight": 0,
            'axisYRight': 4,
            "buttonRightShoulder": 13,
            "buttonRightTrigger": 2,
            "buttonJoySwitchLeft": 32,
            "axisXLeft": 33,
            "axisYLeft": 25,
            "buttonLeftShoulder": 26,
            "buttonLeftTrigger": 15,
            "buttonUp": 36,
            "buttonDown": 39,
            "buttonLeft": 34,
            "buttonRight": 35
        },
        "signalpin": 16,
        "tx": 1,
        "rx": 3,
        "hardware_specs": {
            "Joystick": {
                "MIN": 0,
                "MAX": 65535
            },
            "Trigger": {
                "MIN": 0,
                "MAX": 2
            }
        }
    }
}