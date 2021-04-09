from os.path import join
Import('env', "FRAMEWORK_DIR")

env.Append(
    CPPPATH=[
        join(FRAMEWORK_DIR, "buildtools", "b43-v2", "assembler"),
        join(FRAMEWORK_DIR, "buildtools", "b43-v2", "disassembler"),
    ],
)