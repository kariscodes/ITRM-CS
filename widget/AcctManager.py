import os
import sys
from PyQt5.QtWidgets import *
# from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import Constants

class AcctWindow(QWidget):
    def __init__(self, parent=None, company=None):
        super().__init__()
        if company:
            self._company = company
        else:
            self._company = 'DEMO'

        if parent:
            self._parent = parent
            self._company = parent._company
        else:
            self._parent = None
        # self.setWindowModality(Qt.NonModal)  # to set non-modal dialog
        self.initUI()

    # def __init__(self, parent=None):
    #     super().__init__(parent)
    #     self.setWindowModality(Qt.NonModal)     # to set non-modal dialog
    #     self.initUI()

    def initUI(self):
        self.setWindowTitle(self._company + ' - ' + '자산취득등록')
        self.setWindowIcon(QIcon(Constants.BASE_PATH + '/img/daesung.ico'))
        # self.baseSize()
        # self.setGeometry(100, 100, 500, 300)
        winLayout = QVBoxLayout()
        lable = QLabel('자산취득등록 화면')
        text = QTextEdit()
        winLayout.addWidget(lable)
        winLayout.addWidget(text)
        self.setLayout(winLayout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = AcctWindow(None, '대성에너지')
    w.show()
    sys.exit(app.exec_())