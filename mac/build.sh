#!/bin/bash

tag="v2_2b1"

cd ~
if [ -d iSpider-build ]; then
  mv iSpider-build iSpider-build-`date +"%Y%m%d-%H%m%S"`
fi

cvs -d :ext:$USERNAME@cvs.sourceforge.net:/cvsroot/ipodder export -d iSpider-build -r $tag iSpider
cd iSpider-build
cp mac/setup.py .
unset PYTHONPATH
/usr/bin/python setup.py py2app
  
