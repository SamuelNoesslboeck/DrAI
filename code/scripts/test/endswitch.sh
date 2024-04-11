echo "  manual_check_switch"
echo =======================
echo
echo Manually check if a endswitch is working
echo " -> ATTENTION: Must be executed in the projects root folder"
echo

. "code/scripts/env.sh"
echo

cd "code/syact"

export SYACT_DEVICE_NAME=$2

cargo run --features rasp --example hardware-meas-endswitch -- $1

unset SYACT_DEVICE_NAME

cd "../.."