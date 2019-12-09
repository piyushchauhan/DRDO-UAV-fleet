# Raspberry Pi Setup

# Commands
Download and extract raspbian img file.
Download balena etcher
Flash the image - (Takes 20 mins)
Make empty "ssh" file in boot
Insert SD card into RPi
Power the RPi

Wifi connection - set to shared mode
CMD:

--------------------------------------
```ipconfig
ping raspberrypi.local
ssh pi@raspberrypi.local
-yes
[ssh-keygen -R raspberrypi.local]
```
--------------------------------------
After logging into RPi
```
sudo apt-get update
date
date -s "<Current Date>"

sudo apt-get install python-opencv
```
-------------------------------------

install VNC viewer
install winSCP

CMD - ```vncserver```
copy the ip address at last - paste in vnc viewer - Enjoy the desktop

