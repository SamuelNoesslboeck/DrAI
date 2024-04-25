use std::fs::File;

#[rocket::get("/")]
fn index() -> std::io::Result<File> {
    return File::open("www/index.html")
}

#[rocket::launch]
fn rocket() -> _ {
    rocket::build()
        .mount("/", rocket::routes![index])
        
}
