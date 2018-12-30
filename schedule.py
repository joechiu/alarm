import calendar, os, glob, sys, time
import operator, functools, threading
from datetime import datetime as dt
from datetime import timedelta as td
from datetime import datetime as dt
from config import *

# repeat WEEKDAY
RL = []

# Column Spans
S = c.S

class timeSpinBox(QSpinBox):
    def __init__(self, *args):
        QSpinBox.__init__(self, *args)
    def textFromValue(self, value):
        return "%02d" % value
   

class Schedule(QDialog):
    
    def __init__(self, parent):
        super(Schedule, self).__init__(parent)

        self.init()
        self.main = parent
        self.initUI()
        self.w = self.width()
        self.h = self.height()

    def init(self):
        self.N = 0
        self.id = 0
        self.idx = None
        self.noLoop = c.noLoop
        self.rgb = Qt.red
        self.rgba = c.rgba
        self.color = c.color
        self.size = c.size
        self.opacity = c.opacity
        self.audio = c.audio
        self.b01 = QPushButton(c.b01.txt)
        self.b01.setCheckable(c.T)
        self.b02 = QPushButton(c.b02.txt)
        self.b02.setCheckable(c.T)
        self.a8 = QPushButton(c.WAVFILE)
        self.a9 = QPushButton(c.t.play)
        self.a10 = QCheckBox()
        self.b12 = QLineEdit()
        self.c12 = QPushButton(c.t.color)
        self.b13 = QSlider(Qt.Horizontal)
        self.b14 = QSlider(Qt.Horizontal)
        self.rp = QLabel(c.t.preview)       
        self.rr = QLabel()
        self.wd = c.WEEKDAY
        self.path = c.WAVPATH
        self.file = c.WAVFILE
        self.alertfile = c.WAVPATH + c.WAVFILE
        self.initAudio()
        self.disableMessage()

    def setB01(self):
        self.b01.setChecked(c.T)
        self.b02.setChecked(c.F)
        i = self.idx
        self.main.h[i]['t'] = 0
        self.main.ci(i)
    def setB02(self):
        self.b01.setChecked(c.F)
        self.b02.setChecked(c.T)
        i = self.idx
        if not self.main.h[i]['t'] == 1:
            self.hh.setValue(0)
            self.mm.setValue(0)
            self.ss.setValue(10)
        self.main.h[i]['t'] = 1
        self.main.ci(i)
        
    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Return or key == Qt.Key_Enter:
            self.close()
            
    def initUI(self):

        grid = QGridLayout(self)
        grid.setSpacing(c.spacing)
        
        n = 0
        style = c.t.formStyle
        # field height
        fh = c.h
        a0 = QLabel(c.t.type)
        self.b01.setFixedHeight(fh)
        self.b01.setStyleSheet(c.b01.style)
        self.b01.setIcon(QIcon(c.icon.clock))
        self.b01.setIconSize(QSize(c.b01.sz,c.b01.sz))
        self.b01.clicked.connect(self.setB01)
        self.b02.setFixedHeight(fh)
        self.b02.setStyleSheet(c.b01.style)
        self.b02.setIcon(QIcon(c.icon.timer))
        self.b02.setIconSize(QSize(c.b02.sz,c.b02.sz))
        self.b02.clicked.connect(self.setB02)
        grid.addWidget(a0, n, 0, 1, 1)
        grid.addWidget(self.b01, n, 1, 1, 4)
        grid.addWidget(self.b02, n, 5, 1, 4)
        
        n += 1        
        a1 = QLabel(c.t.name)
        self.b1 = QLineEdit()
        self.b1.setText(c.t.alarm)
        self.b1.textChanged.connect(self.nameChanged)
        grid.addWidget(a1, n, 0, 1, 1)
        grid.addWidget(self.b1, n, 1, 1, 4)

        now = dt.now()
        n += 1
        a2 = QLabel(c.t.time)
        self.hh = self.spinBox(0,-1,24)
        self.hh.valueChanged.connect(self.setHour)
        self.mm = self.spinBox(0,-1,60)
        self.mm.valueChanged.connect(self.setMin)
        self.ss = self.spinBox(0,-1,60)
        self.ss.valueChanged.connect(self.setSec)
        
        grid.addWidget(a2, n, 0, 1, 1)
        grid.addWidget(self.hh, n, 1, 1, 1)
        grid.addWidget(self.mm, n, 2, 1, 1)
        grid.addWidget(self.ss, n, 3, 1, 1)
        
        n += 1
        self.a3 = QLabel(c.t.once)
        grid.addWidget(self.a3, n, 0, 1, S) 
        
        n += 1
        self.initBox(n, grid)
        
        n += 1
        a6 = QLabel(c.t.alert)
        a6.setStyleSheet(style)
        ss = c.t.ss
        a6.setStyleSheet(ss)
        grid.addWidget(a6, n, 0, 1, 1)
        
        n += 1
        self.a7 = QRadioButton(c.t.sound)
        self.a7.audio = c.T
        self.a7.setChecked(c.T)
        self.a7.toggled.connect(self.setAlert)
        grid.addWidget(self.a7, n, 0, 1, S)
        
        n += 1
        self.a8.clicked.connect(self.setAudio)
        self.a9.clicked.connect(self.playAudio)
        grid.addWidget(self.a8, n, 1, 1, S-1)
        grid.addWidget(self.a9, n, S, 1, 1)
        
        n += 1
        self.a10 = QCheckBox(c.t.repeat)
        self.a10.stateChanged.connect(functools.partial(self.setLoop, self.a10))
        grid.addWidget(self.a10, n, 1, 1, S)

        
        n += 1
        self.a11 = QRadioButton(c.t.message)
        self.a11.audio = c.F
        self.a11.toggled.connect(self.setAlert)
        grid.addWidget(self.a11, n, 0, 1, S)
        
        n += 1
        self.b12.setPlaceholderText(c.t.hint)
        self.b12.textChanged.connect(self.preview)
        self.c12.setToolTip(c.t.colorTip)
        self.c12.clicked.connect(self.setColor)

        grid.addWidget(self.b12, n, 1, 1, S-1)
        grid.addWidget(self.c12, n, S, 1, 1)
        self.showColor()

        n += 1
        self.b13.setMinimum(c.ts.min)
        self.b13.setToolTip(c.ts.tip)
        self.b13.setMaximum(c.ts.max)
        self.b13.setTickPosition(QSlider.TicksBelow)
        self.b13.setTickInterval(c.ts.interval)
        self.b13.valueChanged.connect(self.setSize)

        self.b14.setMinimum(c.to.min)
        self.b14.setToolTip(c.to.tip)
        self.b14.setMaximum(c.to.max)
        self.b14.setTickPosition(QSlider.TicksBelow)
        self.b14.setTickInterval(c.to.interval)
        self.b14.valueChanged.connect(self.setOpacity)

        grid.addWidget(self.b13, n, 1, 1, 4)
        grid.addWidget(self.b14, n, 5, 1, 4)

        n += 1
        q = QPushButton(c.t.done)
        q.clicked.connect(self.close)
        grid.addWidget(q, n, S, 1, 1)

        n += 1
        # label - row of preview
        self.rp.setAlignment(Qt.AlignCenter)
        grid.addWidget(self.rp, n, 0, 1, S)
        self.rp.hide()
        
        # good for troubleshooting
        # n += 1
        # label - row of the result
        # grid.addWidget(self.rr, n, 0, 1, S)
        # self.Result()

        self.setLayout(grid)
        
        self.setWindowTitle(c.t.stitle)    
        # self.setWindowModality(Qt.ApplicationModal)

    def R(self, rl):
        # repeat day list
        w = self.wd.split()
        return ', '.join(sorted(rl, key=w.index))
                
    def updateTime(self, h):
        self.hh.setValue(h['h'])
        self.mm.setValue(h['m'])
        self.ss.setValue(h['s'])
        
    def setData(self, i, new=0):
        
        self.alist = self.main.h
        print("row: %d" % i)
        
        r = self.data = data = self.alist[i]
        print(r)
        
        # handle the data list
        self.idx = i
        self.id = data['id']
        # reserved ct and cb
        self.ct = self.main.a.ct(i)
        self.cb = self.main.a.cb(i)
        self.updateTime(r)
        # handle running counter object
        self.idx = i
        self.b1.setText(r['name'])
        
        self.b14.setValue(r['oc'])
        self.dayBox(r['d'])
        
        if r['aud']:
            self.alertfile = r['aud']
            self.a8.setText(r['aud'])
            self.initAudio()
            print(self.alertfile)
        
        if r['t']:
            self.setB02()
        else:
            self.setB01()
        if r['r']:
            self.a10.setChecked(c.T)
        else:
            self.a10.setChecked(c.F)
            
        if r['a']:
            self.a7.setChecked(c.T)
        else:
            self.a11.setChecked(c.T)
        
        if new:
            t = dt.now()
            self.hh.hide()
            self.hh.setValue(t.hour)
            self.mm.setValue(t.minute)
            self.ss.setValue(t.second-1)
            self.hh.show()
        self.rgba = [int(x) for x in r['rgb'].split(',')[:3]]
        self.rgba.append(r['oc'])
        print(self.rgba)
        self.rgb = QColor(*self.rgba);
            
        self.b12.setText(r['msg'])
        
        self.b13.setValue(r['sz'])
        
        self.seat()
        self.t = QTimer()
        self.t.setSingleShot(c.T)
        self.t.timeout.connect(self.initSize)
        self.t.start(100)
        
    def getDayList(self):
        a = []
        for day in self.wd.split():
            d = getattr(self, day)
            if d.isChecked():
                a.append(day)
        days = ', '.join(a)
        return days
        
    def dayBox(self, dayList):
        self.resetBox()
        if not dayList: return
        for day in dayList.split(', '):
            ckb = getattr(self, day)
            if ckb:
                ckb.setChecked(c.T)
            else:
                ckb.setChecked(c.F)
        
    def resetBox(self):
        for day in self.wd.split():
            ckb = getattr(self, day)
            if ckb:
                ckb.setChecked(c.F)
        
    def initBox(self, n, grid):
        nn = 0
        r4 = [None] * len(self.wd.split())
        for day in self.wd.split():
            setattr(self, day, QCheckBox(day))
            o = getattr(self, day)
            o.setChecked(c.F)
            o.stateChanged.connect(functools.partial(self.foo, o, day))
            grid.addWidget(o, n, nn, 1, 1)
            nn += 1
        
    def preview(self):
        txt = self.b12.text().split(' ', 1)[0]
        n = 10
        if len(txt) > n: txt = txt[:n] + '...'
        self.rp.setText(txt)
        # self.rp.setText('Text')
        
    def showColor(self):
        l = list(self.rgba);
        self.rgba[3] = self.opacity
        ss = "color:rgba(%d,%d,%d,%d%%);" % tuple(self.rgba)
        ss += "font-size: %dpx;" % self.size
        self.rp.setStyleSheet(ss)

    def rgb2int(self, t):
        # tuple to list
        f2i = self.f2i
        return [f2i(t[0]), f2i(t[1]), f2i(t[2]), t[3]]
    
    def f2i(self, f):
        # print(f)
        return int(f*255)
    
    def setColor(self):
        col = QColorDialog.getColor(self.rgb, self)
        if col.isValid():
            self.rgba = self.rgb2int(col.getRgbF())
            self.rgb = col
            self.data['rgb'] = ','.join(str(x) for x in self.rgba)
            self.showColor()
        self.Result()

    def setSize(self):
        self.size = self.b13.value()
        self.showColor()
        self.Result()

    def setOpacity(self):
        self.opacity = self.b14.value()
        self.showColor()
        self.Result()

    def disableAudio(self):
        self.a8.setDisabled(c.T)
        self.a9.setDisabled(c.T)

    def disableMessage(self):
        self.b12.setDisabled(c.T)
        self.c12.setDisabled(c.T)

    def enableAudio(self):
        self.a8.setEnabled(c.T)
        self.a9.setEnabled(c.T)
        self.rp.hide()

    def enableMessage(self):
        self.b12.setEnabled(c.T)
        self.c12.setEnabled(c.T)
        self.rp.show()

    def close(self):
        self.stopAudio()
        self.data = self.getData()
        # self.main.updateData(self.idx, self.data)
        print(self.main.db.u(self.data))
        self.updateWorker()
        self.main.reloadMenu()
        # self.main.cbck(self.idx, c.T)
        self.hide()

    def getData(self):
        if not (self.b12.text() or self.a7.isChecked()):
            self.b12.setText("Alarm Message")
        data = {
            'id': self.data['id'],
            'name': self.b1.text(),
            'h': self.hh.value(),
            'm': self.mm.value(),
            's': self.ss.value(),
            't': self.b02.isChecked(), # reserved for timer / alarm option
            'a': int(self.a7.isChecked()),
            'r': int(self.a10.isChecked()),
            'd': self.getDayList(),
            'c': self.data['c'],
            'aud': self.alertfile,
            'msg': self.b12.text(),
            'rgb': self.data['rgb'],
            'sz': self.b13.value(),
            'oc': self.b14.value(),
        }
        return data
        
    def setAlert(self):
        self.stopAudio()
        r = self.sender()
        if r.isChecked():
            self.audio = r.audio
            if r.audio:
                self.enableAudio()
                self.disableMessage()
            else:
                self.enableMessage()
                self.disableAudio()
            self.Result()

    def foo(self, cc, d):
        msg = ''
        if cc.isChecked():
            RL.append(d)
            msg = "Repeat: %s" % self.R(RL)
        else:
            RL.remove(d)
            if len(RL) < 1:
                msg = c.t.once
            else:
                msg = "Repeat: %s" % self.R(RL)
        print(msg)
        self.a3.setText(msg)
        self.data['d'] = self.R(RL)
        self.Result()
        self.timeChanged()

    def setLoop(self, cc):
        self.a10 = cc
        if cc.isChecked():
            self.sound.setLoops(QSound.Infinite)
            if not self.sound.isFinished():
                self.a9.setText("Stop")
            return c.T
        else:
            self.sound.setLoops(1)
            if not self.sound.isFinished():
                self.a9.setText("Play")
            return c.F

    def stopAudio(self):
        self.a9.setText("Play")
        self.sound.stop()

    def playAudio(self):
        if self.sound.isFinished():
            self.sound.play()
        else:
            self.stopAudio()
        self.setLoop(self.a10)

    def initAudio(self):
        self.sound = QSound(self.alertfile, self)
        self.path, self.file = os.path.split(self.alertfile)
        self.a8.setText(self.file)

    def setAudio(self):
        self.stopAudio()
        fname = QFileDialog.getOpenFileName(
            self, 'Open file', self.path,"Audio files (*.wav);;All files (*.*)"
        )
        
        if fname[0]:
            self.alertfile = fname[0]
        else:
            self.alertfile = "%s/%s" % (self.path, self.file)

        print(self.alertfile)
        self.initAudio()            
        self.a9.setText("Play")
     
    def updateWorker(self):
        i = self.idx
        self.updata()
        # self.main.stopWork(i)
        self.main.startWork(i)
        
    def updata(self):
        e = ('name', 'h', 'm', 's', 'd', 'c', 'r', 'a', 't', 'aud', 'msg', 'rgb', 'sz', 'oc')
        for f in e:
            self.main.h[self.idx][f] = self.data[f]
            
    def loop(self, sb):
        if sb.value() >= sb.maximum():
            if self.noLoop:
                sb.setValue(sb.maximum()-1)
                return sb
            sb.setValue(sb.minimum()+1)
        if sb.value() <= sb.minimum():
            if self.noLoop:
                sb.setValue(sb.minimum()+1)
                return sb
            sb.setValue(sb.maximum()-1)
        return sb
    def setHour(self):
        self.hh = self.loop(self.hh)
        self.data['h'] = self.hh.value()
        self.timeChanged()
    def setMin(self):
        self.mm = self.loop(self.mm)
        self.data['m'] = self.mm.value()
        self.timeChanged()
    def setSec(self):
        self.ss = self.loop(self.ss)
        self.data['s'] = self.ss.value()
        self.timeChanged()
    def timeChanged(self):
        # print("time changed: %s:%s:%s" % (self.data['h'],self.data['m'],self.data['s']))
        self.updateWorker()
        self.main.reloadMenu()
        self.main.setTime(self.idx, self.main.timeset(self.idx))
        self.Result()
        
    def nameChanged(self):
        lbl = self.main.getLab(self.b1.text())
        self.main.setCellWidget(self.idx, 2, lbl)        
        self.main.reloadMenu()
        
    def closeEvent(self, e):
        print("window closing................")
        self.stopAudio()
        # self.setData(self.idx)
        self.updateWorker()
        self.main.reloadMenu()
        self.Result()
    
    def Result(self):
        self.a3.hide()
        msg = "%02d:%02d:%02d " % (self.hh.value(), self.mm.value(), self.ss.value())
        msg += self.R(RL) + " - "
        msg += "Audio" if self.audio else self.b12.text()
        msg += " - (%d,%d,%d,%d%%)" % tuple(self.rgba)
        msg += " - %d" % self.size
        self.a3.show()
        # self.rr.setText(msg)
        
    def spinBox(self, v, min, max):
        sb = timeSpinBox()
        sb.setAccelerated(c.T)
        sb.setRange(min, max)
        sb.setSingleStep(1)
        sb.setValue(v)
        return sb

    def seat(self):
        p = QApplication.desktop().cursor().pos()
        # x = p.x() + self.main.width() / 3 
        # y = p.y() - (self.main.height()+self.height())/len(self.main.h)
        self.initSize()
        self.move(p.x(), p.y())        
        
    def initSize(self):
        self.resize(self.w,self.h)
