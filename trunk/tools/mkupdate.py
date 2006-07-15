import zipfile
import time
import os, os.path
import sys

assert os.path.isfile('updater.py'), "Run this from the source directory!"

sys.path.insert(0, 'win32')
import setup

filename = "juice-%04d-%02d-%02d.zip" % time.localtime()[:3]
filename = os.path.join('dist', filename)
# zipfile.PyZipFile(filename, 'w').writepy('ipodder')
zf = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)

for top in ['ipodder', 'gui']: 
    for root, dirs, files in os.walk(top): 
        if os.path.split(root)[1] == 'CVS': 
            continue
        for file in files: 
            name, ext = os.path.splitext(file)
            if not ext in ['.py']: 
                continue
            print file
            zf.write(os.path.join(root, file))

for root, files in setup.kwargs['data_files']: 
    for file in files: 
        print file
        zf.write(file)

for file in ['iPodderGui.py']: 
    print file
    zf.write(file)

zf.close()
os.system(filename)
