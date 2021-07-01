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
from distutils.dir_util import copy_tree
from distutils.file_util import copy_file
from distutils.dir_util import mkpath
from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
platform = env.PioPlatform()
board = env.BoardConfig()
# needed for differentiating between multiple chips (bcm4330, bcm4339...)
mcu = board.get("build.mcu")
# needed for differentiating between multiple firmware versions (6_37_34_43, ...)
firmware = board.get("build.firmware")

FRAMEWORK_DIR = platform.get_package_dir("framework-mbed")
PACKAGE_DIR = os.path.dirname(FRAMEWORK_DIR) # Directory that holds all local PlatformIO packages
NEXMON_DIR = os.path.join(PACKAGE_DIR, "nexmon") # Directory inside of PlatformIO's package directory where nexmon is cloned to
BUILDTOOLS = os.path.join(NEXMON_DIR, "buildtools") # Directory of nexmon's buildtools
FIRMWARES = os.path.join(NEXMON_DIR, "firmwares") # Directory of nexmon's firmwares
PROJECT_DIR = env["PROJECT_DIR"] # Directory where the project is generated
SRC_DIR = os.path.join(PROJECT_DIR, "src") # Src folder of the generated project; the custom patch will be written in here
LIB_DIR = os.path.join(PROJECT_DIR, "lib") # Lib folder of the generated project; all nexmon relevant files will go into here
PROJECT_NEXMON_DIR = os.path.join(LIB_DIR, "nexmon") # Directory where nexmon is stored inside of the project

# If nexmon is not found, clone it into PlatformIO's package directory
if not isdir(NEXMON_DIR):
    git.Repo.clone_from("https://github.com/seemoo-lab/nexmon", to_path=NEXMON_DIR)

# Removing the unneeded main.cpp that is generated at the beginning of each new PlatformIO project
if isfile(os.path.join(SRC_DIR, "main.cpp")):
    os.remove(os.path.join(SRC_DIR, "main.cpp"))

# Copying all important nexmon files into the project folder
if not isdir(PROJECT_NEXMON_DIR):
    # Creating the nexmon folder that will hold all files for building the patch
    os.mkdir(os.path.join(LIB_DIR, "nexmon"))

    # Copying the buildtool files
    copy_tree(
        os.path.join(BUILDTOOLS, "b43"),
        os.path.join(PROJECT_NEXMON_DIR, "buildtools", "b43"),
    )
    copy_tree(
        os.path.join(BUILDTOOLS, "b43-v2"),
        os.path.join(PROJECT_NEXMON_DIR, "buildtools", "b43-v2"),
    )
    copy_tree(
        os.path.join(BUILDTOOLS, "b43-v3"),
        os.path.join(PROJECT_NEXMON_DIR, "buildtools", "b43-v3"),
    )
    copy_tree(
        os.path.join(BUILDTOOLS, "flash_patch_extractor"),
        os.path.join(PROJECT_NEXMON_DIR, "buildtools", "flash_patch_extractor"),
    )
    copy_tree(
        os.path.join(BUILDTOOLS, "isl-0.10"),
        os.path.join(PROJECT_NEXMON_DIR, "buildtools", "isl-0.10"),
    )
    copy_tree(
        os.path.join(BUILDTOOLS, "mkboot"),
        os.path.join(PROJECT_NEXMON_DIR, "buildtools", "mkboot"),
    )
    copy_tree(
        os.path.join(BUILDTOOLS, "mpfr-3.1.4"),
        os.path.join(PROJECT_NEXMON_DIR, "buildtools", "mpfr-3.1.4"),
    )
    copy_tree(
        os.path.join(BUILDTOOLS, "scripts"),
        os.path.join(PROJECT_NEXMON_DIR, "buildtools", "scripts"),
    )
    copy_tree(
        os.path.join(BUILDTOOLS, "ucode_extractor"),
        os.path.join(PROJECT_NEXMON_DIR, "buildtools", "ucode_extractor"),
    )
    copy_file(
        os.path.join(BUILDTOOLS, "Makefile"),
        os.path.join(PROJECT_NEXMON_DIR, "buildtools"),
    )

    # Copying the firmware files
    copy_tree(
        os.path.join(FIRMWARES, mcu, firmware),
        os.path.join(PROJECT_NEXMON_DIR, "firmwares", mcu, firmware),
    )
    copy_file(
        os.path.join(FIRMWARES, "Makefile"),
        os.path.join(PROJECT_NEXMON_DIR, "firmwares"),
    )
    copy_file(
        os.path.join(FIRMWARES, mcu, "Makefile"),
        os.path.join(PROJECT_NEXMON_DIR, "firmwares", mcu),
    )
    copy_file(
        os.path.join(FIRMWARES, mcu, "structs.common.h"),
        os.path.join(PROJECT_NEXMON_DIR, "firmwares", mcu),
    )

    # Creating the nexmon specific path that will hold the patch source files
    mkpath(os.path.join(PROJECT_NEXMON_DIR, "patches", mcu, firmware, "nexmon", "src"))

    # Copying only the necessary files and folders into the patches folder
    copy_tree(
        os.path.join(NEXMON_DIR, "patches", "include"),
        os.path.join(PROJECT_NEXMON_DIR, "patches", "include"),
    )
    copy_tree(
        os.path.join(NEXMON_DIR, "patches", "common"),
        os.path.join(PROJECT_NEXMON_DIR, "patches", "common"),
    )
    copy_tree(
        os.path.join(NEXMON_DIR, "patches", mcu, firmware, "nexmon", "include"),
        os.path.join(PROJECT_NEXMON_DIR, "patches", mcu, firmware, "nexmon", "include"),
    )
    copy_file(
        os.path.join(NEXMON_DIR, "patches", mcu, firmware, "nexmon", "Makefile"),
        os.path.join(PROJECT_NEXMON_DIR, "patches", mcu, firmware, "nexmon"),
    )
    copy_file(
        os.path.join(NEXMON_DIR, "patches", mcu, firmware, "nexmon", "patch.ld"),
        os.path.join(PROJECT_NEXMON_DIR, "patches", mcu, firmware, "nexmon"),
    )
    copy_file(
        os.path.join(NEXMON_DIR, "patches", mcu, firmware, "version.mk"),
        os.path.join(PROJECT_NEXMON_DIR, "patches", mcu, firmware, "version.mk"),
    )
    # Copying the original patch source files into the project src folder
    copy_tree(
        os.path.join(NEXMON_DIR, "patches", mcu, firmware, "nexmon", "src"), SRC_DIR
    )
    # Copying the root Makefile of nexmon into the Project
    copy_file(os.path.join(NEXMON_DIR, "Makefile"), PROJECT_NEXMON_DIR)
    # Creating the main.c that will be available for writing custom patches
    open(os.path.join(SRC_DIR, "main.c"), "a").close()

# When building copy the files in the project src folder to the nexmon patch folder where they are supposed to be according to the makefile
copy_tree(
    SRC_DIR,
    os.path.join(PROJECT_NEXMON_DIR, "patches", mcu, firmware, "nexmon", "src"),
)

# Include path go here
env.Append(
    CPPPATH=[
        os.path.join(NEXMON_DIR, "patches", "include"),
        os.path.join(NEXMON_DIR, "patches", "common"),
        os.path.join(NEXMON_DIR, "patches", mcu, firmware, "nexmon", "include"),
        os.path.join(PROJECT_NEXMON_DIR, "firmwares", mcu, firmware),
    ]
)

# Get system specifications for the nexmon build process
HOSTUNAME = (
    subprocess.check_output(["uname", "-s"])
    .decode(encoding="utf-8")
    .replace("\n", "")
)
PLATFORMUNAME = (
    subprocess.check_output(["uname", "-m"])
    .decode(encoding="utf-8")
    .replace("\n", "")
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
        NEXMON_DIR, "buildtools", "gcc-nexmon-plugin", "nexmon.so"
    )
    os.environ["ZLIBFLATE"] = "zlib-flate -compress"
elif (
    HOSTUNAME in "Linux" and PLATFORMUNAME in "armv7l"
) or PLATFORMUNAME in "armv6l":
    os.environ["CC"] = os.path.join(
        NEXMON_DIR,
        "buildtools",
        "gcc-arm-none-eabi-5_4-2016q2-linux-armv7l",
        "bin",
        "arm-none-eabi-",
    )
    os.environ["CCPLUGIN"] = os.path.join(
        NEXMON_DIR, "buildtools", "gcc-nexmon-plugin-arm", "nexmon.so"
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

# This is where the patch files are kept in the project
patch_path = os.path.join(PROJECT_NEXMON_DIR, "patches", mcu, firmware, "nexmon")

# Build buildtools and firmware files
rc = subprocess.call(["make", "-s"], cwd=PROJECT_NEXMON_DIR)
# Build patched firmware
rc1 = subprocess.call(
    ["make", "-s"],
    cwd=patch_path,
)
# Backup current firmware
rc2 = subprocess.call(["make", "backup-firmware"], cwd=patch_path)
# Install new firmware
rc3 = subprocess.call(["make", "install-firmware"], cwd=patch_path)

print(rc, rc1, rc2, rc3)
