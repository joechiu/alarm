from schedule import *
from runit import *
from db import db
from checkbox import cc
from worker import w
from action import a

SS = c.SS

find = lambda searchList, elem: [[i for i, x in enumerate(searchList) if x == e] for e in elem]

class Main(QTableWidget):
    
    # external declaration for sending worker signal
    scs = pyqtSignal(int)
    
    def __init__(self, parent):
        super(Main, self).__init__(parent)

        # data list
        self.db = db()
        
        self.schedule = Schedule(self)
        self.alarm = parent
        
        self.threadpool = QThreadPool()        
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())                
       
        self.alist = {}
        
        self.n = c.n
        self.COL = c.COL
        self.SIZE = c.SIZE
        
        # data hash
        self.h = []
        self.act = {}
        
        # includes all the actions
        self.pic = {}
        
        self.initIcons()
        
        self.list()
    
    def delete(self, i):
        h = self.h[i]
        print('Length:',len(self.h),self.h)
        if h and self.db.d(h['id']):
            # self.stopWork(i)
            self.removeRow(i)
            del self.h[i]
        print('Length:',len(self.h),self.h)
            
    def id(self, i):
        return self.h[i]['id']
    
    def initIcons(self):       
        t = c.icon.timer
        ic = c.icon.clock
            
        self.pic = {
            'bk': None,
            't0': self.getPx(t), 
            't1': self.getPx(t),
            't2': self.flip(self.getPx(t)),
            'c0': self.getPx(ic),
            'c1': self.getPx(ic, 15),
            'c2': self.getPx(ic, -15),
        }
    def getPx(self, ipath, deg=0):
        pixmap = QPixmap(ipath)
        pixmap = pixmap.scaled(24,24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        px = pixmap.transformed(QTransform().rotate(deg), Qt.SmoothTransformation)
        return px
    def flip(self, px):
        return px.transformed(QTransform().scale(-1, 1))
    
    def ci(self, i):
        
        t = self.h[i]['t']
        if t:
            px = self.pic['t0']
        else:
            px = self.pic['c0']
            
        self.setCellWidget(i, 0, self.cw(px))
            
    # cell widget
    def cw(self, px):
        
        w = QWidget();
        l = QLabel(w);
        if px: l.setPixmap(px)
        layout = QHBoxLayout(w);
        layout.setContentsMargins(0,0,0,0);
        layout.addWidget(l);
        layout.setAlignment( Qt.AlignCenter );
        w.setLayout(layout);
        
        return w
     
    def wiggles(self, i):
        
        anim = self.a.anim(i)
        
        if not anim: return
        
        t = self.h[i]['t']
        if t: pic = 't'
        else: pic = 'c'
        
        self.a.set(i, 'nn', self.a.nn(i) + 1)
        if self.a.nn(i) % 2:
            pic = pic + '1'
            px = self.pic[pic]
        else:
            if anim == 1:
                pic = pic + '2'
                px = self.pic[pic]
            elif anim == 2:
                px = None
            
        self.setCellWidget(i, 0, self.cw(px))
        
    def stopWiggles(self, i):
        self.ci(i)

    def data(self):
        return self.db.list()
    
    def new(self):
        if not self.alist: self.alist = self.data()
        id = self.db.new()
        if id:
            row = len(self.h)
            self.alist.append(self.db.list(id)[0])
            self.add(len(self.alist)-1, 1)
            self.cbck(row, c.T)
            self.schedule.setData(row, 1)
            self.schedule.show()
            return row
        else:
            print("cannot insert new record")
            return -1
        
    def initTable(self):
        
        # setup rows and columns settings for the table
        self.setAcceptDrops(c.T)
        self.setDragEnabled(c.T)
        self.setSelectionBehavior(QTableView.SelectRows)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setDragDropOverwriteMode(c.F)
        self.setDropIndicatorShown(c.F)
        
        self.setColumnCount(self.COL)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.header = self.horizontalHeader()
        self.header.setSectionResizeMode (self.COL-2, QHeaderView.Stretch)
        self.header.setSectionResizeMode (0, QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode (1, QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode (self.COL-1, QHeaderView.ResizeToContents)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.verticalHeader().setStyle(QStyleFactory.create('CleanLooks'))
        self.verticalHeader().hide()
        self.horizontalHeader().hide()

        self.doubleClicked.connect(self.dck)
        self.itemSelectionChanged.connect(self.ck)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setAlternatingRowColors(c.T)
        self.setAttribute(Qt.WA_MacShowFocusRect, c.F)
        
        self.a = a(self)

    def list(self):
        
        self.alist = self.data()
        
        self.initTable()
        
        for i, a in enumerate(self.alist):
            self.add(i)
            
        # focus at the 1st row when initializing
        self.sr()
            
    def add(self, r, new=0):
            
        h = self.alist[r]
        self.h.append(h)
        self.act = {}
        self.alist[r]['act'] = self.act
        
        i = len(self.h)-1
        self.h[i]['act'] = self.act
        print('i=',i,',h=',self.h)
        
        self.a.set(i, 'i', i)
        
        self.insertRow(i)
        self.setColumnWidth(0, self.SIZE)
        self.setRowHeight(i, self.SIZE)
        self.id = h['id']
        
        for j in range(0, self.COL):
            item = QTableWidgetItem()
            if i % 2 == 1:
                item.setBackground(QColor(230, 230, 230))
            self.setItem(i, j, item)

        # counter for countdown
        self.a.set(i, 'cc', None)
        # snooze
        self.a.set(i, 'snz', 0)
        # set audio object
        self.a.set(i, 'sound', None)
        
        # last column checkbox
        cb = cc(h['c'], self.alarm, self, i)
        self.a.set(i, 'cb', cb)
        self.setCellWidget(i, self.COL-1, cb)
        # 1st column
        self.a.set(i, 'nn', 0)
        self.a.set(i, 'anim', 0)
        self.ci(i)
        # 2nd column and threading
        self.a.set(i, 'tt', c.T)
        # timing content
        ct = self.setCT(i)
        # threading tasks
        # self.c.append(ct)
        self.a.set(i, 'ct', ct)
        # 3rd column
        ct = self.getLab(h['name'])
        self.setCellWidget(i, 2, ct)
    
        # reloading table
        self.reloadMenu()
        # focus at the 1st row
        
        h['act'] = self.act
        self.h[i]['act'] = self.act
        # print(self.act)
        # print(self.h[i])
        self.sr(i)
        if not new:
            self.initWork(i)
            self.startWork(i)
        else:
            b = self.a.isit(i)
            print('b=',b)
            if not b:
                self.initWork(i)
                self.startWork(i)
        self.alist[r]['act'] = self.act
            
            
    def initWork(self, i):
        self.a.set(i, 'w', w())
        self.a.w(i).ut.connect(functools.partial(self.updateTimer, i))
        # self.t.append(QThread())
        self.a.set(i, 't', QThread())
        # self.w[i].moveToThread(self.t[i])
        self.a.w(i).moveToThread(self.a.t(i))
        
        
    def startWork(self, i):
        try:
            self.updateTimer(i)
            # dont rely on the action check box
            self.scs.connect(self.a.w(i).startCounting)
            if not self.a.t(i).isRunning():
                print('thread %d started' % i)
                self.scs.emit(i)
                self.a.t(i).start()
            self.scs.disconnect(self.a.w(i).startCounting)
        except Exception as e:
            print("i=",i,"start work crashed...",e)
    def stopWork(self, i):
        print("stopping thread...",self.a.t(i))
        if self.a.t(i).isRunning():
            # self.a.t(i).terminate()
            # print('thread %d terminated' % i)
            self.a.t(i).quit()
            print('thread %d quit' % i)
     
    # critical for updating recent data to the threading, but seems only works 
    @pyqtSlot(int)
    def updateTimer(self, i):
        try:
            h = self.h[i]
            # print('i=',i,'h=',h)
            ct = self.a.ct(i)
            txt = self.HMS(i)
            ct.setText(txt)
            self.wiggles(i)
        except Exception as e:
            if not self.n: print("update timers:",e)
            self.n += 1
    
    def updateData(self, i, h):
        # self.alist[i] = h
        print('up up')
        
    def setCT(self, i):
        h = self.h[i]
        ct = self.getLab(self.HMS(i))
        self.setCellWidget(i, 1, ct)
        return ct
        
    def WD(self, rl):
        lth = len(rl)
        sat = 'Sat'
        sun = 'Sun'
        wdays = "Weekdays"
        wkend = "Weekend"
        txt = ''
        if lth == 7:
            txt = "Everyday"
        elif lth == 2 and sat in rl and sun in rl:
            txt = wkend
        elif lth > 4 and not (sat in rl or sun in rl):
            txt = wdays
        elif lth > 5 and sat in rl and sun not in rl:
            txt += wdays + ', ' + sat
        elif lth > 5 and sun in rl and sat not in rl:
            txt += wdays + ', ' + sun 
        elif sun in rl and sat in rl:
            rl.remove(sat)
            rl.remove(sun)
            txt += self.schedule.R(rl) + ', ' + wkend 
        else:
            txt = self.schedule.R(rl)
        return txt
    
    def timeset(self, i):
        p = self.h[i]
        hh = p['h']
        mm = p['m']
        ss = p['s']
        return (hh,mm,ss)
    
    def dayLists(self, i):
        
        p = self.h[i]
        d = p['d']
        if not d: d = self.today()
        
        wdays = list(calendar.day_abbr)
        today = find(wdays,[self.today()])[0]
        days = find(wdays, list(d.split(', ')))
        
        return wdays, today, days
        
    def dayLoc(self, i, op):
        wdays, today, days = self.dayLists(i)
        idx = -1
        # get today's index 
        for i, d in enumerate(days):
            if op(d, today):
                idx = i
                break
        return idx
    
    def timeBehind(self, i):
        n = dt.now()
        if (n.hour,n.minute,n.second) < self.timeset(i):
            return c.T
        return c.F
        
    def getIdx(self, i):
        
        # 1. if the current time is behind the set time: get the todays -> coming -> prev days idx
        # 2. else get the coming days -> todays -> prvious days idx
        
        # get today's index 
        tidx = self.dayLoc(i, operator.eq)        
        # get the next one if found any
        nidx = self.dayLoc(i, operator.gt)        
        # if not in the today or coming days, find the previous one if found any
        pidx = self.dayLoc(i, operator.lt)        
        
        # current time < setting time
        if self.timeBehind(i):
            if tidx > -1: return tidx
            if nidx > -1: return nidx
        else:
            if nidx > -1: return nidx
            if pidx > -1: return pidx
            if tidx > -1: return tidx
        
        return pidx
            
    def daydiff(self, i):
        
        p = self.h[i]
        (hh, mm, ss) = self.timeset(i)
        
        wdays, today, days = self.dayLists(i)
        
        idx = self.getIdx(i)
        
        diff = 0
        try:
            diff = days[idx][0] - today[0]
        except Exception as e:
            print("day diff:",e)
            
        if diff < 0: diff = diff + len(wdays)
            
        s = dt.today()
        foo = s.replace(hour=hh, minute=mm, second=ss)
        s1 = dt.now()
        s2 = foo + td(days=diff)
        
        return s2-s1       
        
    def sec2hms(self, sec):
        m, s = divmod(sec, 60)
        h, m = divmod(m, 60)
        return (h, m, s)
        
    def timediff(self, i):
        p = self.h[i]
        
        (hh, mm, ss) = self.timeset(i)
        
        diff = self.daydiff(i)
        
        (h, m, s) = self.sec2hms(diff.seconds)
        if diff.days > 0: 
            h += diff.days * 24
        elif diff.days < 0: 
            if p['d']: h += 6 * 24
        
        # print(repr(diff), h, m, s)
        
        l = (h, m, s)
        return self.timeout(i, l)
        
    def tc2hms(self, l):
        (hh, mm, ss) = l
        sec = hh*60*60 + mm*60 + ss - 1
        # print('seconds: ', sec)
        return self.sec2hms(sec)
        
    def countdown(self, i):
        p = self.h[i]
        if self.a.cc(i):
            self.setTime(i, self.tc2hms(self.a.cc(i)))
        else:
            self.setTime(i, self.timeset(i))
        return self.timeout(i, self.a.cc(i))
    
    def knock(self, l):
        (hh, mm, ss) = l
        if hh % 24 == 0 and mm == 0 and ss == 0:
            return c.T
        else:
            return c.F
        
    def msgo(self, id):
        run = runit(id)
        self.threadpool.start(run)
        
    def timeout(self, i, l):
        
        p = self.h[i]
        
        if self.knock(l):
            if p['d']: 
                # if not date checked
                b1 = not self.a.cb(i).isChecked()
                # if not today
                b2 = self.today() not in p['d'].split(', ')
                # ignored if not date checked and not today
                if b1 and b2: return l
            else:
                self.cbck(i, c.F)
            
            if p['t']:
                self.setTime(i, self.timeset(i))
                self.cbck(i, c.F)
                
            self.alarmReset(i)
            
            if p['a']:
                self.stopAudio(i)
                self.initAudio(i, p['aud'])
                self.playAudio(i)
                self.setLoop(i, p['r'])
                self.alarm.trayMsg(c.t.trayAud % (i+1, p['name'], p['aud']))
                if p['msg']: self.msgo(p['id'])
            elif p['msg']:
                self.alarm.trayMsg(c.t.trayMsg % (i+1, p['name'], p['msg']), QIcon(c.icon.msg))
                self.msgo(p['id'])
        
        return l
    
    def alarmReset(self, i):
        self.a.set(i, 'anim', 1)
        self.a.set(i, 'snz', 0)
        self.alarm.stopAct.setEnabled(c.T)
        self.alarm.snoozeAct.setEnabled(c.T)
        self.sr(i)
        
    def today(self):
        FMT = '%a'
        return dt.now().strftime(FMT)            
            
    def setLoop(self, i, r):
        if r:
            self.a.sound(i).setLoops(QSound.Infinite)
            return c.T
        else:
            self.a.sound(i).setLoops(1)
            return c.F
    
    def stopAudio(self, i):
        if self.a.sound(i): self.a.sound(i).stop()

    def playAudio(self, i):
        if self.a.sound(i).isFinished():
            self.a.sound(i).play()
        else:
            self.stopAudio(i)

    def initAudio(self, i, file):
        self.a.set(i, 'sound', QSound(file, self))
    
    def HMS(self, i):
        h = self.h[i]
        cb = self.a.cb(i)

        fmt = c.t.fmt
                
        if self.a.snz(i) > 0:
            if h['t']:
                if cb.isChecked():
                    hms = fmt % self.countdown(i)
                    if h['t']: hms = '<b>-</b>' + hms
                else:
                    hms = fmt % self.timeset(i)
            else:
                if cb.isChecked():
                    hms = fmt % self.countdown(i)
                    if h['t']: hms = '<b>-</b>' + hms
                else:
                    hms = fmt % self.timeset(i)
        else:
            if h['t']:
                if cb.isChecked():
                    hms = fmt % self.countdown(i)
                    if h['t']: hms = '<b>-</b>' + hms
                else:
                    hms = fmt % self.timeset(i)
            else:
                if cb.isChecked():
                    hms = fmt % self.timediff(i)
                else:
                    hms = fmt % self.timeset(i)
                
        rl = []
        if h['d']:
            rl = h['d'].split(', ')
            hms += '<br>%s' % self.WD(rl)
        return hms
    
    def sr(self, r=0):
        self.setFocus()
        self.selectRow(r)
        
    def cbck(self, i, b):
        print("event: ", i, "checked: ", b)
        cb = self.a.cb(i).c
        cb.setChecked(b)
        
    def getLab(self, txt):
        ss = ';'.join(SS)
        f = QFont()
        f.setStyleStrategy(QFont.PreferAntialias)
        lbl = QLabel()
        lbl.setStyleSheet(ss)
        lbl.setFont(f)
        lbl.setWordWrap(c.T)
        lbl.setText(txt)
        return lbl

    def keyPressEvent(self, event):
        key = event.key()
        print(self.alarm.isActiveWindow())
        if key == Qt.Key_Return or key == Qt.Key_Enter:
            self.setFocus()
            if self.selectedItems():
                self.dck(self.selectedItems()[0])
        elif key == Qt.Key_Left:
            print('...')
        elif key == Qt.Key_Right:
            print('......')        
        elif key == Qt.Key_Tab:
            self.alarm.setFocus()
            self.alarm.newAct.setIcon(self.alarm.newHover)
        else:
            super(Main, self).keyPressEvent(event)
        
    def ck(self):
        self.alarm.reset()
        items = self.selectedItems()
        if items:
            try: 
                i = self.currentRow()
                h = self.h[i]
                cb = self.a.cb(i).c
                self.alarm.okAct.setChecked(cb.isChecked())
                hms = "[%02d:%02d:%02d]" % self.timeset(i)
                if h['a']:
                    mode = "Audio: %s" % h['aud']
                else:
                    mode = "Message: "
                msg = "%d. %s %s %s" % ((i+1), hms, mode, h['msg'])
                self.alarm.statusBar().showMessage(msg)
                
                if self.a.anim(i): 
                    self.alarm.stopAct.setEnabled(c.T)
                    self.alarm.snoozeAct.setEnabled(c.T)
                else: 
                    self.alarm.stopAct.setEnabled(c.F)
                    self.alarm.snoozeAct.setEnabled(c.F)
        
                self.alarm.enableAll()
            except Exception as e:
                print('checkbox click error:',e)
            return
        if not len(items):
            self.alarm.enableAll()
            
    def dck(self, idx):
        if not idx: 
            # self.msgBox(c.t.noitem)
            self.alarm.trayMsg(c.t.noitem)
            return
        row = idx.row()
        col = idx.column()
        self.cbck(row, c.T)
        self.schedule.setData(row)
        self.schedule.show()
        i = row
        self.a.set(i, 'anim', 0)
        self.ci(i)
        self.alarm.stopAct.setEnabled(c.F)
        if self.a.sound(i):
            self.stopAudio(i)
        self.alarm.reset()

    def reloadMenu(self):
        self.setVisible(c.F)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)        
        self.resizeColumnsToContents()
        self.setVisible(c.T)
    
    def setTime(self, i, t):
        self.a.set(i, 'cc', t)

    def msgBox(self, msg):
        QMessageBox.about(self, c.t.TITLE, msg)
