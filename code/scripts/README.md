# Scripts

Scripts and batch files required for setup, updating and maintaining

## General scripts

General purpose scripts

- [env](env.sh)(.sh/.bat): Sets all the environment variables required for other scripts, executing in advance will not be required!
- [setup](setup.sh)(.sh/.bat): Setup script that should be called after installing to ensure functionality
- [update](update.sh)(.sh/.bat): Updates all repos if there are any available

## Start scripts

Scripts for starting up the main processes for a specific device (e.g. drai-camera).

- [camera.sh](start/camera.sh)
- [ctrl.sh](start/ctrl.sh)
- [server.sh](start/server.sh)
  
## Test scripts

Scripts for testing the functionallity of electronics and connections.

- [manual_switch_pos_x.sh](test/manual_switch_pos_x.sh): Tests whether the positive endswitch of the X-Axis is working
- [manual_switch_pos_y.sh](test/manual_switch_pos_x.sh): Tests whether the positive endswitch of the Y-Axis is working

## Calibration scripts

Scripts for the calibration of the robot.