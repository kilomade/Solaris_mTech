import evdev

# Replace with the name of your uinput device
device_name = "python-uinput"

# Find the uinput device with the given name
devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
print(devices)
device = None
for dev in devices:
    if dev.name == device_name:
        device = dev
        break

# If no device was found, print an error and exit
if not device:
    print(f"No device found with name {device_name}")
    exit(1)

# Loop infinitely, reading events from the device and printing them
for event in device.read_loop():
    print(evdev.categorize(event))
