#!/bin/bash

gpio mode 2 out
gpio mode 5 out
gpio write 2 0
gpio write 5 0
sleep 5
gpio write 2 1
gpio write 5 1