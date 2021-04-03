from builder.main import FRAMEWORK_DIR
from os.path import join
Import('env', "FRAMEWORK_DIR")

env.Append(
    CCFLAGS=[
        "-std=c99",
        "-Wall",
        "-Wno-unused-result",
        "-O0",
        "-D_BSD_SOURCE",
    ],
    CPPPATH=[
        join(FRAMEWORK_DIR, "buildtools", "ucode_extractor"),
    ],
)

env.BuildProgram(join(FRAMEWORK_DIR, "buildtools", "ucode_extractor"))