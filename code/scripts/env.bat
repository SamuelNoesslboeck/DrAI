@REM Helper script for setting environment variables

@REM Networking
set DRAI_CAMERA_PORT=40324
set DRAI_POINTS_PORT=40325

set DRAI_CAMERA_USER_FILE="/key/drai-cam/username.key"
set DRAI_CAMERA_PW_FILE="/key/drai-cam/password.key"

@REM Controls
@REM  Stepper 
@REM   X-Axis
set DRAI_X_AXIS_STEP_PIN=12
set DRAI_X_AXIS_DIR_PIN=21
set DRAI_X_SWITCH_POS_PIN=5
set DRAI_X_SWITCH_NEG_PIN=0

@REM   Y-Axis
set DRAI_Y_AXIS_STEP_PIN=20
set DRAI_Y_AXIS_DIR_PIN=13
set DRAI_Y_SWITCH_POS_PIN=6
set DRAI_Y_SWITCH_NEG_PIN=0

@REM   Z-Axis
set DRAI_Z_AXIS_STEP_PIN=19
set DRAI_Z_AXIS_DIR_PIN=26
set DRAI_Z_SWITCH_POS_PIN=0
set DRAI_Z_SWITCH_NEG_PIN=0