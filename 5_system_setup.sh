#!/bin/bash

function startupProcedure {
  #Enable all repositories
  sudo add-apt-repository "deb http://archive.ubuntu.com/ubuntu $(lsb_release -sc) main universe restricted multiverse"

  #Temporary directory
  mkdir ~/tmpBuild | echo "tmpBuild Path exists"
  mkdir ~/tmpBuild/Emulators | echo "tmpBuild/Emulators exists"
  mkdir /usr/RdynBin/ | echo "usr/RdynBin/ exists"
}

#File lists
DOLPHIN_EMULATOR_INIT=/home/orangepi/tmpBuild/Emulators/GFX.ini
DOLPHIN_AUDIOPIPE_FILE=/usr/include/soundtouch/FIFOSamplePipe.h

function getScriptDependencies {
  sudo apt-get install -y git zip unzip wget gnutls-bin gawk
}

function configureOnscreenKeyboard {
  sudo apt-get install onboard -y
}

function configureAWS {
  curl "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip" -o "awscliv2.zip"
  unzip awscliv2.zip
  sudo ./aws/install --update
  aws configure set aws_access_key_id AKIAWXBPGPIP2UMUNZ5Z
  aws configure set aws_secret_access_key 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
  aws configure set region us-east-1
  aws configure set output json
}

function enableSnapStore {
  sudo apt update
  sudo apt install snapd -y
}

function configureSnapRPCS3 {
  sudo snap install rpcs3-emu -y
}

function configureRetroPie {
  echo "Building RetroPie"
  sudo apt install -y git dialog unzip xmlstarlet
  sudo apt install -y lsb-release
  cd ~/tmpBuild/Emulators/
  git clone --depth=1 https://github.com/RetroPie/RetroPie-Setup.git
  cd RetroPie-Setup/
  chmod +x retropi_setup.sh
  echo "MANUAL STEP: RetroPie Dependency"
  ./retropi_setup.sh
  echo "COMPLETED: RetroPie Dependency"
}

function configureAetherSX2 {
	echo "Building AetherSX2"        
	cd ~/tmpBuild/Emulators/
  aws s3 cp s3://rdyn-artifacts-bucket-us-east-2/Emulators/Playstation/AetherSX2-alpha-1929.AppImage .
  mv AetherSX2-alpha-1929.AppImage /usr/RdynBin/AetherSX2-alpha-1929.AppImage
  chmod +x /usr/RdynBin/AetherSX2-alpha-1929.AppImage
	echo "AetherSX2 is built"
}

function installPCSXReloaded {
  #Install PCSX-Reloaded
  echo "Installing PCSX-Reloaded"
  sudo apt-get -y install pcsxr
}

function buildDolphinEmulator {
        #Build Dolphin Emulator
  echo "Building Dolphin"
  echo "\tInstalling system dependencies"
  cd ~/tmpBuild/Emulators/
  aws s3 cp s3://rdyn-artifacts-bucket-us-east-2/Emulators/Wii/FIFOSamplePipe.h .
  aws s3 cp s3://rdyn-artifacts-bucket-us-east-2/Emulators/Wii/GFX.ini .
  echo "Temporary patch for FIFOSamplePipe.h"
  mv "$DOLPHIN_AUDIOPIPE_FILE" /usr/include/soundtouch/FIFOSamplePipe.h.bak
  mv FIFOSamplePipe.h "$DOLPHIN_AUDIOPIPE_FILE"
  git clone https://github.com/dolphin-emu/dolphin.git
  cd dolphin
  git submodule update --init
  #git checkout -f tags/5.0
  mkdir Build && cd Build
  sudo cmake ..
  sudo make
  sudo make install
  echo "Removed temporary patch for FIFOSamplePipe.h"
  mv /usr/include/soundtouch/FIFOSamplePipe.h.bak "$DOLPHIN_AUDIOPIPE_FILE"
  mv GFX.ini /opt/retropie/configs/gc/Config/GFX.ini
  #if [ -f "$DOLPHIN_EMULATOR_INIT"; then
  #	echo "Move dolphin GFX.ini"
  #	mv
  #else
  #	echo "Pull dolphin GFX.ini from S3"
  #	aws s3 cp s3://rdyn-artifacts-bucket-us-east-2/Emulators/Wii/GFX.ini /home/orangepi/config/dolphin-emu/GFX.ini
  #fi
}

function installSteamLink {
	echo "Installing the libc dependencies"
	#Reference: https://sourceware.org/glibc/wiki/Testing/Builds
	git clone https://sourceware.org/git/glibc.git
	cd glibc
	git checkout master
	mkdir /usr/RdynBin/glibc
	mkdir Build
	cd Build
	../configure --prefix=
	make
	make check
	make install DESTDIR=/usr/RdynBin/glibc
	echo "Pulling Steam dependencies"
	cd ~/tmpBuild/Emulators/
	aws s3 cp s3://rdyn-artifacts-bucket-us-east-2/Emulators/SteamLink/libappindicator1_0.4.92-7_armhf.deb .
	aws s3 cp s3://rdyn-artifacts-bucket-us-east-2/Emulators/SteamLink/libindicator7_0.5.0-4_armhf.deb .
	aws s3 cp s3://rdyn-artifacts-bucket-us-east-2/Emulators/SteamLink/steam_latest.deb .
	sudo mv ./lib* /tmp
	sudo mv ./steam_latest.deb /tmp
	sudo chown root:root /tmp/lib*
	sudo chown root:root /tmp/steam_latest.deb
	echo "Installing SteamLink"
	sudo apt install -y /tmp/lib*
	sudo apt install -y /tmp/steam_latest.deb
	sudo rm -r /tmp/lib*
	sudo rm /tmp/steam_latest.deb
}

function configureMoonlight {
  sudo apt-get install -y moonlight-embedded
}

#getScriptDependencies
#configureOnscreenKeyboard
#startupProcedure
#enableSnapStore
#configureAWS
#configureSnapRPCS3
#configureAetherSX2
#installPCSXReloaded
#buildDolphinEmulator
#configureRetroPie
#installSteamLink
