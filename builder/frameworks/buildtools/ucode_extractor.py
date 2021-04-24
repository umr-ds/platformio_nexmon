import os.path
Import('env', "FRAMEWORK_DIR")

print("Compiling ucode extractor...")

env.Append(
    CFLAGS=[
        "-std=c99",
        "-Wall",
        "-Wno-unused-result",
        "-O0",
        "-D_BSD_SOURCE",
    ],
    CPPPATH=[
        os.path.join(FRAMEWORK_DIR, "buildtools", "ucode_extractor"),
    ],
)

env.BuildSources(os.path.join("$BUILD_DIR", "Framework-Nexmon", "ucode_extractor"), os.path.join(FRAMEWORK_DIR, "buildtools", "ucode_extractor"))