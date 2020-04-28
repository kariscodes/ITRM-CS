import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QIcon
from interface import mysqlHandler
from widget import CommonWidget

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import Constants
# sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

# def openDBConnection(self):
#     self._db_connection = mysqlHandler.dbConnect()
#     self._cursor = mysqlHandler.dbDictCursor(self._db_connection)
#
# def runSQL_Select(self, sql):
#     self._cursor.execute(sql)
#     # object: dictionary
#     result = self._cursor.fetchall()
#     return result
#
# def closeDBConnection(self):
#     self._db_connection.close()

__NOT_SELECTED__ = -1

class CodeWindow(QWidget):
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
        # self.setWindowModality(Qt.NonModal)     # to set non-modal dialog
        self.initUI()

    def initUI(self):

        self.setWindowTitle(self._company + ' - ' + '공통코드관리')
        self.setWindowIcon(QIcon(Constants.BASE_PATH + '/img/daesung.ico'))

        self._storedCodeList = []
        self._currentCodeList = []

        self.composeLayout()
        self.setCodeTypeList()
        self.setSignals()

    # def setWindowIndex(self, index):
    #     self._index = index
    #
    # def getWindowIndex(self):
    #     return self._index

    def composeLayout(self):

        titleLayout = CommonWidget.TitleLayout('공통코드관리')

        # mainButtonLayout = QVBoxLayout()
        # self._btnClose = QPushButton('닫기')
        # # self._btnClose.setFixedWidth(100)
        # self._btnClose.resize(self._btnClose.sizeHint())
        # mainButtonLayout.addWidget(self._btnClose)
        # mainButtonLayout.setAlignment(Qt.AlignRight)

        bodyLayout = QGridLayout()

        leftLayout = QHBoxLayout()
        self._codeTree = QTreeWidget()
        # self._codeTree.setFixedWidth(400)
        # self._codeTree.setFixedHeight(500)
        leftLayout.addWidget(self._codeTree)

        rightLayout = QVBoxLayout()

        subtitleLayout = QHBoxLayout()
        self._codeTypeLabel = CommonWidget.SubtitleLabel('공통코드')
        subtitleLayout.addWidget(self._codeTypeLabel)

        codeTableLayout = QHBoxLayout()
        self._codeTableWidget = QTableWidget(self)
        self._codeTableWidget.setColumnCount(2)
        # self._codeTableWidget.setColumnWidth(0, 15)
        self._codeTableWidget.setHorizontalHeaderLabels(['코드ID', '코드명'])
        self._codeTableWidget.setAlternatingRowColors(True)      # 행 색상이 번갈아 구분 표시되게 한다.
        self._codeTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)      # Edit 금지
        self._codeTableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)     # Row 단위로 선택이 표되게 한다.
        self._codeTableWidget.setSelectionMode(QAbstractItemView.SingleSelection)    # 하나의 Row만 선택하게 함. (다중
        # self._codeTableView.setFixedWidth(300)
        # self._codeTableView.setFixedHeight(380)
        codeTableLayout.addWidget(self._codeTableWidget)

        codeItemLayout = QHBoxLayout()
        self._textBoxCodeID = QLineEdit()
        self._textBoxCodeID.setAlignment(Qt.AlignCenter)
        # self._textBoxCodeID.setFixedWidth(50)
        self._textBoxCodeName = QLineEdit()
        # self._textBoxCodeName.setFixedWidth(240)
        codeItemLayout.addWidget(self._textBoxCodeID)
        codeItemLayout.addWidget(self._textBoxCodeName)

        buttonLayout = QHBoxLayout()
        self._btnAdd = QPushButton('추가')
        self._btnModify = QPushButton('수정')
        self._btnRemove = QPushButton('삭제')
        self._btnAdd.setEnabled(False)
        self._btnModify.setEnabled(False)
        self._btnRemove.setEnabled(False)
        buttonLayout.addWidget(self._btnAdd)
        buttonLayout.addWidget(self._btnModify)
        buttonLayout.addWidget(self._btnRemove)

        saveLayout = QHBoxLayout()
        self._btnSave = QPushButton('저장')
        self._btnSave.setEnabled(False)
        saveLayout.addWidget(self._btnSave)

        rightLayout.addLayout(subtitleLayout)
        rightLayout.addLayout(codeTableLayout)
        rightLayout.addLayout(codeItemLayout)
        rightLayout.addLayout(buttonLayout)
        rightLayout.addLayout(saveLayout)

        bodyLayout.addLayout(leftLayout, 0, 0)
        bodyLayout.addLayout(rightLayout, 0, 1)

        winLayout = QVBoxLayout()
        winLayout.addLayout(titleLayout)
        # winLayout.addLayout(mainButtonLayout)
        winLayout.addLayout(bodyLayout)

        self.setLayout(winLayout)

    def setCodeTypeList(self):
        # self._codeTree.header().setVisible(False)
        self._codeTree.setColumnCount(2)
        self._codeTree.setHeaderLabels(['코드유형 ID', '코드유형 명칭'])
        self._codeTree.header().setSectionResizeMode(QHeaderView.Stretch)
        self._codeTree.setAlternatingRowColors(True)
        db_connection = mysqlHandler.dbConnect()
        cursor_dict = mysqlHandler.dbDictCursor(db_connection)
        sql = 'select code_type, code_type_name from myasset.common_code_hdr order by code_type_name'
        cursor_dict.execute(sql)
        # object: dictionary
        self._codeTypeList = cursor_dict.fetchall()
        topNode = QTreeWidgetItem(self._codeTree)
        topNode.setText(0, '공통코드')
        for r in self._codeTypeList:
            item = QTreeWidgetItem(topNode)
            item.setText(0, r.get('code_type'))
            item.setText(1, r.get('code_type_name'))
        self._codeTree.expandAll()

        sql = 'select code_type, code_id, code_name from myasset.common_code order by code_id'
        cursor_dict.execute(sql)
        # object: dictionary
        self._codeAllList = cursor_dict.fetchall()

        db_connection.close()
    # def changeState(self, state):
    #     """
    #     toggle 상태에 따라 배경색과 상태 텍스트 변환
    #     """
    #     self.runState.setStyleSheet("background-color: %s" % ({True: "green", False: "red"}[state]))
    #     self.runState.setText({True: "ON", False: "OFF"}[state])

    def keyReleaseEvent(self, e):
        if e.key() == Qt.Key_Down or e.key() == Qt.Key_Up:
            self.__treeItemClicked()

    def setSignals(self):
        # self._btnClose.clicked.connect(self.close)  # closeEvent
        # self._codeTree.itemChanged.connect(self.__treeItemChanged)
        self._codeTree.itemClicked.connect(self.__treeItemClicked)
        self._codeTableWidget.cellClicked.connect(self.__cellClicked)
        self._btnAdd.clicked.connect(self.__btnAddClicked)
        self._btnModify.clicked.connect(self.__btnModifyClicked)
        self._btnRemove.clicked.connect(self.__btnRemoveClicked)
        self._btnSave.clicked.connect(self.__btnSaveClicked)
        self._textBoxCodeID.textEdited.connect(self.__textEdited)
        self._textBoxCodeName.textEdited.connect(self.__textEdited)

    # def closeEvent(self, event):
    #     # if self.parent != None:
    #     #     self.parent.windowChildClosed(self)
    #     event.accept()
    #     print("Closed")

    def __textEdited(self):
        self.enableOperation(True)

    def showCurrentData(self):
        self._codeTableWidget.clearContents()
        self._codeTableWidget.setRowCount(len(self._currentCodeList))
        cnt = 0
        for i in self._currentCodeList:
            codeID = QTableWidgetItem(i[1])
            codeName = QTableWidgetItem(i[2])
            codeID.setTextAlignment(Qt.AlignCenter)
            codeName.setTextAlignment(Qt.AlignVCenter)
            # codeID.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)     # not editable
            # codeName.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)   # not editable
            self._codeTableWidget.setItem(cnt, 0, codeID)
            self._codeTableWidget.setItem(cnt, 1, codeName)
            cnt += 1

        self._codeTableWidget.resizeRowsToContents()
        self._codeTableWidget.resizeColumnsToContents()

        self.enableOperation(False)
        self._btnSave.setEnabled(True)

    def __btnAddClicked(self):
        codeType = self._codeType
        codeID = self._textBoxCodeID.text()
        codeName = self._textBoxCodeName.text()
        if len(codeID) == 0 or len(codeName) == 0:
            QMessageBox.information(self, 'Warning', '코드ID나 코드명에 데이터 값이 없습니다. 다시 확인하시기 바랍니다.')
            return

        for i in self._currentCodeList:
            if i[1] == codeID:
                QMessageBox.information(self, 'Warning', '코드가 중복되었습니다. 다시 확인하시기 바랍니다.')
                return
        self._currentCodeList.append([codeType, codeID, codeName])
        self.showCurrentData()

    def __btnModifyClicked(self):
        codeType = self._codeType
        codeID = self._textBoxCodeID.text()
        codeName = self._textBoxCodeName.text()
        if len(codeID) == 0 or len(codeName) == 0:
            QMessageBox.information(self, 'Warning', '코드ID나 코드명에 데이터 값이 없습니다. 다시 확인하시기 바랍니다.')
            return

        row = 0
        for i in self._currentCodeList:
            if i[1] == codeID:
                self._codeItemIndex = row
            row += 1
        if self._codeItemIndex != __NOT_SELECTED__:
            index = self._codeItemIndex
            self._currentCodeList[index] = [codeType, codeID, codeName]
            self.showCurrentData()

    def __btnRemoveClicked(self):
        codeType = self._codeType
        codeID = self._textBoxCodeID.text()
        codeName = self._textBoxCodeName.text()
        if len(codeID) == 0 or len(codeName) == 0:
            QMessageBox.information(self, 'Warning', '코드ID나 코드명에 데이터 값이 없습니다. 다시 확인하시기 바랍니다.')
            return

        if [codeType, codeID, codeName] in self._currentCodeList:
            self._currentCodeList.remove([codeType, codeID, codeName])
            self.showCurrentData()
        else:
            QMessageBox.information(self, 'Warning', '삭제하려는 코드가 없습니다. 다시 확인하시기 바랍니다.')
            return

    def __btnSaveClicked(self):
        if self._currentCodeList == self._storedCodeList:
            return

        try:
            codeType = self._codeType
            codeList = self._currentCodeList
            # DB Data handling
            # 1) delete all data with the specific code_type
            # 2) create all data with the specific code_type
            db_connection = mysqlHandler.dbConnect()
            cursor = mysqlHandler.dbCursor(db_connection)
            sql = 'delete from myasset.common_code where code_type = %s'
            cursor.execute(sql, codeType)
            sql = 'insert into myasset.common_code(code_type, code_id, code_name) values (%s, %s, %s)'
            cursor.executemany(sql, codeList)
            db_connection.commit()
            # 3) Get the data from the code table newly.
            sql = 'select code_type, code_id, code_name from myasset.common_code order by code_id'
            cursor_dict = mysqlHandler.dbDictCursor(db_connection)
            cursor_dict.execute(sql)
            # object: dictionary
            self._codeAllList = cursor_dict.fetchall()
        finally:
            db_connection.close()
            self._storedCodeList = self._currentCodeList.copy()
            self._codeTableWidget.sortByColumn(0, Qt.AscendingOrder)
            self.enableOperation(False)
            self._btnSave.setEnabled(False)

    def __treeItemClicked(self):
        if self._currentCodeList != self._storedCodeList:
            QMessageBox.information(self, 'Information', '저장하지 않은 데이터가 있습니다. 변경 사항을 저장하십시오.')
            return

        selectedItem = self._codeTree.currentItem()
        self._codeType = selectedItem.text(0)
        self._codeTypeName = selectedItem.text(1)
        self._codeTypeLabel.setText(self._codeType + '\t' + self._codeTypeName)
        self._storedCodeList = []
        for c in self._codeAllList:
            if c.get('code_type') == self._codeType:
                item = [c.get('code_type'), c.get('code_id'), c.get('code_name')]
                self._storedCodeList.append(item)

        self._currentCodeList = self._storedCodeList.copy()
        self.showCurrentData()

        self._codeItemIndex = __NOT_SELECTED__

        self.enableOperation(False)
        self._btnSave.setEnabled(False)

    @pyqtSlot(int, int)
    def __cellClicked(self, row, col):
        codeID = self._codeTableWidget.item(row, 0)
        codeName = self._codeTableWidget.item(row, 1)
        self._codeItemIndex = row
        self._textBoxCodeID.setText(codeID.text())
        self._textBoxCodeName.setText(codeName.text())
        self.enableOperation(True)
        return

    def enableOperation(self, isAvalable):
        if isAvalable == True:
            self._btnAdd.setEnabled(True)
            self._btnModify.setEnabled(True)
            self._btnRemove.setEnabled(True)
        elif isAvalable == False:
            self._textBoxCodeID.clear()
            self._textBoxCodeName.clear()
            self._btnAdd.setEnabled(False)
            self._btnModify.setEnabled(False)
            self._btnRemove.setEnabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    w = CodeWindow(None, '대성에너지')
    w.show()
    sys.exit(app.exec_())