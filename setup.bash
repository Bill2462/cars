# Disable boot to GUI
sudo systemctl set-default multi-user

# Reboot here
sudo apt update && sudo apt upgrade -y

# Delete unnecessary packages.
sudo apt purge libreoffice-* -y
sudo apt purge thunderbird chromium-browser rhythmbox -y

sudo systemctl disable docker --now
sudo systemctl disable containerd --now
sudo systemctl disable whoopsie --now

# Install necessary packages using apt.
sudo apt install nvidia-jetpack htop nano python3-pip git cmake libpython3-dev \
python3-numpy libzmq3-dev libjpeg-dev zlib1g-dev libopenblas-base libopenmpi-dev -y

sudo apt autoremove -y

sudo apt clean

#Add the folowing
# export CUDA_HOME=/usr/local/cuda
# Adds the CUDA compiler to the PATH
# export PATH=$CUDA_HOME/bin:$PATH
# Adds the libraries
# xport LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH

# Compiling opencv
# Copy buid_opencv.sh and patches folder to card. Or copy precompiled opencv_build.tar
# In both cases run
sh build_opencv.sh

# Install packages using pip.
sudo -H pip3 install jetson-stats traitlets flask pygamepad gunicorn packaging Adafruit-SSD1306
sudo -H pip3 install setuptools-scm==6.0.1
sudo -H pip3 install adafruit-circuitpython-servokit==1.3.8
sudo -H pip3 install --no-binary=:all: pyzmq
sudo -H pip3 install torch-1.10.0-cp36-cp36m-linux_aarch64.whl
sudo -H pip3 install 'pillow<9'
sudo -H pip3 install --global-option=build_ext \
--global-option="-I/usr/local/cuda-10/targets/aarch64-linux/include/" \
--global-option="-L/usr/local/cuda-10/targets/aarch64-linux/lib/" pycuda

# Copy torch-1.10.0-cp36-cp36m-linux_aarch64.whl file to jetson
git clone --branch v0.11.1 https://github.com/pytorch/vision torchvision
cd torchvision
sudo python3 setup.py install

# Or copy prebuilt torchvision package.
