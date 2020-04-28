import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QIcon

from interface import mysqlHandler
from widget import CommonWidget

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import Constants

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

class OrgWindow(QWidget):
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

        self.setWindowTitle(self._company + ' - ' + '조직관리')
        self.setWindowIcon(QIcon(Constants.BASE_PATH + '/img/daesung.ico'))

        self._storedUserList = []
        self._currentCodeList = []


        self.composeLayout()

        self.getTable_Org()
        self.getTable_User()

        self.composeOrgTree()

        self.setSignals()

    # def setWindowIndex(self, index):
    #     self._index = index
    #
    # def getWindowIndex(self):
    #     return self._index

    def composeLayout(self):

        titleLayout = CommonWidget.TitleLayout('조직관리')

        # mainButtonLayout = QVBoxLayout()
        # self._btnClose = QPushButton('닫기')
        # # self._btnClose.setFixedWidth(100)
        # self._btnClose.resize(self._btnClose.sizeHint())
        # mainButtonLayout.addWidget(self._btnClose)
        # mainButtonLayout.setAlignment(Qt.AlignRight)

        bodyLayout = QGridLayout()

        leftLayout = QHBoxLayout()
        self._orgTreeWidget = QTreeWidget()
        # self._orgTreeWidget.setFixedWidth(400)
        # self._orgTreeWidget.setFixedHeight(500)
        leftLayout.addWidget(self._orgTreeWidget)
        self._orgTreeWidget.header().setVisible(True)
        orgHeaderLabels = ['회사조직', '상위조직', '중간조직', '조직']
        self._orgTreeWidget.setHeaderLabels(orgHeaderLabels)
        self._orgTreeWidget.setColumnCount(len(orgHeaderLabels))
        self._orgTreeWidget.header().setSectionResizeMode(QHeaderView.Stretch)
        # self._orgTreeWidget.setAlternatingRowColors(True)
        rightLayout = QVBoxLayout()

        subtitleLayout = QHBoxLayout()
        self._orgLabel = CommonWidget.SubtitleLabel('조직 구성원')
        self._countLabel = CommonWidget.SubtitleLabel('(인원수)')   # 인원수
        subtitleLayout.addWidget(self._orgLabel)
        subtitleLayout.addWidget(self._countLabel)

        codeTableLayout = QHBoxLayout()
        self._userTableWidget = QTableWidget(self)
        self._userTableWidget.setColumnCount(4)
        self._userTableWidget.setHorizontalHeaderLabels(['Chk', '조직', '사용자', '지역'])
        # self._userTableWidget.setColumnWidth(0, 15)
        self._userTableWidget.setAlternatingRowColors(True)      # 행 색상이 번갈아 구분 표시되게 한다.
        self._userTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)      # Edit 금지
        self._userTableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)     # Row 단위로 선택이 표되게 한다.
        self._userTableWidget.setSelectionMode(QAbstractItemView.SingleSelection)    # 하나의 Row만 선택하게 함. (다중
        # self._codeTableView.setFixedWidth(300)
        # self._codeTableView.setFixedHeight(380)
        codeTableLayout.addWidget(self._userTableWidget)

        orgItemLayout = QGridLayout()
        self._textBoxCompany = QLineEdit()
        self._textBoxSuperOrg = QLineEdit()
        self._textBoxMiddleOrg = QLineEdit()
        self._textBoxOrg = QLineEdit()
        self._textBoxCompany.setAlignment(Qt.AlignCenter)
        self._textBoxSuperOrg.setAlignment(Qt.AlignCenter)
        self._textBoxMiddleOrg.setAlignment(Qt.AlignCenter)
        self._textBoxOrg.setAlignment(Qt.AlignCenter)
        # self._textBoxCodeID.setFixedWidth(50)
        # self._textBoxCodeName.setFixedWidth(240)
        orgItemLayout.addWidget(QLabel('회사'), 0, 0, Qt.AlignCenter)
        orgItemLayout.addWidget(QLabel('상위조직'), 0, 1, Qt.AlignCenter)
        orgItemLayout.addWidget(QLabel('중간조직'), 0, 2, Qt.AlignCenter)
        orgItemLayout.addWidget(QLabel('부서(팀)'), 0, 3, Qt.AlignCenter)
        orgItemLayout.addWidget(self._textBoxCompany, 1, 0, Qt.AlignCenter)
        orgItemLayout.addWidget(self._textBoxSuperOrg, 1, 1, Qt.AlignCenter)
        orgItemLayout.addWidget(self._textBoxMiddleOrg, 1, 2, Qt.AlignCenter)
        orgItemLayout.addWidget(self._textBoxOrg, 1, 3, Qt.AlignCenter)

        self._btnAdd = QPushButton('추가')
        self._btnRemove = QPushButton('삭제')
        orgButtonLayout = QHBoxLayout()
        orgButtonLayout.addWidget(self._btnAdd)
        orgButtonLayout.addWidget(self._btnRemove)


        orgItemFrame = QFrame()
        orgItemAllLayout = QVBoxLayout()
        orgItemAllLayout.addWidget(CommonWidget.SubtitleLabel('조직'))
        orgItemAllLayout.addLayout(orgItemLayout)
        orgItemAllLayout.addLayout(orgButtonLayout)
        orgItemFrame.setFrameShape(QFrame.StyledPanel)
        orgItemFrame.setFrameShadow(QFrame.Raised)
        orgItemFrame.setLineWidth(1)
        orgItemFrame.setMidLineWidth(3)
        orgItemFrame.setLayout(orgItemAllLayout)

        moveUserFrame = QFrame()
        moveUserAllLayout = QVBoxLayout()
        moveUserLayout = QGridLayout()
        self._textBoxMoveCompany = QLineEdit()
        self._textBoxMoveOrg = QLineEdit()
        self._btnMove = QPushButton('부서 이동')
        moveUserLayout.addWidget(QLabel('이동할 회사'), 0, 0, Qt.AlignCenter)
        moveUserLayout.addWidget(QLabel('이동할 부서(팀)'), 0, 1, Qt.AlignCenter)
        moveUserLayout.addWidget(self._textBoxMoveCompany, 1, 0, Qt.AlignCenter)
        moveUserLayout.addWidget(self._textBoxMoveOrg, 1, 1, Qt.AlignCenter)
        moveUserLayout.addWidget(self._btnMove, 0, 2, 2, 1, Qt.AlignCenter)
        moveUserFrame.setFrameShape(QFrame.StyledPanel)
        moveUserFrame.setFrameShadow(QFrame.Raised)
        moveUserFrame.setLineWidth(1)
        moveUserFrame.setMidLineWidth(3)
        moveUserAllLayout.addWidget(CommonWidget.SubtitleLabel('조직 이동'))
        moveUserAllLayout.addLayout(moveUserLayout)
        moveUserFrame.setLayout(moveUserAllLayout)

        rightLayout.addWidget(orgItemFrame)
        rightLayout.addLayout(subtitleLayout)
        rightLayout.addLayout(codeTableLayout)
        rightLayout.addWidget(moveUserFrame)

        bodyLayout.addLayout(leftLayout, 0, 0)
        bodyLayout.addLayout(rightLayout, 0, 1)

        winLayout = QVBoxLayout()
        winLayout.addLayout(titleLayout)
        # winLayout.addLayout(mainButtonLayout)
        winLayout.addLayout(bodyLayout)

        self.setLayout(winLayout)

    def getTable_User(self):
        db_connection = mysqlHandler.dbConnect()
        cursor_dict = mysqlHandler.dbDictCursor(db_connection)
        sql = 'select org, user_name, region from myasset.it_user ' \
              ' order by org, user_name'
        cursor_dict.execute(sql)
        db_connection.close()
        self._userAllList = cursor_dict.fetchall()

    def getTable_Org(self):
        db_connection = mysqlHandler.dbConnect()
        cursor_dict = mysqlHandler.dbDictCursor(db_connection)
        sql = 'select company, super_org2, super_org1, org from myasset.it_user_org ' \
              ' order by company, super_org2, super_org1, org'
        cursor_dict.execute(sql)
        db_connection.close()
        self._codeTypeList = cursor_dict.fetchall()

    def composeOrgTree(self):
        self._orgTreeWidget.clear()
        rootItem = QTreeWidget.invisibleRootItem(self._orgTreeWidget)
        lastCompanyText = None
        lastSuperOrgText = None
        lastMiddleOrgText = None
        lastOrgText = None
        for r in self._codeTypeList:
            thisCompanyText = r.get('company')
            thisSuperOrgText = r.get('super_org2')
            thisMiddleOrgText = r.get('super_org1')
            thisOrgText = r.get('org')
            if thisCompanyText != lastCompanyText:
                companyItem = QTreeWidgetItem(rootItem)  # company
                companyItem.setText(Constants.TREE_COL_0, thisCompanyText)
                lastCompanyText = thisCompanyText
                lastSuperOrgText = None
                lastMiddleOrgText = None
                lastOrgText = None
            if thisCompanyText == lastCompanyText \
                and thisSuperOrgText != lastSuperOrgText:
                superOrgItem = QTreeWidgetItem(companyItem)  # super_org2
                superOrgItem.setText(Constants.TREE_COL_0, thisSuperOrgText)
                superOrgItem.setText(Constants.TREE_COL_1, thisSuperOrgText)
                lastSuperOrgText = thisSuperOrgText
                lastMiddleOrgText = None
                lastOrgText = None
            if thisCompanyText == lastCompanyText \
                and thisSuperOrgText == lastSuperOrgText \
                and thisMiddleOrgText != lastMiddleOrgText:
                middleOrgItem = QTreeWidgetItem(superOrgItem)  # super_org1
                middleOrgItem.setText(Constants.TREE_COL_0, thisMiddleOrgText)
                middleOrgItem.setText(Constants.TREE_COL_2, thisMiddleOrgText)
                lastMiddleOrgText = thisMiddleOrgText
                lastOrgText = None
            if thisCompanyText == lastCompanyText \
                and thisSuperOrgText == lastSuperOrgText \
                and thisMiddleOrgText == lastMiddleOrgText \
                and thisOrgText != lastOrgText:
                orgItem = QTreeWidgetItem(middleOrgItem)  # org
                orgItem.setText(Constants.TREE_COL_0, thisOrgText)
                orgItem.setText(Constants.TREE_COL_3, thisOrgText)
                lastOrgText = thisOrgText
        self._orgTreeWidget.expandAll()


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
        # self._orgTreeWidget.itemChanged.connect(self.__treeItemChanged)
        self._orgTreeWidget.itemClicked.connect(self.__treeItemClicked)
        self._userTableWidget.cellClicked.connect(self.__cellClicked)
        self._btnAdd.clicked.connect(self.__btnAddClicked)
        self._btnRemove.clicked.connect(self.__btnRemoveClicked)
        # self._textBoxCodeID.textEdited.connect(self.__textEdited)
        # self._textBoxCodeName.textEdited.connect(self.__textEdited)
        # self._btnAdd.clicked.connect(self.moveItem)
        # self.btnUp.clicked.connect(self.moveItem)
        # self.btnDown.clicked.connect(self.moveItem)

    # def moveItem(self):
    #     # sender = self.sender()
    #     #
    #     # if self.btnUp == sender:
    #     #     source = self.lecture_list
    #     #     target = self.wishlist
    #     # else:
    #     #     source = self.wishlist
    #     #     target = self.lecture_list
    #     source = self._orgTreeWidget
    #     target = self._orgTreeWidget
    #     # idx = self._orgTreeWidget.currentIndex()
    #     # item = self._orgTreeWidget.currentIndex().row()
    #     # self._orgTreeWidget.rowsInserted(item, idx+1)
    #     theItem = self._orgTreeWidget.currentItem()
    #     parentItem = theItem.parent()
    #     QTreeWidgetItem.p
    #     item = QTreeWidget.invisibleRootItem(source).takeChild(source.currentIndex().row())
    #     QTreeWidget.invisibleRootItem(target).addChild(item)
    #     QTreeWidget.invisibleRootItem(target).insert
    #     QTreeWidgetItem.insertChild()



    # 다른 객체간으로 아이템 이동
    # def move_Item(self):
    #     sender = self.sender()
    #
    #     if self.btnUp == sender:
    #         source = self.lecture_list
    #         target = self.wishlist
    #     else:
    #         source = self.wishlist
    #         target = self.lecture_list
    #
    #     item = QTreeWidget.invisibleRootItem(source).takeChild(source.currentIndex().row())
    #     QTreeWidget.invisibleRootItem(target).addChild(item)



    # def closeEvent(self, event):
    #     # if self.parent != None:
    #     #     self.parent.windowChildClosed(self)
    #     event.accept()
    #     print("Closed")

    def __textEdited(self):
        pass

    def showOrgUsers(self):
        self._userTableWidget.clearContents()
        self._userTableWidget.setRowCount(len(self._currentCodeList))
        for i, row in enumerate(self._currentCodeList):
            org = QTableWidgetItem(row[0])
            userName = QTableWidgetItem(row[1])
            region = QTableWidgetItem(row[2])
            org.setTextAlignment(Qt.AlignVCenter)
            userName.setTextAlignment(Qt.AlignVCenter)
            region.setTextAlignment(Qt.AlignVCenter)
            # codeID.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)     # not editable
            # codeName.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)   # not editable
            chkCellWidget = QWidget()
            chkLayout = QHBoxLayout(chkCellWidget)
            chkLayout.addWidget(QCheckBox())
            chkLayout.setAlignment(Qt.AlignCenter)
            chkLayout.setContentsMargins(0,0,0,0)
            chkCellWidget.setLayout(chkLayout)
            self._userTableWidget.setCellWidget(i, 0, chkCellWidget)
            self._userTableWidget.setItem(i, 1, org)
            self._userTableWidget.setItem(i, 2, userName)
            self._userTableWidget.setItem(i, 3, region)

        self._userTableWidget.resizeRowsToContents()
        self._userTableWidget.resizeColumnToContents(0)     # to resize CheckBox column
        # self._userTableWidget.resizeColumnsToContents()

    def showOrgData(self):
        selectedItem = self._orgTreeWidget.currentItem()
        orgText = selectedItem.text(0)
        middleOrgItem = selectedItem.parent()
        middleOrgText = middleOrgItem.text(0)
        superOrgItem = middleOrgItem.parent()
        superOrgText = superOrgItem.text(0)
        companyItem = superOrgItem.parent()
        companyText = companyItem.text(0)
        self._textBoxCompany.setText(companyText)
        self._textBoxSuperOrg.setText(superOrgText)
        self._textBoxMiddleOrg.setText(middleOrgText)
        self._textBoxOrg.setText(orgText)

    def __treeItemClicked(self):
        self._orgLabel.setText('조직 구성원')
        self._countLabel.setText('(인원수)')
        self._textBoxCompany.clear()
        self._textBoxSuperOrg.clear()
        self._textBoxMiddleOrg.clear()
        self._textBoxOrg.clear()
        self._userTableWidget.clearContents()
        self._userTableWidget.setRowCount(0)
        selectedItem = self._orgTreeWidget.currentItem()
        # Check if last node having 'org'
        if selectedItem.text(Constants.TREE_COL_0) != selectedItem.text(Constants.TREE_COL_3):
            return

        middleOrgItem = selectedItem.parent()
        superOrgItem = middleOrgItem.parent()
        companyItem = superOrgItem.parent()
        companyText = companyItem.text(Constants.TREE_COL_0)
        orgText = selectedItem.text(Constants.TREE_COL_0)
        self._storedUserList = []
        for c in self._userAllList:
            # 'company' needs to be considered later
            # if c.get('company') == companyText and c.get('org') == orgText:
            if c.get('org') == orgText:
                item = [c.get('org'), c.get('user_name'), c.get('region')]
                self._storedUserList.append(item)

        self._currentCodeList = self._storedUserList.copy()
        self.showOrgUsers()
        self._orgLabel.setText(companyText + ' ' + orgText)
        self._countLabel.setText('(' + str(len(self._currentCodeList)) + ')명')
        self.showOrgData()

        self._codeItemIndex = __NOT_SELECTED__

    def reInitData(self):
        self.getTable_Org()
        self.composeOrgTree()
        self._textBoxCompany.clear()
        self._textBoxSuperOrg.clear()
        self._textBoxMiddleOrg.clear()
        self._textBoxOrg.clear()
        self._orgLabel.setText('조직 구성원')
        self._countLabel.setText('(인원수)')
        self._userTableWidget.clearContents()
        self._userTableWidget.setRowCount(0)

    # primary key 중복 체크 추가 (company, org)
    # 텍스트 내용이 비어 있는 경우에 동작하지 않도록 함.
    def __btnAddClicked(self):
        orgText = self._textBoxOrg.text()
        middleOrgText = self._textBoxMiddleOrg.text()   # super org 1
        superOrgText = self._textBoxSuperOrg.text()     # super org 2
        companyText = self._textBoxCompany.text()
        dbData = [companyText, orgText, middleOrgText, superOrgText]
        try:
            db_connection = mysqlHandler.dbConnect()
            cursor = mysqlHandler.dbCursor(db_connection)
            sql = 'insert into myasset.it_user_org(company, org, super_org1, super_org2) ' \
                  'values (%s, %s, %s, %s)'
            cursor.execute(sql, dbData)
            db_connection.commit()
            __DB_TRANSACTION_FLAG__ = True
        except Exception as e:
            __DB_TRANSACTION_FLAG__ = False
            print(e)
        finally:
            db_connection.close()
        if __DB_TRANSACTION_FLAG__ == True:
            self.reInitData()

    # 해당 조직에 속한 사용자가 있는지 DB에서 체크 -> 있다면 삭제 못하게 막아야 함.
    # 텍스트 내용이 비어 있는 경우에 동작하지 않도록 함.
    def __btnRemoveClicked(self):
        __DB_TRANSACTION_FLAG__ = None
        orgText = self._textBoxOrg.text()
        middleOrgText = self._textBoxMiddleOrg.text()   # super org 1
        superOrgText = self._textBoxSuperOrg.text()     # super org 2
        companyText = self._textBoxCompany.text()
        dbData = [companyText, orgText, middleOrgText, superOrgText]
        try:
            db_connection = mysqlHandler.dbConnect()
            cursor = mysqlHandler.dbCursor(db_connection)
            sql = 'delete from myasset.it_user_org ' \
                  ' where company = %s and org = %s and super_org1 = %s and super_org2 = %s'
            cursor.execute(sql, dbData)
            db_connection.commit()
            __DB_TRANSACTION_FLAG__ = True
        except Exception as e:
            __DB_TRANSACTION_FLAG__ = False
            print(e)
        finally:
            db_connection.close()
        if __DB_TRANSACTION_FLAG__ == True:
            self.reInitData()

    @pyqtSlot(int, int)
    def __cellClicked(self, row, col):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    w = OrgWindow(None, '대성에너지')
    w.show()
    sys.exit(app.exec_())