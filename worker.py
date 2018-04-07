"""
worker class which handles the signal to and from the slot
"""
import sys
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot

class w(QThread):
    # explicit signal sent in the startCounting function
    ut = pyqtSignal(int)
    
    # explicit slot that takes input from the scs
    @pyqtSlot(int)
    def startCounting(self, i):
        while True:
            self.ut.emit(i)
            QThread.sleep(1)

