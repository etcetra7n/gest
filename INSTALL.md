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

**Note:** If you use this installation method, the game may seem to 
run slower in *some* terminals. If the game runs laggy, either try using
other terminals or try other installation methods

### Build from source
Pyinstaller is required for this method. If you dont have it installed,
Install it using a simple pip install command. Then run the following command:
```s
pyinstaller src/gest.py
```
**Note:** If you use this installation method, the game may seem to 
run slower in *some* terminals. If the game runs laggy, either try using
other terminals or try other installation methods
