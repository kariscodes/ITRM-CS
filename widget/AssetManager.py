import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

from widget import CommonWidget, ItemComputerManager, ItemMonitorManager

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import Constants

class AssetWindow(QWidget):
    def __init__(self, parent=None, company=None):
        super().__init__(parent)
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

    def initUI(self):
        self.setWindowTitle(self._company + ' - ' + '전산자원등록')
        self.setWindowIcon(QIcon(Constants.BASE_PATH + '/img/daesung.ico'))
        self.resize(1000, 650)

        titleLayout = CommonWidget.TitleLayout('전산자원등록')

        self._msgLabel = QLabel()
        self._msgLabel.setText('전산자원등록 화면입니다.')
        msgLayout = QVBoxLayout()
        msgLayout.addWidget(self._msgLabel)
        msgFrame = QFrame()
        msgFrame.setFixedHeight(35)
        msgFrame.setLayout(msgLayout)

        tabWindow = QTabWidget()
        itemComputerWindow = ItemComputerManager.ItemComputerWindow()
        itemMonitorWindow = ItemMonitorManager.ItemMonitorWindow()
        tabWindow.addTab(itemComputerWindow, '컴퓨터')
        tabWindow.addTab(itemMonitorWindow, '모니터')
        tabWindow.addTab(QWidget(), '프린터')

        winLayout = QVBoxLayout()
        winLayout.addLayout(titleLayout)
        winLayout.addWidget(msgFrame)
        winLayout.addWidget(tabWindow)

        self.setLayout(winLayout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    w = AssetWindow(None, '대성에너지')
    w.show()
    sys.exit(app.exec_())