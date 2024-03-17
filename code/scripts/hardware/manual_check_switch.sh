echo   manual_check_switch
echo =======================
echo
echo Manually check if a endswitch is working
echo  -> ATTENTION: Must be executed in the projects root folder
echo
echo Selected switch: $3
echo  -> Pin: $2
echo

sh "code/scripts/env.sh"

cd "code/syact"

cargo run --features=rasp --example hardware-meas-endswitch $2

cd "../.."