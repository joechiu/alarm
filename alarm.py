#!/usr/bin/env python

from menu import *

class Alarm(QMainWindow):
    
    def __init__(self, parent=None):
        super(Alarm, self).__init__(parent)

        # icon control specs
        self.ics = {
            'new':  { 'p': c.icon.new,  'f': "&New",  't': self.new,  'm': c.t.new, 's': QKeySequence.New, 'e': c.T, 'c': c.F },
            'edit': { 'p': c.icon.edit, 'f': "&Edit", 't': self.edit, 'm': c.t.edit, 's': "", 'e': c.F, 'c': c.F },
            'delete': { 'p': c.icon.delete, 'f': "&Delete", 't': self.delete, 'm': c.t.delete, 's': "", 'e': c.F, 'c': c.F },
            'ok':   { 'p': c.icon.ok, 'f': "&Ok",   't': self.ok, 'm': c.t.ok, 's': "", 'e': c.F, 'c': c.T },
            'stop': { 'p': c.icon.stop, 'f': "&Stop", 't': self.stop, 'm': c.t.stop, 's': QKeySequence.Cancel, 'e': c.F, 'c': c.F },
            'snooze': { 'p': c.icon.snooze, 'f': "&Snooze", 't': self.snooze, 'm': c.t.snooze, 's': "", 'e': c.F, 'c': c.F },
            'exit': { 'p': c.icon.exit,'f': "&Exit", 't': self.close,'m': c.t.exit, 's': "Ctrl+Q", 'e': c.T, 'c': c.F },
        }
        
        self.createActions()
        self.createToolBars()
        self.createStatusBar()
        self.pos = c.pos
        self.alt = c.alt
        self.clock = QLabel(c.t.clock, self)
        
        self.am = Menu(self)
        self.schedule = self.am.schedule
        self.setCentralWidget(self.am)
        self.setMinimumSize(QSize(c.W, c.H))
        self.setWindowTitle(c.t.TITLE)
        self.toolBar.setMovable(c.movable)
        self.clock.setText(self.now())
        self.clock.setStyleSheet(
            c.t.style
        )
        # QT built in attribute seems not able to align the text to right even populate the following setting
        # self.clock.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.clock.setAlignment(Qt.AlignVCenter)
        self.t = QTimer()
        self.t.setSingleShot(c.F)
        self.t.timeout.connect(self.timer)
        self.t.start(1000)
        
        self.systray()
        
        self.setWindowIcon(QIcon(c.t.icon))
    
    def systray(self):
        # Init QSystemTrayIcon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(c.t.icon))
        self.tray_icon.activated.connect(self.tray_icon_clicked)        
        show_action = QAction(QIcon(c.icon.ok), c.t.show, self)
        hide_action = QAction(QIcon(c.icon.stop), c.t.hide, self)
        quit_action = QAction(QIcon(c.icon.exit), c.t.quit, self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(self.close)
        self.tray_menu = QMenu()
        self.tray_menu.addAction(show_action)
        self.tray_menu.addAction(hide_action)
        self.tray_menu.addSeparator()
        self.tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.setToolTip(c.t.traytitle)
        self.tray_icon.show()
        
    def tray_icon_clicked(self):
        if not self.tray_menu.isVisible(): 
            if self.isVisible():
                self.hide()
            else:
                self.show()
                
    def timer(self):
        if self.width() > c.colw:
            self.clock.move(self.width()-c.rgap, 0)        
            self.clock.setText(self.now())
        else:
            self.clock.setText('')
        
    def resizeEvent(self, e):
        self.timer()
        
    def now(self):
        FMT = '%T'
        s1 = dt.now().strftime(FMT)
        return s1
        
    def act(self, k):
        return getattr(self, k+'Act')
    def setNormalIcon(self, k):
        act = self.act(k)
        ico = getattr(self, k+'Normal')
        act.setIcon(ico)
        
    def enableAll(self, b=c.T):
        for k in self.ics:
            act = getattr(self, k+'Act')
            exceptions = (
                'new',
                'stop',
                'snooze',
                'exit'
            )
            if not k in exceptions:
                act.setEnabled(b)
        
    def reset(self, b=c.F):
        if b: 
            self.pos = 'new'
        for k in self.ics:
            self.setNormalIcon(k)
        
    def prevAct(self, k):
        foo = self.ics
        i = list(foo.keys()).index(k)
        try:
            list(foo.keys())[i - 1]
        except:
            i = 1
        h = foo[list(foo.keys())[i - 1]]
        k = list(foo.keys())[i - 1]
        return k, h

    def chkPrev(self, k):
        self.reset()
        kk, h = self.prevAct(k)
        act = getattr(self, kk+'Act')
        if not act.isEnabled():
            self.chkNext(kk)
            return
        self.pos = kk
        ico = getattr(self, kk+"Hover")        
        act.setIcon(ico)

    def nextAct(self, k):
        foo = self.ics
        i = list(foo.keys()).index(k)
        try:
            list(foo.keys())[i + 1]
        except:
            i = -1
        h = foo[list(foo.keys())[i + 1]]
        k = list(foo.keys())[i + 1]
        return k, h

    def chkNext(self, k):
        self.reset()
        kk, h = self.nextAct(k)
        act = getattr(self, kk+'Act')
        if not act.isEnabled():
            self.chkNext(kk)
            return
        self.pos = kk
        ico = getattr(self, kk+"Hover")        
        act.setIcon(ico)

    def keyReleaseEvent(self, e):
        key = e.key()
    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Return or key == Qt.Key_Enter:
            act = getattr(self, self.pos+'Act')
            act.trigger()
            self.setFocus()
        elif key == Qt.Key_Left:
            self.chkPrev(self.pos)
        elif key == Qt.Key_Right:
            self.chkNext(self.pos)
        elif key == Qt.Key_Alt:
            # increment / decrement switch 
            self.alt = not self.alt
        else:
            print("end of items")
            # super(ToolBar, self).keyPressEvent(event)
    
    def event(self, event):
        if (event.type()==QEvent.KeyPress) and (event.key()==Qt.Key_Tab):
            self.am.setFocus()
            self.reset(c.T)
            return c.T
        return QMainWindow.event(self, event)
    
    def createActions(self):

        for k in self.ics:
            kk = k + 'Act'
            h = self.ics[k]
            pix = self.ccb(h['p'])
            ico = QIcon(pix)
            setattr(self, k+"Hover", ico)
            ico = QIcon(h['p'])
            setattr(self, k+"Normal", ico)
            vv = QAction(
                ico, h['f'], self, shortcut=h['s'], statusTip=h['m'], 
                triggered=h['t'], enabled=h['e'], checkable=h['c']
            )
            vv.setToolTip(h['m'])
            setattr(self, kk, vv)
            
    # create color button
    def ccb(self, img, w=80, h=80):
        pix = QPixmap(img)
        p = QPainter(pix)
        p.setRenderHint(QPainter.Antialiasing)
        p.setBrush(QColor(0,0,255,40))
        pen = QPen(Qt.transparent, 1);
        p.setPen(pen)
        p.drawRect(0, 0, w, h)
        p.end()
        return pix
                
    def new(self):
        if self.schedule.isVisible():
            return
        self.pos = 'new'
        self.reset()
        self.setNormalIcon('new')
        # insert a new record
        row = self.am.new()
        self.reset()
        
    def edit(self):
        self.pos = 'edit'
        self.reset()
        if self.am.selectedItems():
            self.am.dck(self.am.selectedItems()[0])
            
    def delete(self):
        self.pos = 'edit'
        self.reset()
        if self.am.selectedItems():
            i = self.am.currentRow()
            self.stop()
            self.am.delete(i)
            if not self.am.selectedItems():
                self.enableAll(c.F)
        else:
            print("no alarm selected")
            
    def ok(self):
        self.pos = 'ok'
        self.reset()
        if self.am.selectedItems():
            i = self.am.currentRow()
            self.am.cbck(i, self.okAct.isChecked())
            
    def stop(self):
        if self.am.selectedItems():
            i = self.am.currentRow()
            self.am.a.set(i, 'anim', 0)
            self.am.a.set(i, 'snz', 0)
            self.am.ci(i)
            self.am.a.set(i, 'cc', None)
            self.stopAct.setEnabled(c.F)
            self.snoozeAct.setEnabled(c.F)
            # stop process if it's a timer
            timer = self.am.h[i]['t']
            if timer: self.am.cbck(i, 0)
            if self.am.a.sound(i):
                self.am.stopAudio(i)
        self.pos = 'stop'
        self.reset()

    def msg(self):
        if self.alt: snz = -1
        else: snz = 1
        if snz > 0: msg = c.t.increment
        else : msg = c.t.decrement
        return snz, msg
    
    def snooze(self):
        snz, msg = self.msg()
        self.statusBar().showMessage(msg + c.t.snzStat)
        if self.am.selectedItems():
            i = self.am.currentRow()
            s = self.am.a.snz(i) + snz
            self.am.a.set(i, 'snz', s)
            if self.am.a.snz(i) < 1: self.am.a.set(i, 'snz', 1)
            self.am.a.set(i, 'anim', 2)
            self.am.a.set(i, 'cc', (0, self.am.a.snz(i), 1))
            self.am.updateTimer(i)
            self.am.cbck(i, c.T)
            if self.am.a.sound(i):
                self.am.stopAudio(i)
        
    def createToolBars(self):
        self.toolBar = self.addToolBar(c.t.tools)
        for k in self.ics:
            kk = k + 'Act'
            self.toolBar.addAction(getattr(self, kk))
        
    def createStatusBar(self):
        self.statusBar().showMessage(c.t.ready)

    def close(self):
        self.t.stop()
        sys.exit()
        
    def closeEvent(self, e):
        e.ignore()
        self.trayMsg(c.t.close)
        self.hide()
    
    def trayMsg(self, msg, img=None):
        if not img: img = QIcon(c.icon.app)
        # img = QSystemTrayIcon.Information
        t = 1000 
        self.tray_icon.showMessage(
            c.t.traytitle,
            msg,
            img,
            t
        )
      
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    tb = Alarm()
    tb.show()
    sys.exit(app.exec_())    
    