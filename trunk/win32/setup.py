from distutils.core import setup
import py2exe
import os

kwargs = dict(
    version = "2.2",
    description = "Juice",
    name = "Juice",

    # targets to build
    windows = [ {
        "script": "gui.py", 
        "icon_resources": [
            (1, "icons_status/application.ico"),
            ] 
        } ],
    
    options = {
        "py2exe": {
            "packages": "encodings", 
            "includes": [
                "pythoncom",
                "anydbm",
                "dbhash",
                "_strptime",
                "iPodderGui",
                "updater",
                "win32gui",
                ],
            "excludes": [ "Tkinter" ],
            }
        },
        
    data_files = [
        (".", ["favorites.txt",
               "gpl.txt",
               "readme.txt"]),
        ("gui", ["gui/iPodder.xrc",]),
        ("win32", ["win32/iPodder.ico",]),
        ("icons_status", ['icons_status/%s' % f
                          for f in os.listdir('icons_status')
                          if f.endswith('.ico') or f.endswith('.png') or f.endswith('.gif')]),
        ("images", ['images/%s' % f
                          for f in os.listdir('images')
                          if f.endswith('.bmp') or f.endswith('.gif') or f.endswith('.png')]),
        ("localization/catalog", ['localization/catalog/%s' % f
                          for f in os.listdir('localization/catalog')
                          if f.endswith('.py')]),
        ("plugins", ['plugins/%s' % f
                          for f in os.listdir('plugins')
                          if f.endswith('.py')]),
        ("compat", ['compat/%s' % f
                          for f in os.listdir('compat')
                          if f.endswith('.py')]),
        ("compat/2x", ['compat/2x/%s' % f
                          for f in os.listdir('compat/2x')
                          if f.endswith('.py')]),
        ("docs", ['docs/JuiceUserGuide.html']),
       ]    
    )

if __name__ == '__main__': 
    setup(**kwargs)
