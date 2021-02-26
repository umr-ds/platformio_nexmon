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
Nexmon

Nexmon is a C-based firmware patching framework for Broadcom/Cypress WiFi chips 
that enables you to write your own firmware patches, for example, 
to enable monitor mode with radiotap headers and frame injection.

https://github.com/seemoo-lab/nexmon
"""

import sys
from os.path import isfile, isdir, join

from SCons.Script import DefaultEnvironment, SConscript

env = DefaultEnvironment()
platform = env.PioPlatform()
board = env.BoardConfig()

FRAMEWORK_DIR = platform.get_package_dir("framework-mbed") # Spoofing Nexmon as mbed currently to skip having to publish it as a package
assert isdir(FRAMEWORK_DIR)

mcu = env.BoardConfig().get("build.mcu", "") # not yet needed but nice to have for when multiple boards are implemented

env.Replace(
    AR="arm-none-eabi-ar",
    AS="arm-none-eabi-as",
    CC="arm-none-eabi-gcc",                  # Currently using toolchain-gccarmnoneeabi as host for nexmon specific compiler
    CXX="arm-none-eabi-cpp",
    OBJCOPY="arm-none-eabi-objcopy",
    RANLIB="arm-none-eabi-ranlib",
    SIZETOOL="arm-none-eabi-size",
)

env.Append(
    ASFLAGS=["-x"],
    CFLAGS=["-std=gnu11"],
    CCFLAGS=[
        "-Os",  # optimize for size
        "-mcpu=%s" % env.BoardConfig().get("build.cpu"),
    ],
    CPPPATH=[
        join(FRAMEWORK_DIR, "buildtools", "b43", "assembler"),
        join(FRAMEWORK_DIR, "buildtools", "b43", "disassembler"),
        join(FRAMEWORK_DIR, "buildtools", "b43", "fwcutter"),
        join(FRAMEWORK_DIR, "buildtools", "b43", "ssb_sprom"),
        join(FRAMEWORK_DIR, "buildtools", "b43", "debug", "include"), 
        join(FRAMEWORK_DIR, "buildtools", "b43-v2", "assembler"),
        join(FRAMEWORK_DIR, "buildtools", "b43-v2", "disassembler"),
        join(FRAMEWORK_DIR, "buildtools", "b43-v2", "debug", "include"), 
        join(FRAMEWORK_DIR, "buildtools", "b43-v3", "assembler"),
        join(FRAMEWORK_DIR, "buildtools", "b43-v3", "disassembler"),
        join(FRAMEWORK_DIR, "buildtools", "b43-v3", "fwcutter"),
        join(FRAMEWORK_DIR, "buildtools", "b43-v3", "ssb_sprom"),
        join(FRAMEWORK_DIR, "buildtools", "b43-v3", "debug", "include"), 
        join(FRAMEWORK_DIR, "buildtools", "flash_patch_extractor"),
        join(FRAMEWORK_DIR, "buildtools", "flash_patch_extractor", "darm"),
        join(FRAMEWORK_DIR, "buildtools", "gcc-arm-none-eabi-5_4-2016q2-linux-armv7l", "arm-none-eabi", "include"),
        join(FRAMEWORK_DIR, "buildtools", "gcc-arm-none-eabi-5_4-2016q2-linux-armv7l", "arm-none-eabi", "include", "machine"),
        join(FRAMEWORK_DIR, "buildtools", "gcc-arm-none-eabi-5_4-2016q2-linux-armv7l", "arm-none-eabi", "include", "sys"),
        join(FRAMEWORK_DIR, "buildtools", "gcc-arm-none-eabi-5_4-2016q2-linux-armv7l", "lib", "gcc", "arm-none-eabi", "5.4.1", "include"),
        join(FRAMEWORK_DIR, "buildtools", "gcc-arm-none-eabi-5_4-2016q2-linux-armv7l", "lib", "gcc", "arm-none-eabi", "5.4.1", "include-fixed"),
        join(FRAMEWORK_DIR, "buildtools", "gcc-arm-none-eabi-5_4-2016q2-linux-armv7l", "lib", "gcc", "arm-none-eabi", "5.4.1", "install-tools"),
        join(FRAMEWORK_DIR, "buildtools", "gcc-arm-none-eabi-5_4-2016q2-linux-armv7l", "lib", "gcc", "arm-none-eabi", "5.4.1", "install-tools", "include"),
        join(FRAMEWORK_DIR, "buildtools", "gcc-arm-none-eabi-5_4-2016q2-linux-armv7l", "lib", "gcc", "arm-none-eabi", "5.4.1", "plugin", "include"),
        join(FRAMEWORK_DIR, "buildtools", "gcc-arm-none-eabi-5_4-2016q2-linux-armv7l", "lib", "gcc", "arm-none-eabi", "5.4.1", "plugin", "include", "c-family"),
        join(FRAMEWORK_DIR, "buildtools", "gcc-arm-none-eabi-5_4-2016q2-linux-armv7l", "lib", "gcc", "arm-none-eabi", "5.4.1", "plugin", "include", "config"),
        join(FRAMEWORK_DIR, "buildtools", "gcc-arm-none-eabi-5_4-2016q2-linux-armv7l", "lib", "gcc", "arm-none-eabi", "5.4.1", "plugin", "include", "config", "arm"),
        join(FRAMEWORK_DIR, "buildtools", "gcc-nexmon-plugin"),
        join(FRAMEWORK_DIR, "buildtools", "isl-0.10"),
        join(FRAMEWORK_DIR, "buildtools", "isl-0.10", "include", "isl"),
        join(FRAMEWORK_DIR, "buildtools", "isl-0.10", "interface"),
        join(FRAMEWORK_DIR, "buildtools", "mpfr-3.1.4", "src"),
        join(FRAMEWORK_DIR, "buildtools", "mpfr-3.1.4", "src", "arm"),
        join(FRAMEWORK_DIR, "buildtools", "mpfr-3.1.4", "tune"),
        join(FRAMEWORK_DIR, "buildtools", "mpfr-3.1.4", "tests"),
        join(FRAMEWORK_DIR, "buildtools", "ucode_extractor"),
        join(FRAMEWORK_DIR, "firmwares", "bcm43430a1"),
        join(FRAMEWORK_DIR, "firmwares", "bcm43430a1", "7_45_41_46"),
        join(FRAMEWORK_DIR, "patches", "include"),
        join(FRAMEWORK_DIR, "patches", "common"),
        join(FRAMEWORK_DIR, "patches", "bcm43430a1", "7_45_41_46", "nexmon", "include"),
        join(FRAMEWORK_DIR, "patches", "bcm43430a1", "7_45_41_46", "nexmon", "src"),
        join(FRAMEWORK_DIR, "patches", "bcm43430a1", "7_45_41_46", "nexmon", "brcmfmac_4.14.y-nexmon"),
        join(FRAMEWORK_DIR, "patches", "bcm43430a1", "7_45_41_46", "nexmon", "brcmfmac_4.14.y-nexmon", "include"),
        #join(FRAMEWORK_DIR, "patches", "bcm43430a1", "7_45_41_46", "nexmon", "brcmfmac_kernel44"),
        #join(FRAMEWORK_DIR, "patches", "bcm43430a1", "7_45_41_46", "nexmon", "brcmfmac_kernel44", "include"),   For now only include patches for target kernel 4.14
        #join(FRAMEWORK_DIR, "patches", "bcm43430a1", "7_45_41_46", "nexmon", "brcmfmac_kernel49"),
        #join(FRAMEWORK_DIR, "patches", "bcm43430a1", "7_45_41_46", "nexmon", "brcmfmac_kernel49", "include"),
        join(FRAMEWORK_DIR, "utilities", "nexutil"),
    ],
    LINKFLAGS=[
        "-Os",
        "-mthumb",
        "-mcpu=%s" % env.BoardConfig().get("build.cpu"),
        "--specs=nano.specs",
        "-Wl,--gc-sections,--relax",
        "-Wl,--check-sections",
        "-Wl,--entry=Reset_Handler",
        "-Wl,--unresolved-symbols=report-all",
        "-Wl,--warn-common",
        "-Wl,--defsym=LD_MAX_SIZE=%d" % board.get("upload.maximum_size"),
        "-Wl,--defsym=LD_MAX_DATA_SIZE=%d" % board.get("upload.maximum_ram_size"),
    ],
)
print("Test")