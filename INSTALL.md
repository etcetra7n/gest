# Installation

### Using pip (recommended)
If you have python installed, run the following script

```s
pip install gester
```

### Using NSIS (Only on windows)
NSIS software can be used to create a installer (or setup) executable.
Download the NSIS software on [sourceforge](https://nsis.sourceforge.io/Download)
After installing NSIS, run the following command
```s
makensis nsis/installer.nsi
```
You will find a executable file (.exe file) in the nsis directory. Run this 
executable to have GEST installed. This installation method will also 
set up file type configurations which will make it easier to run the games

**Note:** Using this installation method the game may seem to 
run slower in *some* terminals. If the game runs laggy, try
other installation methodss

### Build from source
Pyinstaller is required for this method. If you dont have it installed.
Install it using a simple pip install command
```s
pyinstaller src/gest.py
```
**Note:** Using this installation method the game may seem to 
run slower in *some* terminals. If the game runs laggy, try
other installation methods
