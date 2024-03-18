# Setup

## Installation (Linux)

To install the software on all devices, simply clone the github repo **in your home folder**:

```sh
cd ~
git clone "https://github.com/SamuelNoesslboeck/DrAI.git"
```

After the clone is complete, go into the cloned directory and run the setup batch file

```sh
cd DrAI
sh "code/scripts/setup.sh"
```

The next step depends on *which device you are setting up*! 

### DrAI-Camera

To setup autostart and more for the camera, run the following script with `sudo` permissions:

```sh
sudo sh "code/scripts/setup/drai_camera.sh"
```

### DrAI-Ctrl

To setup autostart and more for the robot control, run the following script with `sudo` permissions:

```sh
sudo sh "code/scripts/setup/drai_ctrl.sh"
```

### DrAI-Server

To setup autostart and more for the robot control, run the following script with `sudo` permissions:

```sh
sudo sh "code/scripts/setup/drai_server.sh"
```

## After installation

Now the software is ready and will be started as a system process once the device is booted up!
Instead of starting the software manually it is recommened to reboot the system.

```sh
sudo reboot
```