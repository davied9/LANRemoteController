# LANRemoteController
Remote controller for LAN

# Description
Remote controller for LAN, based on [kivy UI framework](https://github.com/kivy/kivy).

Basic implement thought :
- Client : Send key combination information in LAN
- Server : Explain key combination information and excute key combinations
    
    
Things will work on all kinds of devices involved with keyboard, thanks to SavinaRoja/PyUserInput.

# Distribution

build/scripts contains all distribution scripts

## Server


## Client

### Android

`cd build/scripts`
`python -m build_android_client`

the distribution package will be in build\client\android
copy directory to sdcard/kivy, then run with kivy Laucher or pydroid (require kivy 1.10.1)

# Thanks
[PyUserInput by SavinaRoja](https://github.com/SavinaRoja/PyUserInput), distributed with GNU GENERAL PUBLIC LICENSE

