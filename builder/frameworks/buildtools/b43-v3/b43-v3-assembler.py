from os.path import join
Import('env', "FRAMEWORK_DIR")

env.Append(
    CPPPATH=[
        join(FRAMEWORK_DIR, "buildtools", "b43-v3", "assembler"),
        join(FRAMEWORK_DIR, "buildtools", "b43-v3", "disassembler"),
        join(FRAMEWORK_DIR, "buildtools", "b43-v3", "fwcutter"),
        join(FRAMEWORK_DIR, "buildtools", "b43-v3", "ssb_sprom"),
    ],
)