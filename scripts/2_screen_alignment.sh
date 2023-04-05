#!/bin/bash

# Rotate the primary display 180 degrees
xrandr -display :0.0 --output HDMI-1 --rotate inverted
