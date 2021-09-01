# Introduction
This repository consists of the code and the necessary structure to represent a PlatformIO platform for the **PlatformIO Extension** of Visual Studio Code.

**It does not work with the command line version of PlatformIO installed via pip!**

When installed according to the steps described in [Installation](#installation) it can be used to create PlatformIO projects with nexmon support, allowing one to write custom patches for the target board.

# Installation
The following packages need to be installed locally for this to work properly:
```
pip3 install gitpython SCons
sudo apt-get install git gawk qpdf adb flex bison
```
**The next commands are only necessary for x86_64 systems:**
```
sudo dpkg --add-architecture i386
sudo apt-get update
sudo apt-get install libc6:i386 libncurses5:i386 libstdc++6:i386
```

To use this repository install the Visual Studio Code extension [PlatformIO IDE](https://marketplace.visualstudio.com/items?itemName=platformio.platformio-ide).

The extension will automatically generate a .platformio folder at *~/.platformio*. (Assuming that you are on a machine running a UNIX OS)  
This is where PlatformIO will from now on store all information related to locally installed platforms, packages or boards.

Now to install this platform change directories to *~/.platformio/platforms/* and clone the repository into this folder.

`git clone https://github.com/umr-ds/platformio_nexmon.git`

At last open up Visual Studio Code, open the PlatformIO extension (There should be a symbol that looks like an ant head on the left of the VS Code window). Opening the extension should give you access to the quick access menu. There under *updates* execute the **Update All** function by left clicking and PlatformIO should automatically update its local database with the *Platform-Cypress* and the new boards.

# Usage
## Creating a new project
Now in order to use this platform for creating a new project to write a custom patch with nexmon just follow along these steps:
1. Open VS Code
2. Open the PlatformIO extension's quick access menu by left clicking the ant head on the left of your VS Code window
3. Under **PIO Home** left-click **Open**
4. PlatformIO's home menu should open inside of VS Code with another quick access menu
5. Left-click **+ New Project**. This should open PlatformIO's project wizard.
6. Under **Board** search for **nexmon**. This should give you a list of all boards that are currently supported by this platform
7. The **Framework** will be automatically set to *Mbed*. (Hint: **This CAN NOT and SHOULD NOT be changed**)
8. Specify a location to where the project files are saved (If not specified the default is *~/Documents/PlatformIO/Projects/*)
9. Hit **Finish**

When doing this for the first time this might take **quite a lot of time** depending on your internet connection, because the [nexmon](https://github.com/seemoo-lab/nexmon) repository has to be cloned into *~/.platformio/packages/*.

When finished VS Code will automatically open the new project folder with the following structure:

.  
├── include  
├── lib  
├── .pio  
├── src  
├── test  
└── .vscode


## Writing a custom patch
After a new project is generated the necessary source files are found inside of the project's src-folder. Inside of the src-folder the empty *main.c* file can be used to write a custom patch.

## Building
To build your custom patch follow these steps:
1. Open the PlatformIO extension's quick access menu again by left clicking the ant head on the left of your VS Code window
2. A new menu called **Project Tasks** should appear there now
3. Under **Project Tasks** left-click onto the name of the board you are developing a patch for. This should open a new menu
4. There under **General** left-click the **Build** option
5. A terminal should open inside of VS Code showing all steps nexmon goes through when building and applying a patch
6. The important part here is: **PlatformIO's own build will fail** showing all kinds of error messages, because the platform is not exactly using PlatformIO's method of building a project. **This is normal and expected. It has no impact on the build of the patch whatsoever.**
7. To look for whether the build executed properly scroll up until you find these messages:  
    ```bash
    Building the buildtools exited with exit code: 0  
    Building the patch exited with exit code: 0  
    Backing up the current firmware exited with exit code: 0  
    Installing the new firmware exited with exit code: 0
    ```
8. The exit codes are process exit codes. Every other exit code besides 0 means something went wrong
9.  To spare yourself from having to scroll through the error messages manually it is possible to execute the build process from a terminal and pipe the output into something like grep to provide a better overview
10. Instead of executing build from the **Project Tasks** menu, open the **Quick Access** menu item, scroll down until you see **Miscellaneous** and left-click **PlatformIO Core CLI**. This will open a terminal in which you have access to PlatformIO's terminal interface. Type **pio run** into the terminal and pipe the output into something like grep to get a more sanitized build output.

## Adding support for a new board
To add support for a new board follow these steps:
1. Create a new json file named after the board and the firmware you want to use inside `/platformio_nexmon/boards`
   1. e.g. *nexmon_nexus5_6_37_34_43.json*
2. Copy the following code into the new file and only edit the lines that have comments beside them:  
    ```json
    {
        "build": {
            "core": "arm",
            "cpu": "arm8",
            "f_cpu": "2300000000L",
            "mcu": "bcm4339", //<-- replace this with the WiFi chip used by the new board
            "firmware": "6_37_34_43" // <-- replace this with the firmware version you want to use
        },
        "frameworks": [
            "mbed"
        ],
        "name": "Nexus 5 Nexmon 6_37_34_43", // <-- give the new board a recognizable name
        "upload": {
            "maximum_ram_size": 2147483648,
            "maximum_size": 2147483648
        },
        "url": "https://www.qualcomm.com/media/documents/files/snapdragon-800-product-brief.pdf",
        "vendor": "Qualcomm"
    }
    ```
3. Now when you open the PlatformIO extension in VS Code and create a new project you should be able to search for the name of the new board