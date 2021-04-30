from os.path import join
Import('env', "FRAMEWORK_DIR")

print("Compiling b43-v3 fwcutter...")

env.Append(
    CPPPATH=[
        join(FRAMEWORK_DIR, "buildtools", "b43-v3", "fwcutter"),
    ],
)

rc = subprocess.Popen(["make", "-s"], cwd=os.path.join(FRAMEWORK_DIR, "buildtools", "b43", "assembler"))