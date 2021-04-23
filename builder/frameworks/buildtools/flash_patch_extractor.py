from os.path import join
Import('env', "FRAMEWORK_DIR")

print("Configuring flash patch extractor...")

env.Append(
    CPPPATH=[
        join(FRAMEWORK_DIR, "buildtools", "flash_path_extractor"),
        join(FRAMEWORK_DIR, "buildtools", "flash_path_extractor", "darm"),
    ],
)