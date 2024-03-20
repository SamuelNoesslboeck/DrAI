# Testing

In order to check the correct functionality, different routines have been created as shell scripts to execute and check the following components:

- [Testing](#testing)
  - [Axes](#axes)
    - [Test endswitches of each axis](#test-endswitches-of-each-axis)
    - [Test motor(s) of each axis](#test-motors-of-each-axis)
    - [Test all axes by driving to the home position](#test-all-axes-by-driving-to-the-home-position)
  - [Table](#table)

Note that you have to navigate to the projects root directory before using any testing scripts!

```sh
# For example:
cd ~/DrAI
# that is, if you have installed the project at the default location
```

## Axes

Each of the three axes of the robot can be tested in the following order:

- Test endswitches of each axis
- Test motor(s) of each axis
- Test all axes by driving to the home position

### Test endswitches of each axis

Each axis has a positive and a negative endswitch, so to test a specific switch type:

```sh
# Form:
# sh "code/scripts/test/endswitch_{orientation - pos/neg}_{axis - x/y/z}.sh"

# So for the positive endswitch of the X axis:
sh "code/scripts/test/endswitch_pos_x.sh"

# Or for the negative endswitch of the Y axis:
sh "code/scripts/test/endswitch_neg_y.sh"
```

The script will plot the current value of the input pin, which should be `true` by default and change to `false` once the input is triggered.

### Test motor(s) of each axis

To test wheiter the motor of an axis is moving correctly, run the following script:

```sh
# Form:
# sh "code/scripts/test/motor_{axis - x/y/z}.sh"

# For the Z-axis this would be
sh "code/scripts/test/motor_z.sh"
```

The script will then move the motor to both its endswitches, watch for stuttering or loud noise during the movement.

### Test all axes by driving to the home position

To finally test all axes together execute the script for driving to the home position.

```sh
sh "code/scripts/test/home_pos.sh"
```

## Table