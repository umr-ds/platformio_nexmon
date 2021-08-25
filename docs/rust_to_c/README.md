# Steps to take to write rust code and use it from C
1. Pre-requisites:
   1. `cargo` and the `rust toolchain` have to be installed
   2. `gcc` has to be installed
   3. `cbindgen` has to be installed for automatic generation of C header files from Rust code: `cargo install cbindgen`
2. Create a new rust library with `cargo new --lib <your_library_name>`
3. Open the `cargo.toml` of the newly created library
   1. Add this  
    ```toml
    [lib]
    crate-type = ["cdylib"] // for dynamic lib
    or
    crate-type = ["staticlib"] // for static lib
    ```
4. Open `lib.rs` and write a rust function that you want to run from C e.g  
```rust
#[no_mangle] // This has to be declared above all functions you want to call from C, because the Rust compiler will otherwise mangle your definitions in a way C can't handle
pub extern "C" fn rust_function(){
    print!("Hello, world!\n");
}
```
5. Build your project `cargo build`
6. The generated library can be found under `<your_project_name>/target/debug/<your_project_name.so>` for a dynamic or `<your_project_name>/target/debug/<your_project_name.a>` for a static lib
7. Generate the header file(s): `cbindgen --lang c --output <header_file_name.h>`
8. Include the definitions from the header file in your C code `#include "<header_file_name.h>"`
9. Call/use the imported Rust functions in your code
10. Compile your C project with gcc by explicitly stating the library: `gcc -o test test.c /path/to/your/rustlib_to_c.so` or `gcc -o test test.c /path/to/your/rustlib_to_c.a`
11. *Debug:*
    1.  If compiling fails for a static library try this command:  
        `gcc -o test test.c ./target/debug/librust_to_c.a -pthread -Wl,--no-as-needed -ldl`