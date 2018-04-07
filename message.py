#!/usr/bin/python3

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPainter, QPolygon, QIcon, QFont
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QDesktopWidget
from db import db

class MessageBox(QWidget):
    
    def __init__(self, rid):
        super().__init__()
        
        self.db = db()
        r = self.db.list(rid)[0]
        msg = r['msg']
        print(r)
        size = str(r['sz'])
        rgba = r['rgb'].split(',')[:3]
        rgba.append(str(r['oc']))        
        print("color: rgba("+','.join(rgba)+"%)")
        
        if not msg:
            msg = "Unknow"
            
        b = QPushButton(msg, self)
        b.clicked.connect(self.todo)
        b.resize(1200, 150)
        sa = [
            "background-color: rgba(255, 255, 255, 1%)",
            "font-size: "+size+"px",
            "color: rgba("+','.join(rgba)+"%)",
        ]
        print(sa)
        ss = ';'.join(sa)
        b.setStyleSheet( ss )
        
        self.setWindowIcon(QIcon('message.ico'))
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
    
        self.move(QApplication.desktop().screen().rect().center()- b.rect().center())
        # self.center(b)
        self.show()
        
    def center(self, b):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center() - b.rect().center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())        
    
    def todo(self):
        sys.exit()
        
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            sys.exit()
            
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    
    try:
        if len(sys.argv) > 1:
            print(sys.argv[1])
            ex = MessageBox(sys.argv[1])
        else:
            ex = MessageBox("Unknown")
    except Exception as e:
        print("Error: ", str(e))
        
    sys.exit(app.exec_())    
    