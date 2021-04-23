from os.path import join
Import('env', "FRAMEWORK_DIR")

print("Configuring b43 fwcutter...")

env.Append(
    CPPPATH=[
        join(FRAMEWORK_DIR, "buildtools", "b43", "fwcutter"),
    ],
)