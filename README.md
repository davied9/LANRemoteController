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

`python -m pip install git+https://github.com/PyUserInput/PyUserInput.git@d45f45ffbb2399d964eb515c887c493a1837c09d`

we do not use master here to avoid dependency on pyHook for python3 on windows (not neccessary && convenient)

##### pypiwin32 (needed by windows server)

`python -m pip install pypiwin32`

this is used for windows server

##### kivy (needed by client)

see [kivy official site](https://kivy.org/doc/stable/gettingstarted/installation.html)

if --no-ui is given to server, then kivy is not neccessary

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

All built packages will be found in ./dist

# Usage

### windows

make sure PythonXXX/Scripts/ in your system search path

call `lrcserver --no-ui start_lrc` to start server

call `lrcclient` to start client

type `lrcserver -h` or `lrcclient -h` for help

### android

1. use pydroid

copy the directory extracted from ./history_packages/LRCClient-x.x.x-Android.tar.gz to <android-device>/sdcard/kivy, 

then run main.py with kivy Laucher or pydroid (require kivy 1.10.1)

2. use built apk

./history_packages/LRC-0.1.3-release-unsigned.apk

# Releases Notes:

### 0.1.4

1. rename collections to lrccollections to avoid name conflict with matplotlib

2. replace argument parse process with ArgumentParser from argparse
