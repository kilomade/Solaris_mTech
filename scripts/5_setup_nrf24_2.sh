#!/bin/bash

INSTALL_PATH="."
INSTALL_DIR="/rf24libs"

ROOT_PATH=${INSTALL_PATH}
ROOT_PATH+=${INSTALL_DIR}

echo""
echo "RF24 libraries installer by TMRh20"
echo "report issues at https://github.com/TMRh20/RF24/issues"
echo ""
echo "******************** NOTICE **********************"
echo "Installer will create an 'rf24libs' folder for installation of selected libraries"
echo "To prevent mistaken deletion, users must manually delete existing library folders within 'rf24libs' if upgrading"
echo "Run 'sudo rm -r rf24libs' to clear the entire directory"
echo ""
echo ""

echo "Prerequisite: GIT "
sudo apt-get install git -y
DORF24=1
DORF24Network=1
DORF24Mesh=1
DORF24Gateway=1

sudo apt-get install libncurses5-dev -y

echo "Installing RF24 Repo..."
git clone https://github.com/tmrh20/RF24.git ${ROOT_PATH}/RF24
cd ${ROOT_PATH}/RF24
./configure --driver=wiringPi
make -C ${ROOT_PATH}/RF24
sudo make install -C ${ROOT_PATH}/RF24

echo "Installing RF24Network Repo..."
git clone https://github.com/tmrh20/RF24Network.git ${ROOT_PATH}/RF24Network
make -B -C ${ROOT_PATH}/RF24Network
sudo make install -C ${ROOT_PATH}/RF24Network

echo "Installing RF24Mesh Repo..."
git clone https://github.com/tmrh20/RF24Mesh.git ${ROOT_PATH}/RF24Mesh
make -B -C ${ROOT_PATH}/RF24Mesh
sudo make install -C ${ROOT_PATH}/RF24Mesh

echo "Installing RF24Gateway Repo..."
git clone https://github.com/tmrh20/RF24Gateway.git ${ROOT_PATH}/RF24Gateway
make -B -C ${ROOT_PATH}/RF24Gateway
sudo make install -C ${ROOT_PATH}/RF24Gateway

make -B -C${ROOT_PATH}/RF24Gateway/examples/ncurses
ls ${ROOT_PATH}


echo ""
echo ""
echo "*** Installer Complete ***"
echo "See http://tmrh20.github.io for documentation"
echo "See http://tmrh20.blogspot.com for info "
echo ""
echo "Listing files in install directory rf24libs/"
ls ${ROOT_PATH}



