
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install x11vnc net-tools

sudo apt install libopengl0 -y
sudo add-apt-repository -y ppa:liujianfeng1994/panfork-mesa
sudo add-apt-repository -y ppa:liujianfeng1994/rockchip-multimedia
sudo apt update -y
sudo apt dist-upgrade -y
sudo apt install -y mali-g610-firmware rockchip-multimedia-config

#prereqs for Playstation
sudo apt-get install -y libsdl2-2.0

#emulator for Playstation
sudo apt-get install -y PCSX
