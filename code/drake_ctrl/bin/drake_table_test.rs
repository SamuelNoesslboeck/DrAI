use clap::{command, arg, value_parser};

use drake::servo_table::ServoTable;
use syact::Setup;

fn main() {
        // Init logging
        env_logger::init();
    // 

    // Cmd
        let matches = command!() 
            .about("Table testing program for the drake robot")
            .arg(arg!([state] "The state to set the table to (open/closed/standby), the program will not be halted if a state is given").value_parser(value_parser!(String)))
            .get_matches();

        let state_opt : Option<&String> = matches.get_one::<String>("state");
    // 

    let mut table = ServoTable::new(
        rppal::i2c::I2c::new().unwrap()
    ).unwrap();

    table.setup().unwrap();

    if let Some(state_ref) = state_opt {
        let state = state_ref.clone();
        
        if state == "open" {
            table.set_all_open().unwrap();
        } else if state == "closed" {
            table.set_all_closed().unwrap();
        } else if state == "standby" {
            table.set_all_standby().unwrap();
        } else {
            println!("Invalid state given!");
        }
    }
}