import sys
import os.path
from setuptools import find_packages
from cx_Freeze import setup, Executable

base = None

if sys.platform == 'win32':
    base = 'Win32GUI'

executables = [
    Executable(
        'alarm.py',
        base=base, 
        icon="icon.ico"
    ),
    Executable(
        'message.py',
        base=base, 
        icon="message.ico"
    )
]


options = {
    'build_exe': {
        'include_files':[
            "icon.ico",
            "message.ico",
            ("bak", "bak"),
            ("images", "images"),
            ("sounds", "sounds"),
        ],
    },
}

setup(
    name="Clock Alarm",
    version="2018-02",
    description="QT5 Clock Alarm Widget",
    options=options,
    executables=executables
)
