#!/bin/bash

function layFoundation {
  sudo apt-get install -y gcc-arm-linux-gnueabihf
  sudo apt-get install -y g++-arm-linux-gnueabihf
  sudo -u rdyn bash -c 'mkdir /home/rdyn/tmpComm/' | echo "Directory exists"
  cp 5_setup_nrf24_2.sh /home/rdyn/tmpComm/
  cd /home/rdyn/tmpComm/
}

function cleanupFoundation {
  rm -rf /home/rdyn/tmpComm/
}

function layPiGpio {
  sudo -u rdyn bash -c 'wget https://github.com/joan2937/pigpio/archive/master.zip'
  sudo -u rdyn bash -c 'unzip master.zip'
  cd pigpio-master
  sudo -u rdyn bash -c 'make'
  sudo make install
  cd ..
}

function installRF24 {
  sudo -u rdyn bash -c 'mkdir tempNrfScript'
  cd ./tempNrfScript
  ls -la
  sudo -u rdyn bash -c './5_setup_nrf24_2.sh'
  cd ..
  echo "Installing RF24"
#  sudo -u rdyn bash -c 'git clone https://github.com/nRF24/RF24.git'
  sudo -u rdyn bash -c 'git clone https://git-codecommit.us-east-2.amazonaws.com/v1/repos/cfwRF24_OPi5'
  ls -larth
  sudo -u rdyn bash -c 'cd cfwRF24_OPi5'
  sudo -u rdyn bash -c 'git checkout development && git pull' | echo "Already cloned"
  sudo -u rdyn bash -c './configure'
  sudo -u rdyn bash -c 'make'
  sudo -u rdyn bash -c 'make install'
  make install
  cd ..
  echo "Completed RF24"
}

function installPyRFBasic {
  echo "Laying pyRF Basic components"
  apt-get install python3-dev libboost-python-dev python3-pip
  python3 -m pip install --upgrade pip setuptools
  ln -s $(ls /usr/lib/$(ls /usr/lib/gcc | tail -1)/libboost_python3*.so | tail -1) /usr/lib/$(ls /usr/lib/gcc | tail -1)/libboost_python3.so
  sudo -u rdyn bash -c 'git clone --recurse-submodules https://github.com/nRF24/pyRF24.git'
  cd ./pyRF24
}

function cycleBuild {
  python3 setup.py build
  python3 setup.py install
}

function installPyRF24 {
  echo "Installing pyRF24"
  cd ./RF24/pyRF24
  cycleBuild
  cd ../..
  echo "Completed pyRF24"
}

function installPyRF24Mesh {
  echo "Installing pyRF24Mesh"
  cd ./RF24Mesh/pyRF24Mesh
  cycleBuild
  cd .../..
  echo "Completed pyRF24Mesh"
}

function installPyRF24Network {
  echo "Installing installPyRF24Network"
  cd ./RF24Network/RPi/pyRF24Network
  cycleBuild
  cd ../../..
  echo "Completed PyRF24Network"
}

function runApplication {
  layFoundation
  layPiGpio
  installRF24
  installPyRFBasic
  installPyRF24
  installPyRF24Mesh
  installPyRF24Network
  #cleanupFoundation
}

rm 5_output.txt
runApplication >> 5_output.txt