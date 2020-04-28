import sys
from MainWindow import MainWindow
from PyQt5.QtWidgets import *

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    win = MainWindow('대성에너지')
    win.show()
    sys.exit(app.exec_())