# Setup

## Software

### Installation (Linux)

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

#### DrAI-Camera

To setup autostart and more for the camera, run the following script with `sudo` permissions:

```sh
sudo sh "code/scripts/setup/drai_camera.sh"
```

#### DrAI-Ctrl

To setup autostart and more for the robot control, run the following script with `sudo` permissions:

```sh
sudo sh "code/scripts/setup/drai_ctrl.sh"
```

#### DrAI-Server

To setup autostart and more for the robot control, run the following script with `sudo` permissions:

```sh
sudo sh "code/scripts/setup/drai_server.sh"
```

### After installation

Now the software is ready and will be started as a system process once the device is booted up!
Instead of starting the software manually, it is recommened to reboot the system.

```sh
sudo reboot
```

## Electronics

The electronics of the project are built into a small trunk equipped with the right connectors. In total, the following connectors with the given indexes have to be connected:

- **Power supply**
  - ( PSC ): Power supply for the camera
- **Stepper motors**
  - ( X ): The X-Axis stepper motor
  - ( Y ): The Y-Axis stepper motor
  - ( Z1 ): The left Z-Axis stepper motor (viewed from the front)
  - ( Z2 ): The right Z-Axis stepper motor (viewed from the front)
- **Endswitches**
  - ( X+ ): The positive X-Axis endswitch
  - ( X- ): The negative X-Axis endswitch
  - ( Y+ ): The positive Y-Axis endswitch
  - ( Y- ): The negative Y-Axis endswitch
  - ( Z+ ): The positive Z-Axis endswitch
  - ( Z- ): The negative Z-Axis endswitch
- **Extras**
  - ( BL ): Bed-Layer touch attached to the tool
  - ( SC ): The servo-controller board of the drawing table
- **Optional (might not be included)**
  - ( H1 ): First servo of the head
  - ( H2 ): Second servo of the head