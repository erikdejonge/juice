@ECHO OFF

REM Set the NSIS script to use here !!
SET NSIS="iPodder-py24-2.2.nsi"

REM ****** Do not edit below here *******

Echo.
Echo Building iPodder for Windows
Echo.

cd ..

COPY win32\setup.py .

python setup.py py2exe

MOVE dist\gui.exe dist\iPodder.exe

cd win32

COPY iPodder.exe.manifest ..\dist\iPodder.exe.manifest

"C:\Program Files\NSIS\makensis.exe" %NSIS%

ECHO Deleting the setup file
DEL ..\setup.py

ECHO Deleting the dist build directory
RMDIR /S /Q ..\dist
RMDIR /S /Q ..\build\bdist.win32

Echo.
ECHO iPodder for windows created in win32\ directory
