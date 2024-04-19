use pwm_pca9685::{Address, Channel, Pca9685};
use rppal::i2c::I2c;

const 

pub struct Table {
    pub pwm : Pca9685<I2c>
}

impl Table {
    pub fn new(i2c : I2c) -> Result<Self, Box<std::error::Error>> {
        let mut pwm = Pca9685::new(i2c, Address::default())?;

        pwm.set_prescale(100)?;
        pwm.enable()?;

        Ok(Self {
            pwm
        })
    }


    
    pub fn signal_for_angle(&mut self) {
        
    }

    pub fn set_servo_angle(&m)
}