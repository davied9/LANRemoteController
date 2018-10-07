# LANRemoteController
Remote controller for LAN

# Description
Remote controller for LAN, based on [kivy](https://github.com/kivy/kivy) and [PyUserInput](https://github.com/SavinaRoja/PyUserInput) .

Basic implement thought :
- Client : Send key combination information in LAN
- Server : Explain key combination information and excute key combinations
    
    
Things will work on all kinds of devices involved with keyboard.

# Install

Dependency :

`python -m pip install git+https://github.com/SavinaRoja/PyUserInput.git@master`

`python -m pip install pypiwin32` # this is used for windows server

You can install LRC directly by pip :

`python -m pip install LRC`

Or install LRC from git:

`python -m pip install git+https://github.com/davied9/LANRemoteController.git@master`

# Distribution

scripts contains all distribution scripts

## Server

`python -m setup sdist bdist_wheel`

## Client

### Android

`cd scripts`

`python -m build_android_client`

the distribution package will be in dist\client\android

copy directory to sdcard/kivy, then run with kivy Laucher or pydroid (require kivy 1.10.1)

# Usage

add PythonXXX/Scripts/ to your system search path

call `lrcserver` to start server

call `lrcclient` to start client

type `lrcserver -h` or `lrcclient -h` for help

