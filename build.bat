@echo off

if "%1%"=="" goto End

if %1%==server (
python3 -m PyInstaller --name server .\Server\ServerUI.py
)

if %1%==client (
python3 -m PyInstaller --name client .\ClientWin\ClientUI.py
)

if %1%==test (
python3 -m PyInstaller --name test .\Test\T001_UsingKivy.py
)

:End
@echo on
