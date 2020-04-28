import os
import sys
from PyQt5.QtWidgets import *
# from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import Constants

# sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

class InfoWindow(QDialog):
    def __init__(self, parent=None, company=None):
        super().__init__()
        # self.setWindowModality(Qt.NonModal)  # to set non-modal dialog
        if company:
            self._company = company
        else:
            self._company = 'DEMO'

        if parent:
            self._parent = parent
            self._company = parent._company
        else:
            self._parent = None

        self.initUI()

    # def __init__(self, parent=None):
    #     super().__init__(parent)
    #     self.setWindowModality(Qt.NonModal)     # to set non-modal dialog
    #     self.initUI()

    def initUI(self):
        self.setWindowTitle(self._company + ' - ' + '시스템정보')
        # self.setWindowIcon(QIcon('../img/daesung.ico'))
        self.setWindowIcon(QIcon(Constants.BASE_PATH + '/img/daesung.ico'))
        winLayout = QVBoxLayout()
        lable = QLabel('ITRM - IT Resource Mananger')
        tb = QTextBrowser()
        winLayout.addWidget(lable)
        winLayout.addWidget(tb)
        self.setLayout(winLayout)

        htmlText = '<p style="color: red">개발중</p> \n' \
                   '<p style="font-size: 13px">대성에너지 자산관리시스템</p>'
        tb.append(htmlText)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = InfoWindow(None, '대성에너지')
    # w = InfoWindow()
    w.show()
    sys.exit(app.exec_())