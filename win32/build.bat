@ECHO OFF

REM Set the NSIS script to use here !!
set NSIS_FILE="Juice-2.2.3.nsi"
REM Where you installed NSIS
set NSIS=C:\Program Files\NSIS
REM Where you installed Python (must include py2exe)
set PYTHONDIR="C:\dev\python24"
REM the installed EXE name
set EXEFILE=Juice.exe

REM ****** Do not edit below here *******

Echo.
Echo Building Juice for Windows
Echo.

cd ..
set PATH=%PYTHONDIR%;%PATH%

COPY win32\setup.py .

python setup.py py2exe
COPY win32\iPodder.exe.manifest dist\%EXEFILE%.manifest

cd win32

python genInstallList.py ..\dist installList.nsh uninstallList.nsh
"%NSIS%\makensis.exe" /DINSTALL_LIST=installList.nsh /DUNINSTALL_LIST=uninstallList.nsh %NSIS_FILE%

ECHO Deleting the setup file
DEL ..\setup.py

ECHO Deleting the dist build directory
RMDIR /S /Q ..\dist
RMDIR /S /Q ..\build\bdist.win32

Echo.
ECHO Juice for windows created in win32\ directory
