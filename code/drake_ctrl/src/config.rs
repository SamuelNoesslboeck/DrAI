use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize)]
pub struct DrakeConfig {
    pub home : [Phi; 3]
}