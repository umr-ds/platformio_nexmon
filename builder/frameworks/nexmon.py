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

import os
import git
import subprocess
from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
platform = env.PioPlatform()
board = env.BoardConfig()

# Spoofing Nexmon as mbed currently to skip having to publish it as a package
FRAMEWORK_DIR = platform.get_package_dir("framework-mbed")
PACKAGE_DIR = os.path.dirname(FRAMEWORK_DIR)
assert os.path.isdir(FRAMEWORK_DIR)
assert os.path.isdir(PACKAGE_DIR)

file = os.path.join(PACKAGE_DIR, "test.txt")
open(file, 'a').close()
if not os.path.isdir(os.path.join(PACKAGE_DIR, "nexmon")):
    git.Repo.clone_from("https://github.com/seemoo-lab/nexmon", to_path=os.path.join(PACKAGE_DIR, "nexmon"))

# needed for differentiating between multiple chips (bcm433, bcm4339...)
mcu = env.BoardConfig().get("build.mcu")
cpu = env.BoardConfig().get("build.cpu")

# Get environment variables for the nexmon build process
HOSTUNAME = (
    subprocess.check_output(["uname", "-s"]).decode(encoding="utf-8").replace("\n", "")
)
PLATFORMUNAME = (
    subprocess.check_output(["uname", "-m"]).decode(encoding="utf-8").replace("\n", "")
)

# Default compiler is currently for Linux x86_64
if (HOSTUNAME in "Darwin") or (
    (HOSTUNAME in "Linux" and PLATFORMUNAME in "armv7l") or PLATFORMUNAME in "armv6l"
):
    raise NotImplementedError

# Setting up the nexmon build environment
os.environ["ARCH"] = "arm"
os.environ["SUBARCH"] = "arm"
os.environ["KERNEL"] = "kernel7"
os.environ["HOSTUNAME"] = HOSTUNAME
os.environ["PLATFORMUNAME"] = PLATFORMUNAME
os.environ["NEXMON_ROOT"] = FRAMEWORK_DIR
os.environ["CC"] = os.path.join(
    FRAMEWORK_DIR,
    "buildtools",
    "gcc-arm-none-eabi-5_4-2016q2-linux-x86",
    "bin",
    "arm-none-eabi-",
)
os.environ["CCPLUGIN"] = os.path.join(
    PACKAGE_DIR, "Nexmon-Toolchains", "gcc-nexmon-plugin", "nexmon.so"
)
os.environ["ZLIBFLATE"] = "zlib-flate -compress"
os.environ["Q"] = "@"
os.environ["NEXMON_SETUP_ENV"] = "1"

patch_path = os.path.join(FRAMEWORK_DIR, "patches", mcu, "6_37_34_43", "nexmon")
# Build buildtools and firmware files
rc = subprocess.Popen(["make", "-s"], cwd=FRAMEWORK_DIR)
# Build patched firmware
"""rc1 = subprocess.Popen(
    ["make", "-s"],
    cwd=patch_path,
)
# Backup current firmware
rc2 = subprocess.Popen(
    ["make", "backup-firmware"],
    cwd=patch_path
)
# Install new firmware
rc3 = subprocess.Popen(
    ["make", "install-firmware"],
    cwd=patch_path
)
"""
