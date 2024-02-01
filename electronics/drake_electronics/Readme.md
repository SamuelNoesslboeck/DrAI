# drake electronics

## Summary

The main electronics of the drake robot, including four stepper controllers, a high amount of measurement devices, sensors and up to two cameras.

## Stepper controllers

Supplied with a high voltage and current of 24-36V and ~2A the motors need a powerful controller that can manage high step frequencies as microstepping is used. Assuming a step count of 200 with a microstepping of 16, the frequency required to create a speed of 10rev/s evaluates to 32kHz, which is about the maximum for stepper motor controllers of this size.
