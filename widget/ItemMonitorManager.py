import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent, QKeySequence

from interface import mysqlHandler

__NOT_SELECTED__ = -1

class ItemMonitorWindow(QWidget):
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
        self.composeLayout()
        self.initUIData()
        self.initUIWidgets()
        # self.setSignals()
        # self.loadUsers()
        # self.__CURRENT_USER_NAME = None

    def composeLayout(self):

        cmdBtnFrame = QFrame()
        cmdBtnLayout = QGridLayout()
        self._btnNew = QPushButton('신규')
        self._btnCopy = QPushButton('복사')
        self._btnAdd = QPushButton('추가')
        self._btnModify = QPushButton('수정')
        self._btnRemove = QPushButton('삭제')
        cmdBtnLayout.addWidget(self._btnNew, 0, 0)
        cmdBtnLayout.addWidget(self._btnCopy, 0, 1)
        cmdBtnLayout.addWidget(self._btnAdd, 0, 2)
        cmdBtnLayout.addWidget(self._btnModify, 0, 3)
        cmdBtnLayout.addWidget(self._btnRemove, 0, 4)
        # cmdBtnLayout.setColumnStretch(0, 0)
        # cmdBtnLayout.setRownStretch(0, 0)
        # cmdBtnLayout.setContentsMargins(0,0,0,0)
        # cmdBtnLayout.setVerticalSpacing(0)
        cmdBtnFrame.setLayout(cmdBtnLayout)
        # cmdBtnFrame.setFixedHeight(200)

        inputLayout = QGridLayout()
        lblModel = QLabel('모델번호')
        txtModel = QLineEdit()
        lblAcctNum = QLabel('회계관리번호')
        txtAcctNum = QLineEdit()
        lblBarcode = QLabel('바코드')
        txtBarcode = QLineEdit()
        lblSize = QLabel('화면크기(inch)')
        self._cmbSize = QComboBox()
        lblSupplier = QLabel('구입처')
        self._cmbSupplier = QComboBox()
        lblPurchaseDate = QLabel('구입일')
        self._datePurchase = QDateEdit()
        lblNote = QLabel('비고')
        txtNote = QLineEdit()
        # lblSerialNumber = QLabel('Serial Number')

        # 일련번호 추가/삭제는 Enter key, Delete key, Copy&Paste로 제어
        serialNumBox = QGroupBox('일련번호')
        serialNumLayout = QVBoxLayout()
        self._serialNumItem = QLineEdit()
        self._serialNumList = QListWidget()
        serialNumLayout.addWidget(self._serialNumItem)
        serialNumLayout.addWidget(self._serialNumList)
        serialNumBox.setLayout(serialNumLayout)
        serialNumBox.setFixedWidth(200)

        # self._serialNumItem = QLineEdit()
        # self._serialNumList = QListWidget()
        inputLayout.addWidget(lblModel, 0, 0)
        inputLayout.addWidget(txtModel, 0, 1)
        inputLayout.addWidget(lblSize, 1, 0)
        inputLayout.addWidget(self._cmbSize, 1, 1)
        inputLayout.addWidget(lblPurchaseDate, 2, 0)
        inputLayout.addWidget(self._datePurchase, 2, 1)
        inputLayout.addWidget(lblSupplier, 3, 0)
        inputLayout.addWidget(self._cmbSupplier, 3, 1)
        inputLayout.addWidget(lblAcctNum, 4, 0)
        inputLayout.addWidget(txtAcctNum, 4, 1)
        inputLayout.addWidget(lblBarcode, 5, 0)
        inputLayout.addWidget(txtBarcode, 5, 1)
        inputLayout.addWidget(lblNote, 6, 0)
        inputLayout.addWidget(txtNote, 6, 1, 1, 2)
        inputLayout.addWidget(serialNumBox, 0, 2, 6, 1)
        # inputLayout.addWidget(lblSerialNumber, 0, 2)
        # inputLayout.addWidget(self._serialNumItem, 1, 2)
        # inputLayout.addWidget(self._serialNumList, 2, 2, 4, 1)
        inputLayout.setColumnStretch(0, 0)
        inputLayout.setColumnStretch(1, 1)
        inputLayout.setColumnStretch(2, 1)

        bodyFrame = QFrame()
        bodyFrame.setLayout(inputLayout)
        bodyFrame.setFrameShape(QFrame.StyledPanel)
        bodyFrame.setFrameShadow(QFrame.Raised)
        bodyFrame.setLineWidth(3)
        bodyFrame.setMidLineWidth(3)

        self._itemTableWidget = QTableWidget()
        self._itemTableWidget.setSortingEnabled(True)            # 컬럼 헤더를 클릭하면 정렬이 되게 한다.
        self._itemTableWidget.setAlternatingRowColors(True)      # 행 색상이 번갈아 구분 표시되게 한다.
        # self._modelTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)      # Edit 금지
        # self._modelTableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)     # Row 단위로 선택이 표시되게 한다.
        self._itemTableWidget.setSelectionMode(QAbstractItemView.SingleSelection)    # 하나의 Row만 선택하게 함.
        modelHeaderLabels = ['모델번호', 'Serial Number', '화면 크기', '구입일', '구입처', '회계관리번호', '바코드', '비고']
        self._itemTableWidget.setColumnCount(len(modelHeaderLabels))
        self._itemTableWidget.setHorizontalHeaderLabels(modelHeaderLabels)

        winLayout = QGridLayout()
        winLayout.addWidget(bodyFrame, 0, 0)
        winLayout.addWidget(cmdBtnFrame, 1, 0)
        winLayout.addWidget(self._itemTableWidget, 2, 0)

        self.setLayout(winLayout)

    def initUIData(self):
        # Open DB Connection
        self.db_connection = mysqlHandler.dbConnect()
        self.cursor_dict = mysqlHandler.dbDictCursor(self.db_connection)

        self.getData_MonitorSize()
        self.getData_Supplier()

        # Close DB Connection
        self.db_connection.close()

    def initUIWidgets(self):
        self.fillItems_MonitorSize()
        self.fillItems_Supplier()
        self._cmbSize.setCurrentIndex(__NOT_SELECTED__)
        self._cmbSupplier.setCurrentIndex(__NOT_SELECTED__)

    def getData_MonitorSize(self):
        sql = 'select code_id, code_name from myasset.common_code ' \
              ' where code_type = %s ' \
              ' order by code_type, code_id '
        self.cursor_dict.execute(sql, 'monitor_size')
        codeDict = self.cursor_dict.fetchall()
        # to create dictionary with key-value pair (code id, code name)
        self._sizeList = []
        for i in codeDict:
            dicData = {}
            dicData['inch'] = str(i.get('code_id'))
            # sizeDic['cm'] = str(i.get('code_name'))
            dicData['string'] = str(i.get('code_id')) + ' (' + str(i.get('code_name'))+ 'cm)'
            self._sizeList.append(dicData)

    def getData_Supplier(self):
        sql = 'select code_id, code_name from myasset.common_code ' \
              ' where code_type = %s ' \
              ' order by code_type, code_id '
        self.cursor_dict.execute(sql, 'supplier')
        codeDict = self.cursor_dict.fetchall()
        # to create dictionary with key-value pair (code id, code name)
        self._supplierList = []
        for i in codeDict:
            dicData = {}
            dicData['code_id'] = str(i.get('code_id'))
            # sizeDic['cm'] = str(i.get('code_name'))
            dicData['code_name'] = str(i.get('code_name'))
            self._supplierList.append(dicData)

    def fillItems_MonitorSize(self):
        self._cmbSize.clear()
        for i, dict in enumerate(self._sizeList):
            self._cmbSize.addItem(dict.get('string'), dict.get('inch'))

    def fillItems_Supplier(self):
        self._cmbSupplier.clear()
        for i, dict in enumerate(self._supplierList):
            self._cmbSupplier.addItem(dict.get('code_name'), dict.get('code_id'))

    # def setSignals(self):
    #     # self._btnClose.clicked.connect(self.close)  # closeEvent
    #     self._btn1Add.clicked.connect(self.__clickedNew)
    #     self._btn1Copy.clicked.connect(self.__clickedSearch)
    #     self._btn1Modify.clicked.connect(self.__clickedSave)
    #     self._btn1Remove.clicked.connect(self.__clickedRemove)
    #     self._jobComboBox.currentIndexChanged.connect(self.__jobSelected)
    #     self._diskTypeComboBox.currentIndexChanged.connect(self.__diskTypeSelected)
    #     self._diskCapacityComboBox.currentIndexChanged.connect(self.__diskCapacitySelected)
    #     # self._diskNoButton.clicked.connect(self.__clickedDiskNo)
    #     # self._diskYesButton.clicked.connect(self.__clickedDiskYes)
    #     self._userNameTextBox.returnPressed.connect(self.__userNameEntered)
    #     self._userTableWidget.cellClicked.connect(self.__clickedTableWidget)
    #     self._btnMultiAdd.clicked.connect(self.__clickedMultiAddItems)
    #
    # # def closeEvent(self, event):
    # #     # if self._parent != None:
    # #     #     self._parent.windowChildClosed(self)
    # #     event.accept()
    # #     print("Closed")
    # #
    # # def __textEdited(self):
    # #     self.enableOperation(True)
    #
    # def __clickedNew(self):
    #     self.initUIWidgets()
    #     self.__CURRENT_USER_NAME = None
    #     self._msgLabel.setText('신규 사용자를 입력할 준비가 되었습니다.')
    #
    # def __userNameEntered(self):
    #     self.search()
    #
    # def __clickedSearch(self):
    #     self.search()
    #
    # def search(self):
    #     inputUserName = self._userNameTextBox.text()
    #     if len(inputUserName) == 0:
    #         QMessageBox.warning(self, 'No User Name',
    #                             '사용자명을 입력 후 엔터키를 누르거나 조회 버튼을 눌러 사용자 정보를 조회하십시오.')
    #         msg = '사용자명을 입력하세요.'
    #         self._msgLabel.setText(msg)
    #         return
    #
    #     self.__CURRENT_USER_NAME = inputUserName
    #     self._oneUserData = self.dbLoad(inputUserName)  # List with Dictionary items
    #     if len(self._oneUserData) != 0:
    #         self.showData()
    #         msg = f'사용자 [{inputUserName}]을(를) 조회하였습니다.'  # f-string
    #         self._msgLabel.setText(msg)
    #         self.__USER_EXIST__ = True
    #         self._btnRemove.setEnabled(True)
    #     else:
    #         msg = '사용자를 조회할 수 없습니다.'
    #         self._msgLabel.setText(msg)
    #         self.initUIWidgets()
    #         self.__USER_EXIST__ = False
    #         self._btnRemove.setEnabled(False)
    #
    # def loadUsers(self, specificUserName=None):
    #     self._usersDataList = self.dbLoad()     # List with Dictionary items
    #     self.showUserTable()
    #
    # def dbLoad(self, specificUserName=None):
    #     try:
    #         db_connection = mysqlHandler.dbConnect()
    #         cursor_dict = mysqlHandler.dbDictCursor(db_connection)
    #         sql = 'select ' \
    #               ' user_name, ' \
    #               ' job_type, ' \
    #               ' org, ' \
    #               ' regular_exchange, ' \
    #               ' region, ' \
    #               ' location, ' \
    #               ' extra_disk, ' \
    #               ' extra_disk_type, ' \
    #               ' extra_disk_capacity, ' \
    #               ' user_note '
    #         if specificUserName:
    #             sql += ' from myasset.it_user where user_name = %s'
    #             cursor_dict.execute(sql, specificUserName)
    #         else:
    #             sql += ' from myasset.it_user order by user_name'
    #             cursor_dict.execute(sql)
    #     finally:
    #         db_connection.close()
    #
    #     data = cursor_dict.fetchall()   # List with Dictionary items
    #     # to add key-value pairs : code id(key)에 대응하는 name(value)
    #     for i, row in enumerate(data):
    #         row['job_type_name'] = self._dictJobType.get(row.get('job_type'))
    #         row['location_name'] = self._dictLocation.get(row.get('location'))
    #         row['extra_disk_type_name'] = self._dictDiskType.get(row.get('extra_disk_type'))
    #         row['extra_disk_capacity_name'] = self._dictDiskCapacity.get(row.get('extra_disk_capacity'))
    #         row['region_name'] = self._dictRegion.get(row.get('region'))
    #
    #     return data
    #
    # def showData(self):
    #     if len(self._oneUserData) != 1:
    #         return
    #     r = self._oneUserData[0]
    #     self._userNameTextBox.setText(r.get('user_name'))
    #     self._noteEdit.setText(r.get('user_note'))
    #     self._jobComboBox.setCurrentIndex(self._jobComboBox.findData(r.get('job_type')))
    #     self._locationComboBox.setCurrentIndex(self._locationComboBox.findData(r.get('location')))
    #     self._regionComboBox.setCurrentText(r.get('region'))
    #     # self._orgComboBox.setCurrentText(r.get('org'))
    #     if r.get('extra_disk') == 'Y':
    #         # self._diskYesButton.setChecked(True)
    #         # self._diskNoButton.setChecked(False)
    #         self._diskTypeComboBox.setEnabled(True)
    #         self._diskCapacityComboBox.setEnabled(True)
    #         self.fillItems_DiskType()
    #         self.fillItems_DiskCapacity()
    #         self._diskTypeComboBox.setCurrentIndex(self._diskTypeComboBox.findData(r.get('extra_disk_type')))
    #         self._diskCapacityComboBox.setCurrentIndex(self._diskCapacityComboBox.findData(r.get('extra_disk_capacity')))
    #     elif r.get('extra_disk') == 'N':
    #         # self._diskYesButton.setChecked(False)
    #         # self._diskNoButton.setChecked(True)
    #         self._diskTypeComboBox.setEnabled(False)
    #         self._diskCapacityComboBox.setEnabled(False)
    #         self._diskTypeComboBox.setCurrentIndex(__NOT_SELECTED__)
    #         self._diskCapacityComboBox.setCurrentIndex(__NOT_SELECTED__)
    #
    # def keyReleaseEvent(self, e):
    #     if e.key() == Qt.Key_Down or e.key() == Qt.Key_Up:
    #         self.__clickedTableWidget()
    #
    # # 사용자 데이터 표시
    # def __clickedTableWidget(self):
    #     row = self._userTableWidget.currentRow()
    #     userNameItem = self._userTableWidget.item(row, 0)
    #     inputUserName = userNameItem.text()
    #     theUserDict = {}
    #     for i in self._usersDataList:
    #         if i.get('user_name') == inputUserName:
    #             theUserDict.update(user_name = i.get('user_name'))
    #             theUserDict.update(job_type = i.get('job_type'))
    #             theUserDict.update(location = i.get('location'))
    #             theUserDict.update(region = i.get('region'))
    #             theUserDict.update(org = i.get('org'))
    #             theUserDict.update(regular_exchange = i.get('regular_exchange'))
    #             theUserDict.update(extra_disk = i.get('extra_disk'))
    #             theUserDict.update(extra_disk_type = i.get('extra_disk_type'))
    #             theUserDict.update(extra_disk_capacity = i.get('extra_disk_capacity'))
    #             theUserDict.update(user_note = i.get('user_note'))
    #             break
    #     self._oneUserData = []
    #     self._oneUserData.append(theUserDict)
    #     self.showData()      # List with Dictionary items
    #     msg = f'사용자 [{inputUserName}]을(를) 조회하였습니다.'  # f-string
    #     self._msgLabel.setText(msg)
    #     self.__USER_EXIST__ = True
    #     self.__CURRENT_USER_NAME = inputUserName
    #     # self._userNameTextBox.setEnabled(False)
    #     self._btnRemove.setEnabled(True)
    #
    # def updateUsersList(self, theUserData, newUserFlag):
    #     if newUserFlag == None:
    #         return
    #
    #     userName = theUserData[0]
    #     # print(theUserData)
    #     theUserDict = {}
    #     # to make the data dictionary for the user
    #     theUserDict.update(user_name = theUserData[0])
    #     theUserDict.update(job_type = theUserData[1])
    #     theUserDict.update(org = theUserData[2])
    #     theUserDict.update(regular_exchange = theUserData[3])
    #     theUserDict.update(region = theUserData[4])
    #     theUserDict.update(location = theUserData[5])
    #     theUserDict.update(extra_disk = theUserData[6])
    #     theUserDict.update(extra_disk_type = theUserData[7])
    #     theUserDict.update(extra_disk_capacity = theUserData[8])
    #     theUserDict.update(user_note = theUserData[9])
    #     theUserDict.update(job_type_name = self._dictJobType.get(theUserData[1]))
    #     theUserDict.update(location_name = self._dictLocation.get(theUserData[5]))
    #     theUserDict.update(extra_disk_type_name = self._dictDiskType.get(theUserData[7]))
    #     theUserDict.update(extra_disk_capacity_name = self._dictDiskCapacity.get(theUserData[8]))
    #     theUserDict.update(region_name = self._dictRegion.get(theUserData[4]))
    #
    #     if newUserFlag == False:
    #         for i, row in enumerate(self._usersDataList):
    #             if row.get('user_name') == userName:
    #                 break
    #         self._usersDataList.remove(row)
    #         self._usersDataList.insert(i, theUserDict)
    #     else:
    #         self._usersDataList.append(theUserDict)
    #
    # def isExistent(self, theUserName):
    #     for i, row in enumerate(self._usersDataList):
    #         if row.get('user_name') == theUserName:
    #             return True
    #     return False
    #
    # def __clickedSave(self):
    #     inputUserName = self._userNameTextBox.text()
    #     if self.__CURRENT_USER_NAME != inputUserName and self.isExistent(inputUserName) == True:
    #         QMessageBox.warning(self, 'Mismatched Information',
    #                             '기존 사용자입니다. 사용자 정보를 조회 후 (변경)저장해 주십시오.\n'
    #                             '사용자명을 입력 후 엔터키를 누르거나 조회 버튼을 눌러 사용자 정보를 조회하십시오.')
    #         msg = '잘못된 사용자와 사용자 정보입니다.'
    #         self._msgLabel.setText(msg)
    #         return
    #
    #     # Set user data
    #     dataList = []
    #     dataList.append(inputUserName)
    #     dataList.append(str(self._jobComboBox.currentData()))
    #     # rowIndex = self._orgComboBox.currentIndex()
    #     # org = self._orgModel.item(rowIndex, 0)  # 0 - first column
    #     # dataList.append(org.text())
    #     # dataList.append(self._orgComboBox.currentText())
    #     dataList.append(self._regionComboBox.currentData())
    #     dataList.append(str(self._locationComboBox.currentData()))
    #     # if self._diskYesButton.isChecked() == True:
    #     #     dataList.append('Y')
    #     #     dataList.append(str(self._diskTypeComboBox.currentData()))
    #     #     dataList.append(str(self._diskCapacityComboBox.currentData()))
    #     # elif self._diskNoButton.isChecked() == True:
    #     #     dataList.append('N')
    #     #     dataList.append(None)
    #     #     dataList.append(None)
    #     dataList.append(self._noteEdit.text())
    #     newUserFlag = None
    #     try:
    #         db_connection = mysqlHandler.dbConnect()
    #         cursor = mysqlHandler.dbCursor(db_connection)
    #         if self.__USER_EXIST__ == True and self.__CURRENT_USER_NAME == inputUserName:         # Run "Update"
    #             dataList.append(inputUserName)  # user name in where-clause
    #             sql = 'update myasset.it_user set ' \
    #                   'user_name = %s, job_type = %s, org = %s, regular_exchange = %s, region = %s, ' \
    #                   'location = %s, extra_disk = %s, extra_disk_type = %s, extra_disk_capacity = %s, user_note = %s ' \
    #                   'where user_name = %s'
    #             newUserFlag = False
    #         elif self.__USER_EXIST__ == False or self.__CURRENT_USER_NAME != inputUserName:      # Run "Insert" as a new user
    #             sql = 'insert into myasset.it_user ' \
    #                   '(user_name, job_type, org, regular_exchange, region, location, extra_disk, extra_disk_type, extra_disk_capacity, user_note) values ' \
    #                   '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    #             newUserFlag = True
    #         cursor.execute(sql, dataList)
    #         db_connection.commit()
    #     except Exception as e:
    #         newUserFlag = None
    #         print(e)
    #     finally:
    #         db_connection.close()
    #
    #     msg = f'사용자 [{inputUserName}]을(를) 저장하였습니다.'  # f-string
    #     self._msgLabel.setText(msg)
    #     self.__USER_EXIST__ = True
    #     self.__CURRENT_USER_NAME = inputUserName
    #     self._btnRemove.setEnabled(True)
    #
    #     self.updateUsersList(dataList, newUserFlag)
    #     self.showUserTable()
    #
    # def __clickedRemove(self):
    #     if self.__USER_EXIST__ == True:
    #         inputUserName = self._userNameTextBox.text()
    #         try:
    #             db_connection = mysqlHandler.dbConnect()
    #             cursor = mysqlHandler.dbCursor(db_connection)
    #             sql = 'delete from myasset.it_user where user_name = %s'
    #             cursor.execute(sql, inputUserName)
    #             db_connection.commit()
    #             # to get rid of the user in the user list object
    #             self.removeUserList(inputUserName)
    #             self.showUserTable()
    #             msg = f'사용자 [{inputUserName}]을(를) 삭제하였습니다.'  # f-string
    #             self._msgLabel.setText(msg)
    #             self.initUIWidgets()
    #             self.__USER_EXIST__ == False
    #             self.__CURRENT_USER_NAME = None
    #         finally:
    #             db_connection.close()
    #
    # def removeUserList(self, theUserName):
    #     for i, row in enumerate(self._usersDataList):
    #         if row.get('user_name') == theUserName:
    #             break
    #     self._usersDataList.remove(row)
    #
    # def __jobSelected(self):
    #     pass
    #
    # def __diskTypeSelected(self):
    #     pass
    #
    # def __diskCapacitySelected(self):
    #     pass
    #
    # def __clickedDiskNo(self):
    #     self._diskTypeComboBox.clear()
    #     self._diskTypeComboBox.setEnabled(False)
    #     self._diskCapacityComboBox.clear()
    #     self._diskCapacityComboBox.setEnabled(False)
    #
    # def __clickedDiskYes(self):
    #     self.fillItems_DiskType()
    #     self._diskTypeComboBox.setEnabled(True)
    #     self.fillItems_DiskCapacity()
    #     self._diskCapacityComboBox.setEnabled(True)
    #
    # # to initiate input controls
    # def initUIWidgets(self):
    #     self._btn1Add.setEnabled(True)
    #     self._btn1Copy.setEnabled(True)
    #     self._btn1Modify.setEnabled(True)
    #     self._btn1Remove.setEnabled(False)
    #     self._userNameTextBox.clear()
    #     self._userNameTextBox.setEnabled(True)
    #     # self.fillItems_Org(self._orgList)
    #     # self._orgComboBox.setCurrentIndex(__NOT_SELECTED__)
    #     self.fillItems_Region()
    #     self._regionComboBox.setCurrentIndex(__NOT_SELECTED__)
    #     self.fillItems_JobType()
    #     self._jobComboBox.setCurrentIndex(__NOT_SELECTED__)
    #     self.fillItems_Location()
    #     self._locationComboBox.setCurrentIndex(__NOT_SELECTED__)
    #     # self._diskNoButton.setChecked(True)
    #     # self._diskYesButton.setChecked(False)
    #     self._diskTypeComboBox.setCurrentIndex(__NOT_SELECTED__)
    #     self._diskCapacityComboBox.setCurrentIndex(__NOT_SELECTED__)
    #     self._noteEdit.clear()
    #     self.__USER_EXIST__ = False

    # def showUserTable(self):
    #     self._userTableWidget.clearContents()
    #     self._userTableWidget.setRowCount(len(self._usersDataList))
    #     # print(self._usersDataList)
    #     for row, i in enumerate(self._usersDataList):
    #         userName = QTableWidgetItem(i.get('user_name'))
    #         orgName = QTableWidgetItem(i.get('org'))
    #         regionName = QTableWidgetItem(i.get('region_name'))
    #         locationName = QTableWidgetItem(i.get('location_name'))
    #         jobTypeName = QTableWidgetItem(i.get('job_type_name'))
    #         regularExchange = QTableWidgetItem(i.get('regular_exchange'))
    #         extraDisk = QTableWidgetItem(i.get('extra_disk'))
    #         extraDiskTypeName = QTableWidgetItem(i.get('extra_disk_type_name'))
    #         extraDiskCapacityName = QTableWidgetItem(i.get('extra_disk_capacity_name'))
    #         userNote = QTableWidgetItem(i.get('user_note'))
    #         jobTypeID = QTableWidgetItem(i.get('job_type'))
    #         region = QTableWidgetItem(i.get('region'))
    #         locationID = QTableWidgetItem(i.get('location'))
    #         extraDiskTypeID = QTableWidgetItem(i.get('extra_disk_type'))
    #         extraDiskCapacityID = QTableWidgetItem(i.get('extra_disk_capacity'))
    #         regularExchange.setTextAlignment(Qt.AlignCenter)
    #         extraDisk.setTextAlignment(Qt.AlignCenter)
    #         self._userTableWidget.setItem(row, 0, userName)
    #         self._userTableWidget.setItem(row, 1, orgName)
    #         self._userTableWidget.setItem(row, 2, regionName)
    #         self._userTableWidget.setItem(row, 3, locationName)
    #         self._userTableWidget.setItem(row, 4, jobTypeName)
    #         self._userTableWidget.setItem(row, 5, regularExchange)
    #         self._userTableWidget.setItem(row, 6, extraDisk)
    #         self._userTableWidget.setItem(row, 7, extraDiskTypeName)
    #         self._userTableWidget.setItem(row, 8, extraDiskCapacityName)
    #         self._userTableWidget.setItem(row, 9, userNote)
    #
    #     self._userTableWidget.resizeRowsToContents()
    #     self._userTableWidget.resizeColumnsToContents()

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    w = ItemMonitorWindow(None, '대성에너지')
    w.show()
    sys.exit(app.exec_())