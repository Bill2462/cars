# Setup procedure for the AI car

This document details what to do to replace the card image from scratch and how to flash new jetson cars.

## Setting up the board for SD card boot

Because we have a clone we need to flash the special system image into the EMCC and then change line in the configuration file so our kernel boots from the microSD card.

### Setting up the environment on the PC

This is done only once. This section is for installing SDK and downloading the jetpack image.

 - First install ubuntu 18.04 desktop on some computer (VM with USB passhtrough in theory should work but it causes many problems during flashing).
 - Create nvidia developer account and then download and install sdk manager following instructions from their website (https://developer.nvidia.com/drive/sdk-manager).
 - Open sdkmanage by typing `sdkmanager` in the console.
 - Login to you nvidia developer account.
 - Short-circuit the FC REC and GND pins on the nvidia jetson board and connect it to the computer through microUSB cable Do not plug in the cable that connects it to the rest of the car!!
 - A prompt should pop up that the board is detected. Select jetson nano in this prompt.
 - In jetpack options select latest jetpack image, uncheck Host Machine and click CONTINUE.
 - Select Jetson OS, and remove the option of Jetson SDK Components. Check the protocol and click CONTINUE.
 - Starting from JetPack version 4.6.1, the pre-config window will pop up when programming the system with SDK Manager. Select manual setup and oem to runtime.
 - Wait until operations are complete.

### Mdyfing the device tree

This is done only once when new image is downloaded. This section is for modyfing device tree on the jetpack image so system detects microSD card.

 - Install device tree compiler on the host machine. `sudo apt install device-tree-compiler`
 - In your home folder there should be a directory called `nvidia`. In the console type `cd nvidia/nvidia_sdk/` and then list sdks by typing `ls`.
 - Go to the downloaded SDK that will be displayed by `ls` (there should be one) by typing `cd NAME OF THE SDK`.
 - Go to the device tree by running `cd Linux_for_Tegra/kernel/dtb`.
 - Decompile device tree by running `dtc -I dtb -O dts -o tegra210-p3448-0002-p3449-0000-b00.dts tegra210-p3448-0002-p3449-0000-b00.dtb`.
 - Open tegra210-p3448-0002-p3449-0000-b00.dts file in a text editor. It is saved in nvidia/nvidia_sdk/SDK_NAME/kernel/dtb
 - Find section `sdhci@700b0400`.
 - Change `status = "disabled";` to `status = "okay";`.
 - Add the following section after `vmmc-supply` line:

```
cd-gpios = <0x5b 0xc2 0x0>;
sd-uhs-sdr104;
sd-uhs-sdr50;
sd-uhs-sdr25;
sd-uhs-sdr12;
```

 - Add the following section after `mmc-ddr1_8v` line:

```
no-mmc;
uhs-mask = <0xc>;
```

 - Compile device tree `dtc -I dts -O dtb -o tegra210-p3448-0002-p3449-0000-b00.dtb tegra210-p3448-0002-p3449-0000-b00.dts`.

### Flashing the image into the jetson EMCC

This is done for every new jetson once.

Short-circuit the FC REC and GND pins on the nvidia jetson board and connect it to the computer through microUSB cable Do not plug in the cable that connects it to the rest of the car!!

Now on the computer go to `~/nvidia/nvidia_sdk/NAME_OF_THE_JETSON_SDK/Linux_for_Tegra` using `cd`. Then run `sudo ./flash.sh jetson-nano-emmc mmcblk0p1`. Wait until the flashing is completed. If flashing fails just rerun the flash script and try again.

### Copying image to the microSD card

This is done as a first step to "Preparing card image from scratch".

First connect monitor, keyboard to the jetson. Also insert microSD to the card slot. Then connect power. System should boot and display initial config wizard. Set the username to jetson and password to jetson (default for this course).

Once desktop is shown go to the console and type `sudo ls /dev/mmcblk* `. See if on the displayed list of devices there is `mmcblk1p`. If it is there then the microSD card is detected.

Then format the card using `sudo mkfs.ext4 /dev/mmcblk1` command. Then once card formatting is completed mount it using `sudo mount /dev/mmcblk1 /mnt`.
Then copy the rootfs using `sudo cp -ax / /mnt`. Then unmount the card `sudo umount /mnt/`.

### Configuring EMCC image for microSD boot

This is done for every new jetson once.

First connect monitor, keyboard to the jetson. Also insert microSD to the card slot. Then connect power. System should boot and display initial config wizard. Since the system will boot from microSD we don't care about the username and password. Set to anything you like.

Then once desktop is shown open terminal and open extlinux.conf in vim `sudo vi /boot/extlinux/extlinux.conf` (then press insert to enable editing mode)..

Find the statement APPEND ${cbootargs} quiet root=/dev/mmcblk0p1 rw rootwait rootfstype=ext4 console=ttyS0,115200n8 console=tty0, modify mmcblk0p1 to mmcblk1. Then save file by pressing escape and then typing. :wq command.

## Flashing the prebuilt image and basic config

If we want to flash prebuilt image then we use balena etcher to flash the image into the card. Then we mount the card on the PC.

Then we connect camera and keyboard to the jetson and we login (user: jetson, password: jetson) and then we customize the host name:

`sudo nano /etc/hostname`

Then we edit the file with new hostname.

Then type in `nmcli device widi connect  "<ssid_name>" password "<password>"`

## Preparing card image from scratch

This section assumes that clean image is installed on the microSD card (from setting up the board for SD card boot).

First boot the jetson and connect keyboard and mouse to it. It is then recommended to change power limit to MAXN. So this step does not proceed really slowly.
Then please connect board to wifi or to ethernet network with access to internet.

Now we will update and clean up the system and install necessary packages.

First we install necessary system updates:

```
sudo apt update && sudo apt upgrade -y
```

Then we remove unnecessary and bulky packages:

```
sudo apt purge libreoffice-* -y
sudo apt purge thunderbird chromium-browser rhythmbox -y
sudo apt autoremove -y
```

Then we install all necessary packages from apt:

```
sudo apt install nvidia-jetpack htop nano python3-pip git cmake libpython3-dev python3-numpy libzmq3-dev -y
```

Then we install necessary packges from PIP:

```
sudo -H pip3 install jetson-stats
sudo -H pip3 install setuptools-scm==6.0.1
sudo -H pip3 install adafruit-circuitpython-servokit==1.3.8
sudo -H pip3 install Adafruit-SSD1306
sudo -H pip3 install packaging
sudo -H pip3 install --no-binary=:all: pyzmq
```

Then we built jetson-inference package:

```
git clone --recursive https://github.com/dusty-nv/jetson-inference
cd jetson-inference
mkdir build
cd build
cmake ..
make -j$(nproc)
sudo make install
sudo ldconfig
```

Please unselect all models during prompt that will popup when running cmake ... And then skip pytorch installation. We will do all training on a different computer.

Then we clean some space on the harddrive:

```
sudo apt clean
sudo rm -rf *
```

Now we disable docker and containerd services.

```
sudo systemctl disable docker
sudo systemctl disable containerd
```

To disable desktop we run:

```
sudo systemctl set-default multi-user
```
