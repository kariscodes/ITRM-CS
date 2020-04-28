import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QKeyEvent, QKeySequence

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import Constants

class AssetItemCreatorWindow(QDialog):
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
        self.setWindowModality(Qt.NonModal)     # to set non-modal dialog
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self._company + ' - ' + 'Multi Items Creator Window')
        self.setWindowIcon(QIcon(Constants.BASE_PATH + '/img/daesung.ico'))

        serialNumBox = QGroupBox('일련번호')
        serialNumLayout = QVBoxLayout()
        self._serialNumItem = QLineEdit()
        self._serialNumList = QListWidget()
        serialNumLayout.addWidget(self._serialNumItem)
        serialNumLayout.addWidget(self._serialNumList)
        serialNumBox.setLayout(serialNumLayout)

        winLayout = QHBoxLayout()
        winLayout.addWidget(serialNumBox)
        self.setLayout(winLayout)

    def keyPressEvent(self, event: QKeyEvent):
        if event.matches(QKeySequence.Paste):
            theText = QApplication.clipboard().text()
            # print(theText)
            theList = theText.splitlines()
            for i, r in enumerate(theList):
                print(i, r)
                item = QListWidgetItem(r)
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.PlainText)
                self._serialNumList.addItem(item)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'Are you sure to quit?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = AssetItemCreatorWindow(None, '대성에너지')
    w.show()
    sys.exit(app.exec_())