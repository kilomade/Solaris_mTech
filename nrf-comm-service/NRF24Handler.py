import time
from RF24 import *
from RF24Network import *
from RF24Mesh import *

# Set up radio
radio = RF24(0, 0)
network = RF24Network(radio)
mesh = RF24Mesh(radio, network)

# Set up addresses
this_node = mesh.getNodeID()
mesh.setNodeID(0)
mesh.begin()
radio.setPALevel(RF24_PA_MAX)

# Main loop
while True:
    mesh.update()

    # Check for incoming messages
    while network.available():
        header, payload = network.read(32)
        print("Received message from node {}: {}".format(header.from_node, payload.decode()))

    # Send a message every 5 seconds
    if time.monotonic() % 5 == 0:
        mesh.write("Hello from node {}".format(mesh.getNodeID()))

    time.sleep(0.1)
