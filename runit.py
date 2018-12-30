import os, time, subprocess
from PyQt5.QtCore import QRunnable, pyqtSlot

DEV = True
if os.path.exists('python36.dll'):
    DEV = False

class runit(QRunnable):    
    def __init__(self, rid):
        super(runit, self).__init__()
        self.id = str(rid)
        
    @pyqtSlot()
    def run(self):
        print("Thread start - " + self.id) 
        
        if DEV:
            cmd = [ "python", "message.py", self.id ]
        else:
            cmd = [ "message.exe", self.id ]
            
        subprocess.call(cmd)
        time.sleep(5)
        print("Thread complete - " + self.id)

