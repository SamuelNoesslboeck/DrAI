use clap::{command, arg, value_parser};

use drake::table::*;

fn main() {
        // Init logging
        env_logger::init();
    // 

    // Cmd
        let matches = command!() 
            .about("Table testing program for the drake robot")
            .arg(arg!([state] "Pin number of the step pin").value_parser(value_parser!(String)))
            .arg(arg!([z_state] "The current state of the Z-Axis (Drawing 0, Lifted 1)").value_parser(value_parser!(usize)))
            .get_matches();

        let path : String = matches.get_one::<String>("path").expect("A valid path has to be provided").clone();
        let z_state : usize = *matches.get_one("z_state").expect("A valid Z-State has to be provided");
    // 
}