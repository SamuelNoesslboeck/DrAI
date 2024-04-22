use clap::{command, arg, value_parser};

use drake::servo_table::*;

fn main() {
        // Init logging
        env_logger::init();
    // 

    // Cmd
        let matches = command!() 
            .about("Table testing program for the drake robot")
            .arg(arg!([state] "The state to put the table in (open/standby/closed)").value_parser(value_parser!(String)))
            .get_matches();

        let state_opt = matches.get_one::<String>("state");
    // 
}