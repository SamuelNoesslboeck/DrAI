# Helper build script for robot control

sh "code/scripts/setup.sh"

cd "code/drake_ctrl"

cargo build --verbose --features rasp

cd "../../"