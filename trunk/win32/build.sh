#!/bin/bash

tag="v2_2"

cd /cygdrive/c
if [ -d juice ]; then
  mv juice juice-`date +"%Y%m%d-%H%m%S"`
fi

cvs -d :ext:$USERNAME@cvs.sourceforge.net:/cvsroot/juicereceiver export -r $tag juice
cd juice
cp win32/setup.py .
python setup.py py2exe
mv dist/gui.exe dist/Juice.exe
cp /cygdrive/c/Python23/python.exe.manifest dist/Juice.exe.manifest
cd win32
/cygdrive/c/Program\ Files/NSIS/makensis.exe iPodder2.2.nsi
