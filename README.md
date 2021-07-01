# Introduction
This repository consists of the code and the necessary structure to represent a PlatformIO platform for the **PlatformIO Extension** of Visual Studio Code.

**It does not work with the command line version of PlatformIO installed via pip!**

When installed according to the steps described in [Installation](#installation) it can be used to create PlatformIO projects with nexmon support, allowing one to write custom patches for the target board.

# Installation
To use this repository install the Visual Studio Code extension [PlatformIO IDE](https://marketplace.visualstudio.com/items?itemName=platformio.platformio-ide).

The extension will automatically generate a .platformio folder at *~/.platformio*. (Assuming that you are on a machine running a UNIX OS)  
This is where PlatformIO will from now on store all information related to locally installed platforms, packages or boards.

Now to install this platform change directories to *~/.platformio/platforms/* and clone the repository into this folder. Once this is done go into the newly created folder, go into the *boards* folder and copy the contents from there into *~/.platformio/boards*.

At last open up Visual Studio Code, open the PlatformIO extension (There should be a symbol that looks like an ant head on the left of the VS Code window). Opening the extension should give you access to the quick access menu. There under *updates* execute the **Update All** function by left clicking and PlatformIO should automatically update its local database with the *Platform-Cypress*.
