# LANRemoteController
Remote controller for LAN

# Description
Remote controller for LAN, based on [kivy](https://github.com/kivy/kivy) and [PyUserInput](https://github.com/SavinaRoja/PyUserInput) .

Basic implement thought :
- Client : Send key combination information in LAN
- Server : Explain key combination information and excute key combinations
    
    
Things will work on all kinds of devices involved with keyboard.

# Install

### Dependency :

##### PyUseInput (needed by server)

`python -m pip install git+https://github.com/SavinaRoja/PyUserInput.git@master`

##### pypiwin32 (needed by windows server)

`python -m pip install pypiwin32` # this is used for windows server

##### kivy (needed by client)

see [kivy official site](https://kivy.org/doc/stable/gettingstarted/installation.html)

### LRC

You can install LRC directly by pip :

`python -m pip install LRC`

Or install LRC from git:

`python -m pip install git+https://github.com/davied9/LANRemoteController.git@master`

All packages can directly get from [here](https://github.com/davied9/LANRemoteController/tree/master/history_packages):

# Distribution

Run the following commands, packages will be found in ./dist

`cd scripts`

`python -m build`

All packages will be found in ./dist

# Usage

### windows

make sure PythonXXX/Scripts/ in your system search path

call `lrcserver` to start server

call `lrcclient` to start client

type `lrcserver -h` or `lrcclient -h` for help

### android

copy the directory extracted from ./dist/LRCClient-x.x.x-Android.tar.gz to <android-device>/sdcard/kivy, 

then run main.py with kivy Laucher or pydroid (require kivy 1.10.1)

