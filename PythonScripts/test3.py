import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

class LoadGif(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.lable = QLabel('',self)
        self.setFixedSize(658,494)
        self.setWindowFlags(Qt.WindowFullscreenButtonHint)
        self.movie = QMovie('./images/test.gif')
        self.lable.setMovie(self.movie)
        self.movie.start()

app = QApplication.instance()
if app is None:
    # this must excu or will crash
    app = QApplication(sys.argv)
test = LoadGif()
test.show()
sys.exit(app.exec_())