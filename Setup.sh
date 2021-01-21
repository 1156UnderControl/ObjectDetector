sudo apt -y update
sudo apt -y upgrade
sudo apt -y install python3-opencv
sudo pip3 install pynetworktables
sudo pip3 install "picamera[array]"
mkdir /home/pi/Desktop/object-detection
mkdir /home/pi/.config/autostart
chmod 777 /home/pi/Desktop/object-detection
chown pi:pi /home/pi/Desktop/object-detection
chmod 777 /home/pi/.config/autostart
chown pi:pi /home/pi/.config/autostart
sudo mv "/home/pi/Desktop/scripts/ObjectDetectorRuntime.desktop" "/home/pi/.config/autostart"
sudo rm "/home/pi/Desktop/Setup.sh"
sudo reboot