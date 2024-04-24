use syact::device::led::LED;
use syact::device::pin::{InputPin, UniInPin};
use syact::Setup;

pub struct UserTerminal {
    switch_start : UniInPin,
    led_start : LED,

    switch_halt : UniInPin,
    led_halt : LED,
}

impl UserTerminal {
    pub fn new(switch_start_pin : u8, led_start_pin : u8, switch_halt_pin : u8, led_halt_pin : u8) -> Self {
        Self {
            switch_start: UniInPin::new(switch_start_pin),
            led_start: LED::new(led_start_pin),
            
            switch_halt: UniInPin::new(switch_halt_pin),
            led_halt: LED::new(led_halt_pin)
        }
    }

    // Buttons
        pub fn check_start(&self) -> bool {
            self.switch_start.is_high().unwrap() // TODO: Remove unwrap
        }

        pub fn check_halt(&self) -> bool {
            // Halt button signal is inversed for safety reasons
            self.switch_halt.is_low().unwrap() // TODO: Remove unwrap
        }
    // 

    // LEDS
        pub fn is_start_led_on(&self) -> bool {
            self.led_start.is_on()
        }

        pub fn set_start_led(&mut self, value : bool) {
            self.led_start.set(value);
        }

        pub fn is_halt_led_on(&self) -> bool {
            self.led_halt.is_on()
        }

        pub fn set_halt_led(&mut self, value : bool) {
            self.led_halt.set(value);
        }
    // 
}

impl Setup for UserTerminal {
    fn setup(&mut self) -> Result<(), syact::Error> {
        self.switch_start.setup()?;
        self.led_start.setup()?;

        self.switch_halt.setup()?;
        self.led_halt.setup()?;

        Ok(())
    }
}