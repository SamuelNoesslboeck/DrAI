# Scripts

Scripts and batch files required for setup, updating and maintaining

## General scripts

General purpose scripts

- [env](env.sh)(.sh/.bat): Sets all the environment variables required for other scripts, executing in advance will not be required!
- [setup](setup.sh)(.sh/.bat): Setup script that should be called after installing to ensure functionality
- [update](update.sh)(.sh/.bat): Updates all repos if there are any available

## [Start scripts](./start/)

Scripts for starting up the main processes for a specific device (e.g. drai-camera).

- [camera.sh](start/camera.sh)
- [ctrl.sh](start/ctrl.sh)
- [server.sh](start/server.sh)
  
## Test scripts

Scripts for testing the functionallity of electronics and connections.

- []

### Standard test routine

To run the full [standard test routine](./testing.sh) run:

```sh
# Go to the project root directory, default being:
cd ~/DrAI

sh "code/scripts/testing.sh"
```

## Calibration scripts

Scripts for the calibration of the robot.