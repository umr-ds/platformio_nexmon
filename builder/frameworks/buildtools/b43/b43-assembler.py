from os.path import join
Import('env', "FRAMEWORK_DIR")

env.Append(
    CPPPATH=[
        join(FRAMEWORK_DIR, "buildtools", "b43", "assembler"),
        join(FRAMEWORK_DIR, "buildtools", "b43", "disassembler"),
        join(FRAMEWORK_DIR, "buildtools", "b43", "fwcutter"),
        join(FRAMEWORK_DIR, "buildtools", "b43", "ssb_sprom"),
    ],
)

