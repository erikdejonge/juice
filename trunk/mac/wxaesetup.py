#!/usr/bin/env python

from distutils.core import setup, Extension
import os, string

# WXBASE="/usr/local/lib/wxPython-unicode-2.5.5.1/"
WXINCLUDE = '/opt/local/include/wx-2.6/'
WXCONFIG = '/opt/local/bin/wx-config'


defines = [('SWIG_GLOBAL', None),
           ('HAVE_CONFIG_H', None),
           ('WXP_USE_THREAD', '1'),
          ]
cflags = os.popen('%s --cxxflags' % WXCONFIG, 'r').read()[:-1]
cflags = string.split(cflags)
lflags = os.popen('%s --libs' % WXCONFIG, 'r').read()[:-1]
lflags = string.split(lflags)

setup(name = "wxae",
      version = "1.0",
      description = "",
      ext_modules = [Extension("wxae", ["wxaemodule.cpp"],
                               define_macros = defines,
                               extra_compile_args = cflags,
                               extra_link_args = lflags,
                               include_dirs = [WXINCLUDE],
                               )]
)
