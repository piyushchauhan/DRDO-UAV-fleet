## initial setup-prerequisites ##

sudo apt install libnl-3-dev libnl-genl-3-dev
sudo apt-get install git
git clone https://git.open-mesh.org/batctl.git
cd batctl
sudo make install
sudo apt-get install alfred

## procedure to setup ##

sudo bash service wpa_supplicant stop
sudo systemctl mask wpa_supplicant.service
sudo update-rc.d dhcpcd disable
sudo ip link set wlan0 down
sudo systemctl stop dhcpcd
sudo iw wlan0 set type ibss
sudo ifconfig wlan0 mtu 1500
sudo iwconfig wlan0 channel 3
sudo ip link set wlan0 up
sudo iw wlan0 ibss join <ssid> 2432           ## <ssid> = my-mesh-network
sudo modprobe batman-adv
sudo batctl if add wlan0
sudo ip link set up dev wlan0
sudo ip link set up dev bat0
sudo ifconfig bat0 172.27.2.1/16              ## ip adrress to be changed ##
