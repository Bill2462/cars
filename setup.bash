sudo apt update && sudo apt upgrade -y

# Delete unnecessary packages.
sudo apt purge libreoffice-* -y
sudo apt purge thunderbird chromium-browser rhythmbox -y
sudo apt autoremove -y

# Install necessary packages using apt.
sudo apt install nvidia-jetpack htop nano python3-pip git cmake libpython3-dev python3-numpy libzmq3-dev -y

# Install packages using pip.
sudo -H pip3 install jetson-stats
sudo -H pip3 install setuptools-scm==6.0.1
sudo -H pip3 install adafruit-circuitpython-servokit==1.3.8
sudo -H pip3 install Adafruit-SSD1306
sudo -H pip3 install packaging
sudo -H pip3 install --no-binary=:all: pyzmq
sudo -H pip3 install flask pygamepad

# Remove unnecessary packages
sudo apt clean

# Disable garbage services.
sudo systemctl disable docker
sudo systemctl disable containerd

# Disable boot to GUI
sudo systemctl set-default multi-user
