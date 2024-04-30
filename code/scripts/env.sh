# Helper script that sets all the environment variables needed

echo "Setting environment variables ..."

# General
export DRAI_DIR="~/DrAI"
export DRAI_LOG_DIR="/logs"

# Networking
export DRAI_CAMERA_PORT=40324
export DRAI_SERVER_PORT=40325

export DRAI_CAMERA_USER_FILE="/key/drai-camera/username.key"
export DRAI_CAMERA_PW_FILE="/key/drai-camera/password.key"
export DRAI_CTRL_USER_FILE="/key/drai-ctrl/username.key"
export DRAI_CTRL_PW_FILE="/key/drai-ctrl/password.key"
export DRAI_SERVER_USER_FILE="/key/drai-server/username.key"
export DRAI_SERVER_PW_FILE="/key/drai-server/password.key"

# Controls
## Stepper 
export DRAI_STEPPER_VOLTAGE=24

### X-Axis
export DRAI_X_AXIS_STEP_PIN=18
export DRAI_X_AXIS_DIR_PIN=17

export DRAI_X_SWITCH_POS_PIN=12
export DRAI_X_SWITCH_NEG_PIN=23

export DRAI_X_MICROSTEPS=1

### Y-Axis
export DRAI_Y_AXIS_STEP_PIN=9
export DRAI_Y_AXIS_DIR_PIN=10

export DRAI_Y_SWITCH_POS_PIN=22
export DRAI_Y_SWITCH_NEG_PIN=0

export DRAI_Y_MICROSTEPS=1

### Z-Axis
export DRAI_Z_AXIS_STEP_PIN=8
export DRAI_Z_AXIS_DIR_PIN=11

export DRAI_Z_SWITCH_POS_PIN=0
export DRAI_Z_SWITCH_NEG_PIN=0

export DRAI_Z_MICROSTEPS=1



echo " -> done!"