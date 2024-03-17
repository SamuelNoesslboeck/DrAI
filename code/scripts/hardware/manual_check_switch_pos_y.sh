. "code/scripts/env.sh"

# Arguments
export PIN = $DRAI_X_SWITCH_POS_PIN
export NAME = "X-Axis positive"

sh "code/scripts/hardware/manual_check_switch.sh" $DRAI_Y_SWITCH_POS_PIN "X-Axis Positive"