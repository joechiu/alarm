import time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# centrial aligned checkbox
class cc(QWidget):
    def __init__(self, *args):
        super().__init__()
        
        ck = args[0]
        self.menu = args[1]
        self.am = args[2]
        self.row = args[3]
        self.i= args[3]
        self.c = QCheckBox()
        if ck:
            self.c.setChecked(True)
        else:
            self.c.setChecked(False)
            
        self.c.stateChanged.connect(self.cck)
        p = QHBoxLayout(self)
        p.addWidget(self.c)
        p.setAlignment(Qt.AlignCenter)
        p.setContentsMargins(0,0,0,0)
        self.setLayout(p)
    
    def cck(self):
        i = self.i
        # try the existence
        try:
            h = self.am.h[i]
        except:
            i = self.am.currentRow()
            h = self.am.h[i]
        self.am.sr(i)
        self.menu.okAct.setChecked(self.c.isChecked())
        if self.c.isChecked():
            c = 1
            print("row %d checked" % i)
        else:
            c = 0
            self.am.a.set(i, 'snz', 0)
            print("row %d un-checked" % i)
        self.am.db.c(h['id'], c)
        # if not h['t']: self.am.db.c(h['id'], c)
            
    def isChecked(self):
        try:
            if self.c.isChecked():
                return True
            else:
                return False
        except:
            print("invalid checkbox")
            return 'invalid'

    def status(self):
        FMT = '%H:%M:%S'
        s = dt.now().strftime(FMT)            
        ws = self.c.checkState()
        print(ws)
        d = str(0)
        if self.c.isChecked():
            print("%d. %s: row checked( %s )" % (self.row, s, d))
            return True
        else:
            print("%d. %s: row un-checked( %s )" % (self.row, s, d))
            return False
