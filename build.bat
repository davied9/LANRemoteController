@echo off

if "%1%"=="" goto End

if %1%==server (
echo build server for win32
python3 -m PyInstaller --name server .\Server\ServerUI.py
)

if %1%==client (
echo build client for win32
python3 -m PyInstaller --name client .\Client\ClientUI.py
)

if %1%==test (
echo build test for win32
python3 -m PyInstaller --name test .\Test\T007_kivy_start.py
)

if %1%==temp (
echo build client for android
echo this is not ready !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
p4a apk --private .\Client\ClientUI.py --package=dav.LRC.LRCClient --name "LRCClient" --version 0.1 --bootstrap=sdl2 --requirements=python3,kivy
)

:End
@echo on
