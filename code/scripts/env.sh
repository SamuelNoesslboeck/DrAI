# Helper script that sets all the environment variables needed

echo "Setting environment variables ..."

# General
export DRAI_DIR="~/DrAI"
export DRAI_LOG_DIR="/logs"

# Networking
export DRAI_CAMERA_PORT=40324
export DRAI_POINTS_PORT=40325

export DRAI_CAMERA_USER_FILE="/key/drai-cam/username.key"
export DRAI_CAMERA_PW_FILE="/key/drai-cam/password.key"

# Controls
## Stepper 
### X-Axis
export DRAI_X_AXIS_STEP_PIN=12
export DRAI_X_AXIS_DIR_PIN=21
export DRAI_X_SWITCH_POS_PIN=5
export DRAI_X_SWITCH_NEG_PIN=0

### Y-Axis
export DRAI_Y_AXIS_STEP_PIN=20
export DRAI_Y_AXIS_DIR_PIN=13
export DRAI_Y_SWITCH_POS_PIN=6
export DRAI_Y_SWITCH_NEG_PIN=0

### Z-Axis
export DRAI_Z_AXIS_STEP_PIN=19
export DRAI_Z_AXIS_DIR_PIN=26
export DRAI_Z_SWITCH_POS_PIN=0
export DRAI_Z_SWITCH_NEG_PIN=0

echo " -> done!"