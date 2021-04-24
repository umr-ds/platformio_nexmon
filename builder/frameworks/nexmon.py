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

import os.path
import os
import subprocess
from SCons.Script import DefaultEnvironment, SConscript, Export
import glob

env = DefaultEnvironment()
platform = env.PioPlatform()
board = env.BoardConfig()

# Spoofing Nexmon as mbed currently to skip having to publish it as a package
FRAMEWORK_DIR = platform.get_package_dir("framework-mbed")
PACKAGE_DIR = os.path.dirname(FRAMEWORK_DIR)
assert os.path.isdir(FRAMEWORK_DIR)
assert os.path.isdir(PACKAGE_DIR)

# not yet needed but nice to have for when multiple boards are implemented
mcu = env.BoardConfig().get("build.mcu", "")

# Get environment variables for the nexmon build process
HOSTUNAME = subprocess.check_output(["uname", "-s"]).decode(encoding="utf-8").replace("\n", "")
PLATFORMUNAME = subprocess.check_output(["uname", "-m"]).decode(encoding="utf-8").replace("\n", "")

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

# Default compiler is currently for Linux x86_64

if HOSTUNAME in "Darwin":
    # Set Darwin specific compiler here
    raise NotImplementedError
elif (HOSTUNAME in "Linux" and PLATFORMUNAME in "armv7l") or PLATFORMUNAME in "armv6l":
    # Set Linux crosscompiler for arm here
    raise NotImplementedError

env.Append(
    CCPLUGIN = os.path.join(PACKAGE_DIR, "toolchain-gccarmnoneeabi", "gcc-nexmon-plugin", "nexmon.so"),
)

Export('env', "FRAMEWORK_DIR")


SConscript([#'buildtools/ucode_extractor.py',
            #'buildtools/flash_patch_extractor.py', 
            #'buildtools/b43-v3/b43-v3-assembler.py', 
            #'buildtools/b43-v3/b43-v3-disassembler.py',
            #'buildtools/b43-v3/b43-v3-fwcutter.py',
            #'buildtools/b43-v3/b43-v3-ssb_sprom.py',
            #'buildtools/b43-v2/b43-v2-assembler.py',
            #'buildtools/b43-v2/b43-v2-disassembler.py',
            #'buildtools/b43/b43-assembler.py',
            #'buildtools/b43/b43-disassembler.py',
            #'buildtools/b43/b43-fwcutter.py',
            #'buildtools/b43/b43-ssb_sprom.py',
            ], 
            exports=['env', 'FRAMEWORK_DIR'])
            

env.Append(
    CCFLAGS=[
        "-mcpu=%s" % env.BoardConfig().get("build.cpu"),
    ],
)

def PreCompileDependencies():
    rc = subprocess.Popen(["make", "-s"], cwd=os.path.join(FRAMEWORK_DIR, "buildtools", "b43", "assembler"))

PreCompileDependencies()
