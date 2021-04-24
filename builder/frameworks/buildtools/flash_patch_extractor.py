import os.path
Import('env', "FRAMEWORK_DIR")

print("Compiling flash patch extractor...")

env.Append(
    CPPPATH=[
        os.path.join(FRAMEWORK_DIR, "buildtools", "flash_path_extractor"),
        os.path.join(FRAMEWORK_DIR, "buildtools", "flash_path_extractor", "darm"),
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

env.BuildSources(os.path.join("$BUILD_DIR", "Framework-Nexmon", "flash_patch_extractor", "darm"), os.path.join(FRAMEWORK_DIR, "buildtools", "flash_path_extractor", "darm"))
env.BuildSources(os.path.join("$BUILD_DIR", "Framework-Nexmon", "flash_patch_extractor"), os.path.join(FRAMEWORK_DIR, "buildtools", "flash_path_extractor"))