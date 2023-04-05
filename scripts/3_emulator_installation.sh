#!/bin/bash

#File lists
DOLPHIN_EMULATOR_INIT=/home/rdyn/tmpBuild/Emulators/GFX.ini
DOLPHIN_AUDIOPIPE_FILE=/usr/include/soundtouch/FIFOSamplePipe.h

function startupProcedure {
  #Enable all repositories
  sudo add-apt-repository -y "deb http://archive.ubuntu.com/ubuntu $(lsb_release -sc) main universe restricted multiverse"

  #Temporary directory
  mkdir /home/rdyn/tmpBuild | echo "tmpBuild Path exists"
  mkdir /home/rdyn/tmpBuild/Emulators | echo "tmpBuild/Emulators exists"
  mkdir /usr/RdynBin/ | echo "usr/RdynBin/ exists"
}

function cleanUpProcedure {
  rm -rf /home/rdyn/tmpBuild
}

function layFoundation {
  sudo apt-get update -y
  sudo apt-get upgrade -y
  sudo apt-get install -y git zip unzip wget gnutls-bin gawk
  sudo apt-get install -y x11vnc net-tools
  sudo apt install libopengl0 -y
  sudo add-apt-repository -y ppa:liujianfeng1994/panfork-mesa
  sudo add-apt-repository -y ppa:liujianfeng1994/rockchip-multimedia
  sudo apt update -y
  sudo apt dist-upgrade -y
  sudo apt install -y mali-g610-firmware rockchip-multimedia-config
}

function installRetroArch {
  echo "Installing RetroArch"
  sudo add-apt-repository -y ppa:libretro/stable && sudo apt-get update -y && sudo apt-get install retroarch -y
  sudo snap install retroarch
  echo "Completed RetroArch"
}
function installMoonlight {
  echo "Installing Moonlight"
  sudo snap install moonlight
  echo "Completed Moonlight"
}

function installPCSX2 {
  echo "Installing PCSX2"
  sudo apt-get install -y libsdl2-2.0
  sudo apt-get install -y PCSX
  echo "Completed PCSX2"
}

function installPCSXReloaded {
  echo "Installing PCSXR"
  sudo apt-get -y install pcsxr
  echo "Completed PCSXR"
}

function installSnapRPCS3 {
  echo "Installing RPCS3"
  sudo snap install rpcs3-emu -y
  echo "Completed RPCS3"
}

function installDolphinEmu {
  echo "Installing Dolphin Emulator"
  sudo apt-add-repository -y ppa:dolphin-emu/ppa
  sudo apt update -y
  sudo apt install -y dolphin-emu
  echo "Completed Dolphin Emulator"
}

#DO NOT CALL THIS FUNCTION. IT WILL BREAK A LOT OF STUFF.
function configureRetroPie {
  echo "Building RetroPie"
  sudo apt install -y git dialog unzip xmlstarlet
  sudo apt install -y lsb-release
  cd /home/rdyn/tmpBuild/Emulators/
  git clone --depth=1 https://github.com/RetroPie/RetroPie-Setup.git
  cd ./RetroPie-Setup
  ls -larth
  pwd
  chmod +x ./retropie_setup.sh
  echo "MANUAL STEP: RetroPie Dependency"
  pwd
  bash ./retropie_setup.sh
  echo "Build Completed: RetroPie Dependency"
}

function configureAetherSX2 {
	echo "Deploying AetherSX2"
	cd /home/rdyn/tmpBuild/Emulators/
  aws s3 cp s3://rdyn-artifacts-bucket-us-east-2/Emulators/Playstation/AetherSX2-alpha-1929.AppImage .
  mv AetherSX2-alpha-1929.AppImage /usr/RdynBin/AetherSX2-alpha-1929.AppImage
  chmod +x /usr/RdynBin/AetherSX2-alpha-1929.AppImage
	echo "Deployment Completed: AetherSX2"
}

function buildDolphinEmulator {
  #Build Dolphin Emulator
  echo "Building Dolphin"
  echo "Installing system dependencies"
  cd /home/rdyn/tmpBuild/Emulators/
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
  aws s3 cp s3://rdyn-artifacts-bucket-us-east-2/Emulators/Wii/GFX.ini GFX.ini
  mv ./GFX.ini /opt/retropie/configs/gc/Config/GFX.ini
  #if [ -f "$DOLPHIN_EMULATOR_INIT"; then
  #	echo "Move dolphin GFX.ini"
  #	mv
  #else
  #	echo "Pull dolphin GFX.ini from S3"
  #	aws s3 cp s3://rdyn-artifacts-bucket-us-east-2/Emulators/Wii/GFX.ini /home/orangepi/config/dolphin-emu/GFX.ini
  #fi
  echo "Buid Complete: Dolphin Emulator"
}

#DO NOT REALLY CALL THIS FUNCTION. IT WON'T BRICK BUT YOU WILL BE RUNNING A LATE NIGHT(S)
function installSteamLink {
	echo "Building Steam Link"
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
	cd /home/rdyn/tmpBuild/Emulators/
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
	echo "Build Completed: Steam Link"
}

cleanUpProcedure
#layFoundation
startupProcedure
#installRetroArch
#installMoonlight
#installPCSX2
#installPCSXReloaded
#installSnapRPCS3
configureRetroPie
#buildDolphinEmulator
#configureAetherSX2
#cleanUpProcedure