echo "  manual_check_switch"
echo =======================
echo
echo Manually check if a endswitch is working
echo " -> ATTENTION: Must be executed in the projects root folder"
echo
echo Selected switch: $2
echo " -> Pin: $1"
echo

. "code/scripts/env.sh"
echo

cd "code/syact"

cargo run --features=rasp --example hardware-meas-endswitch -- $1

cd "../.."