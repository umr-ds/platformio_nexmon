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

from os.path import dirname, isfile, isdir, join
from subprocess import check_output
from SCons.Script import DefaultEnvironment, SConscript, Export
import glob

env = DefaultEnvironment()
platform = env.PioPlatform()
board = env.BoardConfig()

# Spoofing Nexmon as mbed currently to skip having to publish it as a package
FRAMEWORK_DIR = platform.get_package_dir("framework-mbed")
PACKAGE_DIR = dirname(FRAMEWORK_DIR)
assert isdir(FRAMEWORK_DIR)
assert isdir(PACKAGE_DIR)

# not yet needed but nice to have for when multiple boards are implemented
mcu = env.BoardConfig().get("build.mcu", "")

# Add environment variables for the nexmon build process
HOSTUNAME = check_output(["uname", "-s"]).decode(encoding="utf-8").replace("\n", "")
PLATFORMUNAME = check_output(["uname", "-m"]).decode(encoding="utf-8").replace("\n", "")

env.Append(
    ARCH="arm",
    SUBARCH="arm",
    KERNEL="kernel7",
    HOSTUNAME=HOSTUNAME,
    PLATFORMUNAME=PLATFORMUNAME,
    NEXMON_ROOT=FRAMEWORK_DIR,
    Q="@",
    NEXMON_SETUP_ENV="1"
)

if HOSTUNAME in "Darwin":
    cc_path = join(PACKAGE_DIR, "toolchain-gccarmnoneeabi", "gcc-arm-none-eabi-5_4-2016q2-osx", "bin")
    assert isdir(cc_path)

    cc_list = glob.glob(pathname=join(cc_path, "arm-none-eabi-*"))
    cc_list.sort()

    raise NotImplementedError

elif HOSTUNAME in "Linux" and PLATFORMUNAME in "x86_64":
    cc_path = join(PACKAGE_DIR, "toolchain-gccarmnoneeabi", "gcc-arm-none-eabi-5_4-2016q2-linux-x86", "bin")
    assert isdir(cc_path)

    cc_list = glob.glob(pathname=join(cc_path, "arm-none-eabi-*"))
    cc_list.sort()

    env.Replace(
        ADDR2LINE=cc_list[0],
        AR=cc_list[1],
        AS=cc_list[2],
        CYY=cc_list[3],
        FILT=cc_list[4],
        CPP=cc_list[5],
        ELFEDIT=cc_list[6],
        CXX=cc_list[7],
        CC=cc_list[8],
        CCPLUGIN=join(PACKAGE_DIR, "toolchain-gccarmnoneeabi", "gcc-nexmon-plugin", "nexmon.so"),
        GCC=cc_list[9],
        GCCAR=cc_list[10],
        GCCNM=cc_list[11],
        GCCRANLIB=cc_list[12],
        GCOV=cc_list[13],
        GCOVTOOL=cc_list[14],
        GDB=cc_list[15],
        GDBPY=cc_list[16],
        GPROF=cc_list[17],
        LD=cc_list[18],
        LDBFD=cc_list[19],
        NM=cc_list[20],
        OBJCOPY=cc_list[21],
        OBJDUMP=cc_list[22],
        RANLIB=cc_list[23],
        READELF=cc_list[24],
        SIZETOOL=cc_list[25],
        STRINGS=cc_list[26],
        STRIP=cc_list[27],
    )

elif (HOSTUNAME in "Linux" and PLATFORMUNAME in "armv7l") or PLATFORMUNAME in "armv6l":
    cc_path = join(PACKAGE_DIR, "toolchain-gccarmnoneeabi", "gcc-arm-none-eabi-5_4-2016q2-linux-armv7l", "bin")
    assert isdir(cc_path)

    cc_list = glob.glob(pathname=join(cc_path, "arm-none-eabi-*"))
    cc_list.sort()
    print(cc_list)

    raise NotImplementedError
else:
    raise NotImplementedError

env.Append(
    CCFLAGS=[
        "-mcpu=%s" % env.BoardConfig().get("build.cpu"),
    ],
)

Export('env', "FRAMEWORK_DIR")

SConscript('b43.py')
SConscript('b43-v2.py')
SConscript('b43-v3.py')
SConscript('flash_patch_extractor.py')
SConscript('ucode_extractor.py')