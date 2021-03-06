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

The extension will automatically generate a .platformio folder at _~/.platformio_. (Assuming that you are on a machine running a UNIX OS)  
This is where PlatformIO will from now on store all information related to locally installed platforms, packages or boards.

Now to install this platform open VS Code, then open the PlatformIO extension (Ant head on the left of your editor window). Under **PIO Home** navigate to **Platforms** and select **Advanced Installation**. Insert the repository `https://github.com/umr-ds/platformio_nexmon.git` into the new window and click **Install**. After a while a new window should inform you about the successful installation. The installed platform should be listed under **Platforms** and can be used to instantiate new projects. 

# Usage

## Creating a new project

Now in order to use this platform for creating a new project to write a custom patch with nexmon just follow along these steps:

1. Open VS Code
2. Open the PlatformIO extension's quick access menu
3. Under **PIO Home** left-click **Open**
4. PlatformIO's home menu should open inside of VS Code with another quick access menu
5. Left-click **+ New Project**. This should open PlatformIO's project wizard.
6. Under **Board** search for **nexmon**. This should give you a list of all boards that are currently supported by this platform
7. The **Framework** will be automatically set to _Mbed_. (Hint: **This CAN NOT and SHOULD NOT be changed**)
8. Specify a location to where the project files are saved (If not specified the default is _~/Documents/PlatformIO/Projects/_)
9. Hit **Finish**

When doing this for the first time this might take **quite a lot of time** depending on your internet connection, because the [nexmon](https://github.com/seemoo-lab/nexmon) repository has to be cloned into _~/.platformio/packages/_.

When finished VS Code will automatically open the new project folder with the following structure:

.  
????????? include  
????????? lib  
????????? .pio  
????????? src  
????????? test  
????????? .vscode

### Troubleshooting

In case VSCode shows an error after Step 9. PlatformIO probably did not find the python modules needed for building the project.  
To resolve this problem add the following environment variable to your .bashrc (or whatever shell you are using):

```
export PYTHONPATH=$PYTHONPATH/home/<username>/.local/lib/python3.8/site-packages/:/home/<username>/.local/bin
```

Then:

```
source .bashrc
```

and restart VS Code.

**Note:** Replace `python3.8` in the path by whatever python version you used to install `gitpython` and `SCons` or, if you have multiple python version, add all of their site-packages folders to the path.

## Writing a custom patch

After a new project is generated the necessary source files are found inside of the project's src-folder. Inside of the src-folder the empty _main.c_ file can be used to write a custom patch.

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
   1. The exit codes are process exit codes. Every other exit code besides 0 means something went wrong
   2. To spare yourself from having to scroll through the error messages manually it is possible to execute the build process from a terminal and pipe the output into something like grep to provide a better overview
   3.  Instead of executing build from the **Project Tasks** menu, open the **Quick Access** menu item, scroll down until you see **Miscellaneous** and left-click **PlatformIO Core CLI**. This will open a terminal in which you have access to PlatformIO's terminal interface. Type **pio run** into the terminal and pipe the output into something like grep to get a more sanitized build output.
