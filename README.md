# Python pyqt5 alarm clock Widget

QT5 Alarm Clock Widget is a portable fully-featured alarm clock for the Windows panel or Linux OS by python QT5. It's easy to use yet powerful with the supports of multiple repeatable alarms, customized snoozing and flexible notification features.

## Synopsis

Alarm clock is an alarm management widget. It's handy to create alrams of clock or timer style. 

## Code

The widget is written by Python 3.6.2 and tested by Windows 7. 

## Prerequisition Installation

The PyQT5 bundled with Python 3.x so you need to check the python version before install the QT5 libraries. 

Please be advised you probably need to check your system type to download/install the right python. For example, this clock widget is compiled by 64  bit system and yet for x86.

To check the python version, open the terminal or cmd and type pythone or python --version to see the python version before compile the clock widget.

$ python --version
Python 3.6.2

C:\>python (in windows)
Python 3.6.2 (v3.6.2:5fd33b5, Mar  8 2017, 04:57:36) [MSC v.1900 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>>

## Installation

In order to run this widget you are recommended to search the following systems/utilities/tools existence in your system or install them beforehand if not.

* Linux Ubuntu 16.04 / OS2 / Windows 7
* Python 3.6.2
* PyQT5
* pip
* cx_Freeze
* Python IDE, eg. Wings, PyCharm, Vim... (optional)
* Inno Setup (optional) 

## Test and Run (Windows)

EXE pack:
1. copy the codes to your local directory 
2. change diretory to your local directory
3. under the directory type: 
   python setup.py build
4. when the compile command fired, cx_Freeze will follow the schema in setup.py to build an executable file inside build/exe.win-amd64-3.6
5. run the compiled file alarm.exe inside the exe directory to see the alarm clock widget

MSI pack:
1. run the following command to pack as a msi:
    python setup.py bdist_msi
2. Analog alarm-0.2-amd64.msi will be generated in the dist folder
3. You're probably interested to customize the msi installation by this topic: 
   https://stackoverflow.com/questions/17307934/creating-msi-with-cx-freeze-and-bdist-msi-for-pyside-app

Note: you also can pack the files as a installer by Inno setup if you are interested. see http://www.jrsoftware.org/isinfo.php for more information.

## Snapshots

* alarm and sleep function demo<br>
![running alarm](https://github.com/joechiu/alarm/blob/master/images/1522993859927.gif?raw=true "alarm and sleep function demo")

* schedule setting demo<br>
![schedule](https://github.com/joechiu/alarm/blob/master/images/1522995021335.gif?raw=true "schedule setting demo")

## Contributors

You are free to update these tools to make them more helpful.

## License

A short snippet describing the license (MIT, Apache, etc.)
