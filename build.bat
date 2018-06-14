@echo off

if "%1%"=="" goto End

if %1%==server (
echo build server for win32
python3 -m PyInstaller --name server .\Server\ServerUI.py
goto End
)

if %1%==client (
echo build client for win32
python3 -m PyInstaller --name client .\ClientWin\ClientUI.py
goto End
)

if %1%==test (
echo build test for win32
python3 -m PyInstaller --name test .\Test\T007_kivy_start.py
goto End
)

:End
@echo on
