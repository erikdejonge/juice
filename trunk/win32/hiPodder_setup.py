from distutils.core import setup
import py2exe
import os

kwargs = dict(
    version = "2.1.1",
    description = "Minimal iPodder",
    name = "minpodder",

    # targets to build
    windows = [ {
        "script": "hiPodder.py", 
        "icon_resources": [
            (1, "icons_status/hiPodder.ico"),
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
                "updater",
                "win32gui",
                ],
            }
        },
        
    data_files = [
        (".", ["favorites.txt",
               "gpl.txt",
               "readme.txt"]),
        ("icons_status", ["icons_status/hiPodder.ico",
                          "icons_status/hiPodder_running.ico",
                          ]),
        ]    
    )

if __name__ == '__main__': 
    setup(**kwargs)
