# Motor testing script

. "code/scripts/env.sh"
echo

cd "code/syact"

export MICRO=$3

# Positive direction
cargo run --features rasp --example hardware-stepper-fixed_dist -- $1 $2 

# Negative direction
cargo run --features rasp --example hardware-stepper-fixed_dist -- $1 $2 -- "-6.28"

unset MICRO

cd "../.."