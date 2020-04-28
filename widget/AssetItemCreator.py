import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QDate
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
        self.initUIData()

    def initUI(self):
        self.setWindowTitle(self._company + ' - ' + 'Multi Items Creator Window')
        self.setWindowIcon(QIcon(Constants.BASE_PATH + '/img/daesung.ico'))

        lblAssetName = QLabel('자산명')
        lblProdDate = QLabel('제조일')
        lblReceiptDate = QLabel('입고일')
        lblMgrClass = QLabel('관리부문')
        lblMSOffice = QLabel('MS Office')
        lblHancomOffice = QLabel('한컴 Office')
        lblDisk = QLabel('디스크')
        cmbDisk = QComboBox()
        lblMem = QLabel('메모리')
        cmbMem = QComboBox()
        lblAcctNum = QLabel('회계관리번호')
        lblBarcode = QLabel('바코드')
        lblAssetNote = QLabel('비고')

        cmbAssetName = QComboBox()
        self._dateProd = QDateEdit()
        self._dateProd.setFixedWidth(150)
        self._dateReceipt = QDateEdit()
        self._dateReceipt.setFixedWidth(150)
        cmbMgrClass = QComboBox()
        cmbMSOffice = QComboBox()
        cmbHancomOffice = QComboBox()
        txtAcctNum = QLineEdit()
        txtBarcode = QLineEdit()
        txtAssetNote = QLineEdit()

        # 일련번호 추가/삭제는 Enter key, Delete key, Copy&Paste로 제어
        serialNumBox = QGroupBox('일련번호')
        serialNumLayout = QVBoxLayout()
        self._serialNumItem = QLineEdit()
        self._serialNumList = QListWidget()
        serialNumLayout.addWidget(self._serialNumItem)
        serialNumLayout.addWidget(self._serialNumList)
        serialNumBox.setLayout(serialNumLayout)
        serialNumBox.setFixedWidth(200)

        inputLayout = QGridLayout()
        inputLayout.addWidget(lblAssetName, 0, 0)
        inputLayout.addWidget(cmbAssetName, 0, 1)
        inputLayout.addWidget(lblMgrClass, 0, 2)
        inputLayout.addWidget(cmbMgrClass, 0, 3)
        inputLayout.addWidget(serialNumBox, 0, 4, 6, 1)
        inputLayout.addWidget(lblProdDate, 1, 0)
        inputLayout.addWidget(self._dateProd, 1, 1)
        inputLayout.addWidget(lblReceiptDate, 1, 2)
        inputLayout.addWidget(self._dateReceipt, 1, 3)
        inputLayout.addWidget(lblMem, 2, 0)
        inputLayout.addWidget(cmbMem, 2, 1)
        inputLayout.addWidget(lblDisk, 2, 2)
        inputLayout.addWidget(cmbDisk, 2, 3)
        inputLayout.addWidget(lblMSOffice, 3, 0)
        inputLayout.addWidget(cmbMSOffice, 3, 1)
        inputLayout.addWidget(lblHancomOffice, 3, 2)
        inputLayout.addWidget(cmbHancomOffice, 3, 3)
        inputLayout.addWidget(lblAcctNum, 4, 0)
        inputLayout.addWidget(txtAcctNum, 4, 1)
        inputLayout.addWidget(lblBarcode, 4, 2)
        inputLayout.addWidget(txtBarcode, 4, 3)
        inputLayout.addWidget(lblAssetNote, 5, 0)
        inputLayout.addWidget(txtAssetNote, 5, 1, 1, 3)

        winLayout = QVBoxLayout()
        # winLayout.addWidget(serialNumBox)
        winLayout.addLayout(inputLayout)
        self.setLayout(winLayout)

    def initUIData(self):
        self._dateProd.setDate(QDate.currentDate())
        self._dateProd.setDateRange(QDate(1900, 1, 1), QDate(2100, 12, 31))
        self._dateReceipt.setDate(QDate.currentDate())
        self._dateReceipt.setDateRange(QDate(1900, 1, 1), QDate(2100, 12, 31))

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() in [Qt.Key_Return, Qt.Key_Enter]:
            # Add the input data into the List Widget
            theText = self._serialNumItem.text()
            item = QListWidgetItem(theText)
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.PlainText)
            self._serialNumList.addItem(item)
            self._serialNumItem.clear()
        if event.key() in [Qt.Key_Delete]:
            # Remove the selected data from the List Widget
            row = self._serialNumList.currentRow()
            self._serialNumList.takeItem(row)
        if event.matches(QKeySequence.Paste):
            # Add the clipboard data into the List Widget
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