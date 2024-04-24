use pwm_pca9685::{Address, Channel, Pca9685};
use rppal::i2c::I2c;

use syact::Setup;
use syact::units::*;

// Servo signals
    /// The amount of ticks the servo PWM will stay on for it to be off (out of 4096)
    pub const SERVO_SIG_MIN : u16 = 102;
    /// The amount of ticks the servo PWM will stay on for it to be off (out of 4096)
    pub const SERVO_SIG_MAX : u16 = 512;

    /// Minimum Servo angle
    pub const SERVO_ANG_MIN : Gamma = Gamma::ZERO;
    /// Maximum Servo angle
    pub const SERVO_ANG_MAX : Gamma = Gamma(core::f32::consts::PI);

    /// Returns the required amount of ticks for the servo pwm signal for the servo to match the given angle
    pub fn signal_for_angle(angle : Gamma) -> Option<u16> {
        if angle < SERVO_ANG_MIN {
            None    // Angle out of range (smaller)
        } else if angle > SERVO_ANG_MAX {
            None    // Angle out of range (bigger)
        } else {
            Some(
                SERVO_SIG_MAX   // TODO: FIX
                // (((angle - SERVO_ANG_MIN) / (SERVO_ANG_MAX - SERVO_ANG_MIN)).into() * ((SERVO_SIG_MAX - SERVO_SIG_MIN) as f32)) as u16 + SERVO_SIG_MIN
            )
        }
    }
// 

// Configuration
    /// Whether the servo with the given ID should be inverted or not
    pub const SERVO_INV : [bool; 8] = [ false, true, false, true, true, false, true, false ];

    /// Servo position in the "closed" state
    pub const SERVO_STATE_CLOSED : u16 = SERVO_SIG_MAX;
    /// Servo position in the "open" state
    pub const SERVO_STATE_OPEN : u16 = SERVO_SIG_MIN;
    /// Servo position in the "standby" state
    pub const SERVO_STATE_STANDBY : u16 = (SERVO_SIG_MIN + SERVO_SIG_MAX) / 2;
// 

// Errors & Helpers
    /// Helper array for channel ids
    pub const CHANNEL_IDS : [Channel; 8] = [ 
        Channel::C0, Channel::C1, Channel::C2, Channel::C3, 
        Channel::C4, Channel::C5, Channel::C6, Channel::C7
    ];

    pub enum ServoTableError {
        BadId(u8),
        AngleOutOfRange(u8, Gamma)
    }
// 

pub struct ServoTable {
    pub pwm : Pca9685<I2c>,
    pub signals : [u16; 8]
}

impl ServoTable {
    pub fn new(i2c : I2c) -> Result<Self, Box<dyn std::error::Error>> {
        let mut pwm = Pca9685::new(i2c, Address::default())?;

        Ok(Self {
            pwm,
            signals: [0; 8]
        })
    }

    pub fn set_servo_signal(&mut self, id : u8, signal : u16) -> Result<(), ServoTableError> {
        // Check if the servo id given is valid
        if id >= 8 {
            return Err(ServoTableError::BadId(id));
        }

        // Maybe invert signal
        if SERVO_INV[id as usize] {
            signal = SERVO_SIG_MAX - signal;
        }

        self.pwm.set_channel_on_off(CHANNEL_IDS[id as usize], 0, signal).unwrap();   // TODO: Add board error
        self.signals[id as usize] = signal;

        Ok(())
    }

    pub fn set_servo_angle(&mut self, id : u8, mut angle : Gamma) -> Result<(), ServoTableError> {
        // Get the signal for the given angle and write it to the servo
        let signal = signal_for_angle(angle).ok_or(ServoTableError::AngleOutOfRange(id, angle))?;
        
        self.set_servo_signal(id, signal)
    }

    // Servo states
        pub fn set_servo_closed(&mut self, id : u8) -> Result<(), ServoTableError> {
            self.set_servo_signal(id, SERVO_STATE_CLOSED)
        }

        pub fn set_servo_open(&mut self, id : u8) -> Result<(), ServoTableError> {
            self.set_servo_signal(id, SERVO_STATE_OPEN)
        }

        pub fn set_servo_standby(&mut self, id : u8) -> Result<(), ServoTableError> {
            self.set_servo_signal(id, SERVO_STATE_STANDBY)
        }
    // 

    // All servos
        pub fn set_all_closed(&mut self) -> Result<(), ServoTableError> {
            for i in 0 .. 8 {
                self.set_servo_closed(i)?;
            }
            
            Ok(())
        }

        pub fn set_all_open(&mut self) -> Result<(), ServoTableError> {
            for i in 0 .. 8 {
                self.set_servo_open(i)?;
            }
            
            Ok(())
        }

        pub fn set_all_standby(&mut self) -> Result<(), ServoTableError> {
            for i in 0 .. 8 {
                self.set_servo_standby(i)?;
            }
            
            Ok(())
        }
    // 
}

impl Setup for ServoTable { 
    fn setup(&mut self) -> Result<(), syact::Error> {
        self.pwm.enable()?;
        self.pwm.set_prescale(100)?;

        Ok(())
    }
}