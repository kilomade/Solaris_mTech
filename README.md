# Project Solaris_mTech(RDYN)
## Experience the Future of Gaming, Streaming, and Creativity - All in the Palm of Your Hand!



## Features

- Retro emulation up to PS2
- Educational application for students
- Cybersecurity applications for 

## Capabilities
- Streaming via Moonlight services for Xbox, Playstation, PC
- Tunnelling service for away from home gaming
- DAW for audio production
- Gimp for image editing
- SFTP for secure remote file management
- Integrated into Dropbox/Google Drive

RDYN is a new concept of where we are enabling multi-functional hardware that is focused minimizing the footprint
of computing technologies

## Tech

Dillinger uses a number of open source projects to work properly:

- [Orange Pi 5] - Latest Advanced IoT board utilizing RK3588S, NVME on PCIE 2
- [VisionOS] - Lightweight debian-based OS that is fully capable Operating System
- [NRF] - Markdown parser done right. Fast and easy to extend.
- []


## Feature Descriptions

Base OS: Ubuntu 22.04(Jammy Jellyfish)

Scripts Location: script/
System Services: system-services/

Input Controls:
- Controller ESP: 
  - Purpose: Code logic for the subcontroller
  - Type: Microppython script
  - Code: 
    - builtin-controller
    - builtin-controller-circuitpython(Current)
- Controller Emulation:
  - Purpose: Python program that interprets inputs from the Controller ESP and emulates XBOX controller
  - Type: Python script, Linux service[ builtincontroller.service ]
  - Code:
    - builtin-controller-service
- Touchscreen Interface:
  - Purpose: Adds support for touchscreen main display
  - Type: Bash , Linux service[ screen-rotation.service ]
  - Code:
    - system-services/screen-rotation.service
- X11VNC:
  - Purpose: Remote desktop capability
  - Type: Bash, Linux service[ x11-vnc-local.service ]


## Environment Build Scripts
Location: scripts/

Order of Execution:
1. System setup
   1. Script: 1_system_setup.sh
      1. Use Case: configures OnScreen Keyboard, AWS, and SNAP store
2. Screen alignment
   1. 2_screen_alignment.sh
      1. Use Case: rotates the screen 180 to align with controller. 
   2. 2_touch_calibration.sh
      1. Use Case: must be implemented to align the touch screen with the rotated display
3. Emulation foundation
   1. 3_emulator_installation.sh
      1. Use Case: enables GPU acceleration for MALI G610. Can optionally install
         - RetroARch 
         - Moonlight
         - PCSX2
         - PCSXReloaded
         - RPCS3
         - Dolphin
   2. 3_retropie_ubuntu.sh( DO NOT USE, IW)
      1. Use Case: custom retropie installation script that supports OrangePi 5 boards
4. NRF Communications
   1. 5_setup_rf24.sh( complex, needs refractoring)
      1. Use Case: installs and configures system dependences for NRF communications under C++/Python, requires manual steps
   2. 5_setup_rf24_2.sh( In-Use )
      1. Use Case: automated


## Linux Services

The following underlying services are embedded

| Plugin  | Automation | URL                                                                   | Comment                  |
|---------|------------|-----------------------------------------------------------------------|--------------------------|
| X11 VNC |            |                                                                       |                          |
| Anbox   |            | [ Link ](https://www.makeuseof.com/tag/run-android-apps-games-linux/) | Android system emulation |

## Development




## Docker Services

Services implemented using containerization

| Service              | Description                                                        | Active | Ports | Internal/External | Comments                     |
|----------------------|--------------------------------------------------------------------|-------|-------|-------------------|------------------------------|
| SFTP                 | Used for transferring games/roms on local network                  |       |       | External          | No device level SFTP allowed |
| Dropbox/Google Drive | Used for syncing game saves/configs                                |       |       | Internal          |                              |
| AWS S3 Config Store  | Used for pulling in-house config specs for each supported emulator |       |       | Internal          |                              |
| Netswarmer           | Used for remote service connections for Streaming                  |       |       | Internal          |                              |
|                      |                                                                    |       |       |                   |                              |


