# Copyright 2014-present PlatformIO <contact@platformio.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
    This is a dummy file as the nexmon platform for PlatformIO does not rely on any building functions that come with the PlatformIO building toolchain SCons but this file is still needed because PlatformIO won't initialise the project properly without it.
"""
import subprocess
from os.path import join

from SCons.Script import (
    COMMAND_LINE_TARGETS,
    AlwaysBuild,
    Builder,
    Default,
    DefaultEnvironment,
)


env = DefaultEnvironment()
platform = env.PioPlatform()
board = env.BoardConfig()
FRAMEWORK_DIR = platform.get_package_dir("framework-mbed")

HOSTUNAME = (
    subprocess.check_output(["uname", "-s"]).decode(encoding="utf-8").replace("\n", "")
)
PLATFORMUNAME = (
    subprocess.check_output(["uname", "-m"]).decode(encoding="utf-8").replace("\n", "")
)

# Perform checks to set proper Nexmon compiler
if HOSTUNAME in "Linux" and PLATFORMUNAME in "x86_64":
    env.Replace(
        AR="~/.platformio/packages/nexmon/buildtools/gcc-arm-none-eabi-5_4-2016q2-linux-x86/bin/arm-none-eabi-ar",
        AS="~/.platformio/packages/nexmon/buildtools/gcc-arm-none-eabi-5_4-2016q2-linux-x86/bin/arm-none-eabi-as",
        CC="~/.platformio/packages/nexmon/buildtools/gcc-arm-none-eabi-5_4-2016q2-linux-x86/bin/arm-none-eabi-gcc",
        CCFLAGS=[
            "-mcpu=%s" % env.BoardConfig().get("build.cpu"),
        ],
        CXX="~/.platformio/packages/nexmon/buildtools/gcc-arm-none-eabi-5_4-2016q2-linux-x86/bin/arm-none-eabi-cpp",
        OBJCOPY="~/.platformio/packages/nexmon/buildtools/gcc-arm-none-eabi-5_4-2016q2-linux-x86/bin/arm-none-eabi-objcopy",
        RANLIB="~/.platformio/packages/nexmon/buildtools/gcc-arm-none-eabi-5_4-2016q2-linux-x86/bin/arm-none-eabi-ranlib",
        SIZETOOL="~/.platformio/packages/nexmon/buildtools/gcc-arm-none-eabi-5_4-2016q2-linux-x86/bin/arm-none-eabi-size",
        ARFLAGS=["rc"],
        SIZEPROGREGEXP=r"^(?:\.text|\.data|\.rodata|\.text.align|\.ARM.exidx)\s+(\d+).*",
        SIZEDATAREGEXP=r"^(?:\.data|\.bss|\.noinit)\s+(\d+).*",
        SIZECHECKCMD="$SIZETOOL -A -d $SOURCES",
        SIZEPRINTCMD="$SIZETOOL -B -d $SOURCES",
        PROGSUFFIX=".elf",
    )
elif (HOSTUNAME in "Linux" and PLATFORMUNAME in "armv7l") or PLATFORMUNAME in "armv6l":
    env.Replace(
        AR="~/.platformio/packages/nexmon/buildtools/gcc-arm-none-eabi-5_4-2016q2-linux-armv7l/bin/arm-none-eabi-ar",
        AS="~/.platformio/packages/nexmon/buildtools/gcc-arm-none-eabi-5_4-2016q2-linux-armv7l/bin/arm-none-eabi-as",
        CC="~/.platformio/packages/nexmon/buildtools/gcc-arm-none-eabi-5_4-2016q2-linux-armv7l/bin/arm-none-eabi-gcc",
        CCFLAGS=[
            "-mcpu=%s" % env.BoardConfig().get("build.cpu"),
        ],
        CXX="~/.platformio/packages/nexmon/buildtools/gcc-arm-none-eabi-5_4-2016q2-linux-armv7l/bin/arm-none-eabi-cpp",
        OBJCOPY="~/.platformio/packages/nexmon/buildtools/gcc-arm-none-eabi-5_4-2016q2-linux-armv7l/bin/arm-none-eabi-objcopy",
        RANLIB="~/.platformio/packages/nexmon/buildtools/gcc-arm-none-eabi-5_4-2016q2-linux-armv7l/bin/arm-none-eabi-ranlib",
        SIZETOOL="~/.platformio/packages/nexmon/buildtools/gcc-arm-none-eabi-5_4-2016q2-linux-armv7l/bin/arm-none-eabi-size",
        ARFLAGS=["rc"],
        SIZEPROGREGEXP=r"^(?:\.text|\.data|\.rodata|\.text.align|\.ARM.exidx)\s+(\d+).*",
        SIZEDATAREGEXP=r"^(?:\.data|\.bss|\.noinit)\s+(\d+).*",
        SIZECHECKCMD="$SIZETOOL -A -d $SOURCES",
        SIZEPRINTCMD="$SIZETOOL -B -d $SOURCES",
        PROGSUFFIX=".elf",
    )
elif HOSTUNAME in "Darwin":
    env.Replace(
        AR="~/.platformio/packages/nexmon/buildtools/gcc-arm-none-eabi-5_4-2016q2-osx/bin/arm-none-eabi-ar",
        AS="~/.platformio/packages/nexmon/buildtools/gcc-arm-none-eabi-5_4-2016q2-osx/bin/arm-none-eabi-as",
        CC="~/.platformio/packages/nexmon/buildtools/gcc-arm-none-eabi-5_4-2016q2-osx/bin/arm-none-eabi-gcc",
        CCFLAGS=[
            "-mcpu=%s" % env.BoardConfig().get("build.cpu"),
        ],
        CXX="~/.platformio/packages/nexmon/buildtools/gcc-arm-none-eabi-5_4-2016q2-osx/bin/arm-none-eabi-cpp",
        OBJCOPY="~/.platformio/packages/nexmon/buildtools/gcc-arm-none-eabi-5_4-2016q2-osx/bin/arm-none-eabi-objcopy",
        RANLIB="~/.platformio/packages/nexmon/buildtools/gcc-arm-none-eabi-5_4-2016q2-osx/bin/arm-none-eabi-ranlib",
        SIZETOOL="~/.platformio/packages/nexmon/buildtools/gcc-arm-none-eabi-5_4-2016q2-osx/bin/arm-none-eabi-size",
        ARFLAGS=["rc"],
        SIZEPROGREGEXP=r"^(?:\.text|\.data|\.rodata|\.text.align|\.ARM.exidx)\s+(\d+).*",
        SIZEDATAREGEXP=r"^(?:\.data|\.bss|\.noinit)\s+(\d+).*",
        SIZECHECKCMD="$SIZETOOL -A -d $SOURCES",
        SIZEPRINTCMD="$SIZETOOL -B -d $SOURCES",
        PROGSUFFIX=".elf",
    )
else:
    raise NotImplementedError

# Allow user to override via pre:script
if env.get("PROGNAME", "program") == "program":
    env.Replace(PROGNAME="firmware")

env.Append(
    BUILDERS=dict(
        ElfToBin=Builder(
            action=env.VerboseAction(
                " ".join(["$OBJCOPY", "-O", "binary", "$SOURCES", "$TARGET"]),
                "Building $TARGET",
            ),
            suffix=".bin",
        ),
        ElfToHex=Builder(
            action=env.VerboseAction(
                " ".join(
                    ["$OBJCOPY", "-O", "ihex", "-R", ".eeprom", "$SOURCES", "$TARGET"]
                ),
                "Building $TARGET",
            ),
            suffix=".hex",
        ),
    )
)

#
# Target: Build executable and linkable firmware
#

target_elf = None
if "nobuild" in COMMAND_LINE_TARGETS:
    target_elf = join("$BUILD_DIR", "${PROGNAME}.elf")
    target_firm = join("$BUILD_DIR", "${PROGNAME}.bin")
else:
    target_elf = env.BuildProgram()
    target_firm = env.ElfToBin(join("$BUILD_DIR", "${PROGNAME}"), target_elf)

AlwaysBuild(env.Alias("nobuild", target_firm))
target_buildprog = env.Alias("buildprog", target_firm, target_firm)

#
# Target: Print binary size
#
target_elf = join(
    FRAMEWORK_DIR, "patches", "bcm4339", "6_37_34_43", "nexmon", "gen", "patch.elf"
)
target_firm = join(
    FRAMEWORK_DIR, "patches", "bcm4339", "6_37_34_43", "nexmon", "fw_bcmdhd.bin"
)

target_size = env.Alias(
    "size", target_elf, env.VerboseAction("$SIZEPRINTCMD", "Calculating size $SOURCE")
)
AlwaysBuild(target_size)

#
# Information about obsolete method of specifying linker scripts
#

if any("-Wl,-T" in f for f in env.get("LINKFLAGS", [])):
    print(
        "Warning! '-Wl,-T' option for specifying linker scripts is deprecated. "
        "Please use 'board_build.ldscript' option in your 'platformio.ini' file."
    )

#
# Default targets
#

Default([target_buildprog, target_size])
