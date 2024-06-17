# SaveWizard

* Author of original "SaveWizard" script: DrEGZo
* Original script is taken from here: <https://forum.truckersmp.com/index.php?/topic/55773-savewizard/> (access to the topic has been closed)
* Utility to decrypt file: <https://github.com/TheLazyTomcat/SII_Decrypt>

***

Features:
1. Decrypt file, if save file crypted
2. Check for DLC to the save file (available DLC listed at [DLC_TABLE.md](https://github.com/JDM170/SaveWizard/blob/configs/DLC_TABLE.md))
3. Edit money, experience and loan limit
4. Edit skills
5. Visit cities, unlock garages, dealers and agencies

***

To build project You need Python 3.10.7 and installed requirements from [requirements.txt](https://github.com/JDM170/SaveWizard/blob/dev/requirements.txt)

Command to convert .ui to .py: ```pyuic5 -x input.ui -o output.py```
Commands to build project:
- cx_Freeze: ```python setup.py build```
- PyInstaller: ```pyinstaller build.spec --clean```

***

#### If you've found a bug - please open an issue
