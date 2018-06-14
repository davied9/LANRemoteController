@echo off

if "%1%"=="" goto End

if %1%==server (
python3 -m PyInstaller --name server .\Server\ServerUI.py
goto End
)

if %1%==client (
python3 -m PyInstaller --name client .\ClientWin\ClientUI.py
goto End
)

if %1%==test (
python3 -m PyInstaller --name test .\Test\T007_kivy_start.py
goto End
)

:End
@echo on
