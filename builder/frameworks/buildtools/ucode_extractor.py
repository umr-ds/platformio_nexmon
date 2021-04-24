from os.path import join
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
        join(FRAMEWORK_DIR, "buildtools", "ucode_extractor"),
        join(FRAMEWORK_DIR, "utilities", "libargp")
    ],
)

env.BuildSources(join("$BUILD_DIR", "Framework-Nexmon", "ucode_extractor"), join(FRAMEWORK_DIR, "buildtools", "ucode_extractor"))