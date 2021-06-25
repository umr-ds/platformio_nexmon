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

from genericpath import isdir, isfile
import os
import git
import subprocess
import shutil
import glob
from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
platform = env.PioPlatform()
board = env.BoardConfig()
# needed for differentiating between multiple chips (bcm4330, bcm4339...)
mcu = board.get("build.mcu")
cpu = board.get("build.cpu")
firmware = board.get("build.firmware")

# Spoofing Nexmon as mbed currently to skip having to publish it as a package
FRAMEWORK_DIR = platform.get_package_dir("framework-mbed")
PACKAGE_DIR = os.path.dirname(FRAMEWORK_DIR)
NEXMON_DIR = os.path.join(PACKAGE_DIR, "nexmon")
BUILDTOOLS = os.path.join(NEXMON_DIR, "buildtools")
FIRMWARES = os.path.join(NEXMON_DIR, "firmwares")
PROJECT_DIR = env["PROJECT_DIR"]
BUILD_DIR = env["PROJECT_BUILD_DIR"]
SRC_DIR = os.path.join(PROJECT_DIR, "src")
LIB_DIR = os.path.join(PROJECT_DIR, "lib")
PROJECT_NEXMON_DIR = os.path.join(SRC_DIR, "nexmon")

assert os.path.isdir(FRAMEWORK_DIR)
assert os.path.isdir(PACKAGE_DIR)
assert os.path.isdir(PROJECT_DIR)
assert os.path.isdir(BUILD_DIR)
assert os.path.isdir(SRC_DIR)
assert os.path.isdir(LIB_DIR)

# If nexmon is not found, clone it into PlatformIO's package directory
if not isdir(NEXMON_DIR):
    git.Repo.clone_from("https://github.com/seemoo-lab/nexmon", to_path=NEXMON_DIR)

# Remove the unneeded main.cpp
if isfile(os.path.join(SRC_DIR, "main.cpp")):
    os.remove(os.path.join(SRC_DIR, "main.cpp"))

# Copy all the necessary files from nexmon to the project folder
if not isdir(PROJECT_NEXMON_DIR):
    os.mkdir(os.path.join(SRC_DIR, "nexmon"))
    shutil.copytree(BUILDTOOLS, os.path.join(PROJECT_NEXMON_DIR, "buildtools"))
    shutil.copytree(os.path.join(FIRMWARES, f"{mcu}"), os.path.join(PROJECT_NEXMON_DIR, "firmwares", f"{mcu}"))
    shutil.copy(os.path.join(FIRMWARES, "Makefile"), os.path.join(PROJECT_NEXMON_DIR, "firmwares"))
    shutil.copy(os.path.join(NEXMON_DIR, "Makefile"), PROJECT_NEXMON_DIR)
    shutil.copytree(os.path.join(NEXMON_DIR, "patches", "common"), os.path.join(PROJECT_NEXMON_DIR, "patches", "common"))
    shutil.copytree(os.path.join(NEXMON_DIR, "patches", "include"), os.path.join(PROJECT_NEXMON_DIR, "patches", "include"))
    shutil.copytree(os.path.join(NEXMON_DIR, "patches", f"{mcu}"), os.path.join(PROJECT_NEXMON_DIR, "patches", f"{mcu}"))
    open(os.path.join(PROJECT_NEXMON_DIR, "patches", f"{mcu}", f"{firmware}", "nexmon", "src", "main.c"), "a").close()

env.Append(CPPPATH=[
    os.path.join(PROJECT_NEXMON_DIR, "patches", "include"),
    os.path.join(PROJECT_NEXMON_DIR, "patches", "common"),
    os.path.join(PROJECT_NEXMON_DIR, "patches", "include"),
    os.path.join(PROJECT_NEXMON_DIR, "firmwares", mcu, firmware)
])

# Get system specifications for the nexmon build process
HOSTUNAME = (
    subprocess.check_output(["uname", "-s"]).decode(encoding="utf-8").replace("\n", "")
)
PLATFORMUNAME = (
    subprocess.check_output(["uname", "-m"]).decode(encoding="utf-8").replace("\n", "")
)

# Default compiler is currently for Linux x86_64
if HOSTUNAME in "Linux" and PLATFORMUNAME in "x86_64":
    os.environ["CC"] = os.path.join(
        NEXMON_DIR,
        "buildtools",
        "gcc-arm-none-eabi-5_4-2016q2-linux-x86",
        "bin",
        "arm-none-eabi-",
    )
    os.environ["CCPLUGIN"] = os.path.join(
        PROJECT_NEXMON_DIR, "buildtools", "gcc-nexmon-plugin", "nexmon.so"
    )
    os.environ["ZLIBFLATE"] = "zlib-flate -compress"
elif (HOSTUNAME in "Linux" and PLATFORMUNAME in "armv7l") or PLATFORMUNAME in "armv6l":
    os.environ["CC"] = os.path.join(
        NEXMON_DIR,
        "buildtools",
        "gcc-arm-none-eabi-5_4-2016q2-linux-armv7l",
        "bin",
        "arm-none-eabi-",
    )
    os.environ["CCPLUGIN"] = os.path.join(
        PROJECT_NEXMON_DIR, "buildtools", "gcc-nexmon-plugin-arm", "nexmon.so"
    )
else:
    raise NotImplementedError

# Setting up the nexmon build environment
os.environ["ARCH"] = "arm"
os.environ["SUBARCH"] = "arm"
os.environ["KERNEL"] = "kernel7"
os.environ["HOSTUNAME"] = HOSTUNAME
os.environ["PLATFORMUNAME"] = PLATFORMUNAME
os.environ["NEXMON_ROOT"] = PROJECT_NEXMON_DIR
os.environ["Q"] = "@"
os.environ["NEXMON_SETUP_ENV"] = "1"

patch_path = os.path.join(PROJECT_NEXMON_DIR, "patches", mcu, firmware, "nexmon")

# Build buildtools and firmware files
rc = subprocess.call(["make", "-s"], cwd=PROJECT_NEXMON_DIR)
# Build patched firmware
rc1 = subprocess.call(
    ["make", "-s"],
    cwd=patch_path,
)
# Backup current firmware
rc2 = subprocess.call(
    ["make", "backup-firmware"],
    cwd=patch_path
)
# Install new firmware
rc3 = subprocess.call(
    ["make", "install-firmware"],
    cwd=patch_path
)

print(rc, rc1, rc2, rc3)