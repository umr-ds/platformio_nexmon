# Steps to take to write C code and use it from rust
1. Pre-requisites:
   1. `cargo` and the `rust toolchain` have to be installed
   2. `gcc` has to be installed
   3. `bindgen` for automatic generation of the C FFI for our Rust code
2. Create a new rust library with `cargo new --lib <your_library_name>`
3. Open the `cargo.toml` of the newly created library
   1. Add this  
    ```toml
    [build-dependencies]
    bindgen = "0.59.1"
    ```
4. Create a `wrapper.h` file that includes all headers containing declarations of structs and functions you want bindings for
5. Create a `build.rs` file at the root of your rust crate, with the following content:  
    ```rust
    extern crate bindgen;

    use std::env;
    use std::path::PathBuf;

    fn main() {
        // Tell cargo to tell rustc to link the system bzip2
        // shared library.
        println!("cargo:rustc-link-lib=bz2");   <--- Replace the library you want to link to here

        // Tell cargo to invalidate the built crate whenever the wrapper changes
        println!("cargo:rerun-if-changed=wrapper.h");

        // The bindgen::Builder is the main entry point
        // to bindgen, and lets you build up options for
        // the resulting bindings.
        let bindings = bindgen::Builder::default()
            // The input header we would like to generate
            // bindings for.
            .header("wrapper.h")
            // Tell cargo to invalidate the built crate whenever any of the
            // included header files changed.
            .parse_callbacks(Box::new(bindgen::CargoCallbacks))
            // Finish the builder and generate the bindings.
            .generate()
            // Unwrap the Result and panic on failure.
            .expect("Unable to generate bindings");

        // Write the bindings to the $OUT_DIR/bindings.rs file.
        let out_path = PathBuf::from(env::var("OUT_DIR").unwrap());
        bindings
            .write_to_file(out_path.join("bindings.rs"))
            .expect("Couldn't write bindings!");
    }
    ```
6. Build your project `cargo build`
7. The generated `bindings.rs` for your project can be found under something like `/target/debug/build/<your_project_name_afc7747d7eafd720>/out/`
8. To use the bindings go to the crate's main entry point `src/lib.rs` and add this:  
    ```rust
    #![allow(non_upper_case_globals)]
    #![allow(non_camel_case_types)]
    #![allow(non_snake_case)]

    include!(concat!(env!("OUT_DIR"), "/bindings.rs"));
    ```