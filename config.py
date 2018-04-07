"""
config class which contains the configurable settings for classes
"""
from PyQt5.QtMultimedia import QSound
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class b01:
    txt = "Alarm Clock"
    # image size
    sz = 24
    style = "font-weight:bold;color:#333;font-size:12px;padding-top:3px"
class b02:
    txt = "Timer"
    # image size
    sz = 26
    style = b01.style
class ts:
    min = 20
    tip = "Change text size"
    max = 108
    interval = 10
class to:
    min = 10
    tip = "Change text opacity"
    max = 100
    interval = 10
class pc:    
    PATH = QDir.currentPath()
    
class icon:
    # toolbar menu
    new = pc.PATH + '/images/new.svg'
    edit = pc.PATH + '/images/edit.svg'
    delete = pc.PATH + '/images/delete.svg'
    ok = pc.PATH + '/images/ok.svg'
    stop = pc.PATH + '/images/stop.svg'
    snooze = pc.PATH + '/images/sleep.svg'
    exit = pc.PATH + '/images/exit.svg'
    # menu, schedule
    timer = "images/alarm-timer.png"
    clock = "images/alarm-clock.png"
    
class t:
    # alarm tool bar
    TITLE = 'Alarm Clock'
    clock = "Clock"
    # clock font size
    cfsize = 16
    style = "color:white;font-family:arial;font-size:%dpx;font-weight:bold;" % cfsize
    new = "Create a new file"
    edit = "Edit existing alarm"
    delete = "Delete the selected alarm"
    ok = "Enable/Disable the selected alarm"
    stop = "Stop this alarm"
    snooze = "Snooze the selected alarm"
    exit = "Exit the schedule menu"
    icon = 'icon.ico'
    snzStat = ' by 1 minute - click ALT key to change'
    # system tray
    show = "Open Alarm Clock"
    hide = "Minimize Application to Tray"
    quit = "Exit"
    traytitle = TITLE
    trayAud = "Alarm %d: '%s' audio alarm is triggered"
    trayMsg = "Alarm %d: '%s' message alarm is triggered"
    close = "Alarm Clock was minimized to Tray"
    tools = "Tools"
    ready = "Ready"
    increment = 'increment'
    decrement = 'decrement'
    nochange = ''
    
    # menu
    fmt = "<b>%02d:%02d<font size=-1>:%02d</font></b>\n"
    noitem = "No itmes selected"
    
    # schedule
    play = "Play"
    color = 'Set Color'
    preview = "TEXT"       
    weekday = 'Mon Tue Wed Thu Fri Sat Sun'
    wavpath = "/sounds/"
    wavfile = "notify.wav"
    # schedule font size
    sfsize = 12
    formStyle = "font-weight:bold;color:#333;font-size:%dpx" % sfsize
    type = 'Type:'
    name = 'Name:'
    alarm = "Alarm!"
    time = 'Time:'
    once = 'Repeat: Once'
    alert = "Alert"
    ss = "font-weight:bold"
    sound = "Play sound"
    repeat = "Repeat sound"
    message = "Show message"
    hint = "Alarm Message"
    colorTip = 'Opens color palette'
    done = "Done"
    stitle = 'Alarm Clock Schedule'

class c:
    T = True
    F = False
    
    # toolbar
    PATH = pc.PATH
    W = 380
    H = 224
    
    # clock location
    colw = 270  # column width
    rgap = 72   # gap to right 
    
    pos = 'new'
    alt = F
    movable = F
    
    # system tray
    t = t
    
    # menu font size
    mfsize = 12
    # menu style
    SS = [
        "margin-right:6px",
        "margin-left:6px",
        "color:#333",
        "font-family:Georgia,Arial",
        "font-size:%dpx" % mfsize,
        "outline:0",
    ]
    n = 0
    COL = 4
    SIZE = 42
    IMG = {
        "timer":"images/alarm-timer.png",
        "clock":"images/alarm-clock.png",
    }
    icon = icon
    
    # schedule
    S = 8
    
    noLoop = T
    rgba = [85,0,0,0]
    color = '255,255,0'
    size = 24
    opacity = 100
    audio = T
    
    b01 = b01
    b02 = b02
    
    spacing = 10
    h = 36
    # text size
    ts = ts
    # text opacity
    to = to
    
    WEEKDAY = t.weekday
    WAVPATH = PATH + t.wavpath
    WAVFILE = t.wavfile
    
