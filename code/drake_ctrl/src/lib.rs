use rppal::i2c::I2c;
use syact::act::StateActuator;
use syact::prelude::*;
use sybot::prelude::*;

use syact::meas::take_simple_meas;
use sybot::robs::stepper::{LinearXYStepperRobot, LinearXYStepperActuators};

use crate::servo_table::ServoTable;
use crate::user_terminal::UserTerminal;

// Submodules
    pub mod config;

    pub mod robot;

    pub mod routines;

    pub mod servo_table;

    pub mod user_terminal;
// 

// Constants & Statics
    lazy_static::lazy_static! {
        // Pins
            // Stepper
                pub static ref DRAI_X_AXIS_STEP_PIN : u8 = env!("DRAI_X_AXIS_STEP_PIN").parse::<u8>().unwrap();
                pub static ref DRAI_Y_AXIS_STEP_PIN : u8 = env!("DRAI_Y_AXIS_STEP_PIN").parse::<u8>().unwrap();
                pub static ref DRAI_Z_AXIS_STEP_PIN : u8 = env!("DRAI_Z_AXIS_STEP_PIN").parse::<u8>().unwrap();

                pub static ref DRAI_X_AXIS_DIR_PIN : u8 = env!("DRAI_X_AXIS_DIR_PIN").parse::<u8>().unwrap();
                pub static ref DRAI_Y_AXIS_DIR_PIN : u8 = env!("DRAI_Y_AXIS_DIR_PIN").parse::<u8>().unwrap(); 
                pub static ref DRAI_Z_AXIS_DIR_PIN : u8 = env!("DRAI_Z_AXIS_DIR_PIN").parse::<u8>().unwrap();

                pub static ref DRAI_X_SWITCH_POS_PIN : u8 = env!("DRAI_X_SWITCH_POS_PIN").parse::<u8>().unwrap();
                pub static ref DRAI_Y_SWITCH_POS_PIN : u8 = env!("DRAI_Y_SWITCH_POS_PIN").parse::<u8>().unwrap();
                // pub static ref DRAI_Z_SWITCH_POS_PIN : u8 = env!("DRAI_Z_SWITCH_POS_PIN").parse::<u8>().unwrap();

                pub static ref DRAI_X_SWITCH_NEG_PIN : u8 = env!("DRAI_X_SWITCH_NEG_PIN").parse::<u8>().unwrap();
                // pub static ref DRAI_Y_SWITCH_NEG_PIN : u8 = env!("DRAI_Y_SWITCH_NEG_PIN").parse::<u8>().unwrap();
                pub static ref DRAI_Z_SWITCH_NEG_PIN : u8 = env!("DRAI_Z_SWITCH_NEG_PIN").parse::<u8>().unwrap();
            //

            // User-Terminal
                pub static ref DRAI_UT_SWITCH_START_PIN : u8 = env!("DRAI_UT_SWITCH_START_PIN").parse::<u8>().unwrap();
                pub static ref DRAI_UT_LED_START_PIN : u8 = env!("DRAI_UT_LED_START_PIN").parse::<u8>().unwrap();

                pub static ref DRAI_UT_SWITCH_HALT_PIN : u8 = env!("DRAI_UT_SWITCH_HALT_PI").parse::<u8>().unwrap();
                pub static ref DRAI_UT_LED_HALT_PIN : u8 = env!("DRAI_UT_LED_HALT_PIN").parse::<u8>().unwrap();
            //
        //

        // Static-Config
            pub static ref DRAI_X_MICROSTEPS : u8 = env!("DRAI_X_MICROSTEPS").parse::<u8>().unwrap();
            pub static ref DRAI_Y_MICROSTEPS : u8 = env!("DRAI_Y_MICROSTEPS").parse::<u8>().unwrap();
            pub static ref DRAI_Z_MICROSTEPS : u8 = env!("DRAI_Z_MICROSTEPS").parse::<u8>().unwrap();
        // 
    }

    pub const OFFSET_X : Delta = Delta(-50.0);
    pub const OFFSET_Y : Delta = Delta(-50.0);

    pub const RATIO_X : f32 = 6.0;
    pub const RATIO_Y : f32 = 6.0;
    pub const RATIO_Z : f32 = 8.0 / core::f32::consts::PI / 2.0;

    pub const MEAS_DATA_X : SimpleMeasData = SimpleMeasData {
        set_gamma: Gamma(325.0),
        max_dist: Delta(400.0),
        meas_speed: unsafe { SpeedFactor::from_unchecked(0.4) },

        add_samples: 0,
        sample_dist: Some(Delta(20.0))
    };

    pub const MEAS_DATA_Y : SimpleMeasData = SimpleMeasData {
        set_gamma: Gamma(230.0),
        max_dist: Delta(800.0),
        meas_speed: unsafe { SpeedFactor::from_unchecked(0.4) },

        add_samples: 0,
        sample_dist: Some(Delta(20.0))
    };

    // pub const LIMITS_MIN : [Gamma; 2] = [

    // ]; 

    // Positions
    pub const HOME : [Phi; 2] = [
        Phi(125.0),
        Phi(75.0)
    ];

    pub const STATES_Z : [Gamma; 2] = [
        Gamma::ZERO,
        Gamma(5.0)
    ]; 

    pub const STATE_Z_DRAW : usize = 0;
    pub const STATE_Z_LIFT : usize = 1;

    // Load data    
    pub const WEIGHT_AXES : [Inertia; 2] = [
        Inertia(0.5),
        Inertia(1.0)
    ];
    pub const WEIGHT_BED : Inertia = Inertia(2.0);  // 2kgs
//

// Robots
    pub type DrakeRobot = LinearXYStepperRobot;

    pub fn drake_robot_new() -> DrakeRobot {
        LinearXYStepperRobot::new([
            AngleConfig {
                offset: OFFSET_X,
                counter: false
            },
            AngleConfig {
                offset: OFFSET_Y,
                counter: false
            }
        ], LinearXYStepperActuators {
            x: LinearAxis::new(
                Stepper::new(GenericPWM::new(DRAI_X_AXIS_STEP_PIN, DRAI_X_AXIS_DIR_PIN).unwrap(), StepperConst::MOT_17HE15_1504S)
                    .add_interruptor_inline(Box::new(
                        EndSwitch::new(false, Some(Direction::CW), UniInPin::new(DRAI_X_SWITCH_POS_PIN))
                            .setup_inline().unwrap()
                    ))
                , RATIO_X
            ),
            y: LinearAxis::new(
                Stepper::new(GenericPWM::new(DRAI_Y_AXIS_STEP_PIN, DRAI_Y_AXIS_DIR_PIN).unwrap(), StepperConst::MOT_17HE15_1504S)
                    .add_interruptor_inline(Box::new(
                        EndSwitch::new(false, Some(Direction::CW), UniInPin::new(DRAI_Y_SWITCH_POS_PIN))
                            .setup_inline().unwrap()
                    ))
                , RATIO_Y
            )
        }, Vec::new())
    }
// 

// Station
    pub struct DrakeStation { 
        pub z_axis : StateActuator<LinearAxis<Stepper>, 2>,
        
        pub servo_table : ServoTable,
        pub user_terminal : UserTerminal
    }

    impl DrakeStation {
        pub fn new(i2c : I2c) -> Self {
            Self {
                z_axis: StateActuator::new(
                    LinearAxis::new(
                        Stepper::new(
                            GenericPWM::new(DRAI_Z_AXIS_STEP_PIN, DRAI_Z_AXIS_DIR_PIN).unwrap(),
                            StepperConst::MOT_17HE15_1504S
                        ),
                        RATIO_Z
                    ),
                    STATES_Z
                ),
                servo_table: ServoTable::new(i2c).unwrap(), // TODO: Find solution without unwrap
                user_terminal: UserTerminal::new(
                    DRAI_UT_SWITCH_START_PIN,
                    DRAI_UT_LED_START_PIN,
                    DRAI_UT_SWITCH_HALT_PIN,
                    DRAI_UT_LED_HALT_PIN
                )
            }
        }

        pub fn lift_pen(&mut self) -> Result<(), sybot::Error> {
            self.z_axis.drive_to_state(STATE_Z_LIFT, SpeedFactor::MAX)
        }

        pub fn put_down_pen(&mut self) -> Result<(), sybot::Error> {
            self.z_axis.drive_to_state(STATE_Z_DRAW, SpeedFactor::MAX)
        }

        pub fn reposition_pen(&mut self, rob : &mut LinearXYStepperRobot, new_pos : [Phi; 2]) -> Result<(), sybot::Error> {
            self.lift_pen()?;
            rob.move_abs_j(new_pos, SpeedFactor::MAX)?;
            self.put_down_pen()
        }
    }

    impl Setup for DrakeStation {
        fn setup(&mut self) -> Result<(), syact::Error> {
            self.z_axis.setup()?;
            self.servo_table.setup()?;
            self.user_terminal.setup()?;

            // Set mircosteps
                self.z_axis.set_microsteps(MicroSteps::from(DRAI_Z_MICROSTEPS));
            // 
            
            Ok(())
        }
    }

    impl Station<LinearXYStepperActuators, dyn StepperActuator, 2> for DrakeStation {
        type Robot = LinearXYStepperRobot;

        fn home(&mut self, rob : &mut Self::Robot) -> Result<(), sybot::Error> {
            self.lift_pen()?;

            dbg!(take_simple_meas(&mut rob.comps_mut().x, &MEAS_DATA_X, SpeedFactor::MAX)?);
            dbg!(take_simple_meas(&mut rob.comps_mut().y, &MEAS_DATA_Y, SpeedFactor::MAX)?);

            dbg!(rob.move_abs_j_sync(HOME, SpeedFactor::from(0.25))?);     // Changed speed factor: FIX #1

            Ok(())
        }
    }
// 