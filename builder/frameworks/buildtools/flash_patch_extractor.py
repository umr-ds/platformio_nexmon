from os.path import join
Import('env', "FRAMEWORK_DIR")

print("Compiling flash patch extractor...")

env.Append(
    CPPPATH=[
        join(FRAMEWORK_DIR, "buildtools", "flash_path_extractor"),
        join(FRAMEWORK_DIR, "buildtools", "flash_path_extractor", "darm"),
    ],
)

env.Replace(
    CCFLAGS=[
        "-rdynamic",
        "-std=c99",
        "-Wall",
        "-O2",
        "-Wextra",
        "-Wno-missing-field-initializers"
    ]
)

env.BuildSources(join("$BUILD_DIR", "Framework-Nexmon", "flash_patch_extractor", "darm"), join(FRAMEWORK_DIR, "buildtools", "flash_path_extractor", "darm"))
env.BuildSources(join("$BUILD_DIR", "Framework-Nexmon", "flash_patch_extractor"), join(FRAMEWORK_DIR, "buildtools", "flash_path_extractor"))