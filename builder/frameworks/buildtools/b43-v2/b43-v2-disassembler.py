from os.path import join
Import('env', "FRAMEWORK_DIR")

print("Compiling b43-v2 disassembler...")

env.Append(
    CPPPATH=[
        join(FRAMEWORK_DIR, "buildtools", "b43-v2", "assembler"),
        join(FRAMEWORK_DIR, "buildtools", "b43-v2", "disassembler"),
    ],
)

rc = subprocess.Popen(["make", "-s"], cwd=os.path.join(FRAMEWORK_DIR, "buildtools", "b43", "assembler"))