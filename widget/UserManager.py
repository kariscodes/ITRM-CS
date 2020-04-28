import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
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

class UserWindow(QWidget):
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
        self.setWindowTitle(self._company + ' - ' + '사용자등록')
        self.setWindowIcon(QIcon(Constants.BASE_PATH + '/img/daesung.ico'))

        self.composeLayout()
        self.initUIData()
        self.initUIWidgets()
        self.setSignals()
        self.loadUsers()
        self.__CURRENT_USER_NAME = None

    def composeLayout(self):

        titleLayout = CommonWidget.TitleLayout('사용자등록')

        self._msgLabel = QLabel()
        self._msgLabel.setText('사용자등록 화면입니다.')
        # self._msgLabel.resize(self._msgLabel.sizeHint())
        # self._msgLabel.setFixedHeight(30)
        msgLayout = QVBoxLayout()
        msgLayout.addWidget(self._msgLabel)
        # msgLayout.addWidget(msgFrame)
        # msgLayout.setAlignment(Qt.AlignLeft)
        msgFrame = QFrame()
        msgFrame.setFixedHeight(35)
        # msgFrame.setFrameShape(QFrame.StyledPanel)
        # msgFrame.setFrameShadow(QFrame.Sunken)
        # msgFrame.setLineWidth(1)
        # msgFrame.setMidLineWidth(3)
        # msgFrame.setStyleSheet('background-color: gray;'
        #                        'color: white')
        msgFrame.setLayout(msgLayout)

        cmdBtnLayout = QHBoxLayout()
        self._btnNew = QPushButton('신규')
        self._btnSearch = QPushButton('조회')
        self._btnSave = QPushButton('저장')
        self._btnRemove = QPushButton('삭제')
        cmdBtnLayout.addWidget(self._btnNew)
        cmdBtnLayout.addWidget(self._btnSearch)
        cmdBtnLayout.addWidget(self._btnSave)
        cmdBtnLayout.addWidget(self._btnRemove)

        # radio buttons
        regularGroup = QFrame()
        regularLayout = QHBoxLayout()
        self._regularYesButton = QRadioButton('대상')
        self._regularNoButton = QRadioButton('비대상')
        regularLayout.addWidget(self._regularYesButton)
        regularLayout.addWidget(self._regularNoButton)
        regularLayout.addStretch(1)
        regularGroup.setLayout(regularLayout)

        # radio buttons
        diskGroup = QFrame()
        diskLayout = QHBoxLayout()
        self._diskNoButton = QRadioButton('N(무)')
        self._diskYesButton = QRadioButton('Y(유)')
        diskLayout.addWidget(self._diskNoButton)
        diskLayout.addWidget(self._diskYesButton)
        diskLayout.addStretch(1)
        diskGroup.setLayout(diskLayout)

        # input widgets
        self._userNameTextBox = QLineEdit()
        self._jobComboBox = QComboBox()
        self._orgComboBox = QComboBox()
        self._diskTypeComboBox = QComboBox()
        self._diskCapacityComboBox = QComboBox()
        self._regionComboBox = QComboBox()
        self._locationComboBox = QComboBox()
        self._noteEdit = QLineEdit()
        lbl_User = QLabel('사용자')
        lbl_Job = QLabel('직무구분')
        lbl_Regular = QLabel('정기교체')
        lbl_Org = QLabel('부서')
        lbl_Region = QLabel('지역')
        lbl_Location = QLabel('상세위치')
        lbl_ExtraDisk = QLabel('증설 디스크')
        lbl_DiskType = QLabel('디스크 유형')
        lbl_DiskCapacity = QLabel('디스크 용량')
        lbl_Note = QLabel('비고')

        inputLayout = QGridLayout()
        inputLayout.addWidget(lbl_User, 0, 0)
        inputLayout.addWidget(self._userNameTextBox, 0, 1)
        inputLayout.addWidget(lbl_Job, 0, 2)
        inputLayout.addWidget(self._jobComboBox, 0, 3)
        inputLayout.addWidget(lbl_Regular, 0, 4)
        inputLayout.addWidget(regularGroup, 0, 5)
        inputLayout.addWidget(lbl_Org, 1, 0)
        inputLayout.addWidget(self._orgComboBox, 1, 1)
        inputLayout.addWidget(lbl_Region, 1, 2)
        inputLayout.addWidget(self._regionComboBox, 1, 3)
        inputLayout.addWidget(lbl_Location, 1, 4)
        inputLayout.addWidget(self._locationComboBox, 1, 5)
        inputLayout.addWidget(lbl_ExtraDisk, 2, 0)
        inputLayout.addWidget(diskGroup, 2, 1)
        inputLayout.addWidget(lbl_DiskType, 2, 2)
        inputLayout.addWidget(self._diskTypeComboBox, 2, 3)
        inputLayout.addWidget(lbl_DiskCapacity, 2, 4)
        inputLayout.addWidget(self._diskCapacityComboBox, 2, 5)
        inputLayout.addWidget(lbl_Note, 3, 0)
        inputLayout.addWidget(self._noteEdit, 3, 1, 1, 5)
        inputLayout.setColumnStretch(0, 0)
        inputLayout.setColumnStretch(1, 1)
        inputLayout.setColumnStretch(2, 0)
        inputLayout.setColumnStretch(3, 1)
        inputLayout.setColumnStretch(4, 0)
        inputLayout.setColumnStretch(5, 1)

        bodyTopFrame = QFrame()
        bodyTopFrame.setLayout(inputLayout)
        bodyTopFrame.setFrameShape(QFrame.StyledPanel)
        bodyTopFrame.setFrameShadow(QFrame.Raised)
        bodyTopFrame.setLineWidth(3)
        bodyTopFrame.setMidLineWidth(3)

        self._userTableWidget = QTableWidget()
        self._userTableWidget.setSortingEnabled(True)            # 컬럼 헤더를 클릭하면 정렬이 되게 한다.
        self._userTableWidget.setAlternatingRowColors(True)      # 행 색상이 번갈아 구분 표시되게 한다.
        self._userTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)      # Edit 금지
        self._userTableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)     # Row 단위로 선택이 표되게 한다.
        self._userTableWidget.setSelectionMode(QAbstractItemView.SingleSelection)    # 하나의 Row만 선택하게 함.
        self._userTableWidget.setColumnCount(10)    # 10개 항목 보여주고 5개 항목은 감춘다.
        self._userTableWidget.setHorizontalHeaderLabels(
            ['사용자', '조직', '지역', '위치', '직무', '정기교체대상',
             '디스크증설', '증설디스크유형', '증설디스크용량', '비고'])
        # self._userTableWidget.setHorizontalHeaderLabels(
        #     ['사용자', '조직', '지역', '위치', '직무', '정기교체대상',
        #      '디스크증설', '증설디스크유형', '증설디스크용량', '비고',
        #      '직무ID', '지역ID', '위치ID', '증설디스크유형ID', '증설디스크용량ID'])

        bodyBottomFrame = QFrame()
        bodyBottomLayout = QVBoxLayout()
        bodyBottomLayout.addWidget(self._userTableWidget)
        bodyBottomFrame.setLayout(bodyBottomLayout)

        # bodySplitter = QSplitter(Qt.Vertical)
        # bodySplitter.addWidget(bodyTopFrame)
        # bodySplitter.addWidget(bodyBottomFrame)

        winLayout = QVBoxLayout()
        winLayout.addLayout(titleLayout)
        # winLayout.addLayout(msgLayout)
        winLayout.addWidget(msgFrame)
        winLayout.addLayout(cmdBtnLayout)
        # winLayout.addWidget(bodySplitter)
        winLayout.addWidget(bodyTopFrame)
        winLayout.addWidget(bodyBottomFrame)
        # winLayout.setStretchFactor(bodySplitter, 2)
        # winLayout.addStretch(0)

        # sizePolicy = QSizePolicy()
        # sizePolicy.setVerticalPolicy(QSizePolicy.Minimum)
        # sizePolicy.setVerticalStretch(0)
        # self._userNameTextBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # bodyTopFrame.setSizePolicy(sizePolicy)
        # self._userNameTextBox.setSizePolicy(sizePolicy)
        # lblUser.setSizePolicy(sizePolicy)
        # self._jobComboBox.setSizePolicy(sizePolicy)
        # lblJob.setSizePolicy(sizePolicy)
        # regularGroup.setSizePolicy(sizePolicy)
        # lblRegular.setSizePolicy(sizePolicy)
        # self._userTableWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.setLayout(winLayout)

    def initUIData(self):

        # Open DB Connection
        db_connection = mysqlHandler.dbConnect()
        cursor_dict = mysqlHandler.dbDictCursor(db_connection)

        # Codes
        sql = 'select code_type, code_id, code_name from myasset.common_code ' \
              'order by code_type, code_id'
        cursor_dict.execute(sql)
        codeDict = cursor_dict.fetchall()
        # to create dictionary with key-value pair (code id, code name)
        self._dictJobType = {}
        self._dictDiskType = {}
        self._dictDiskCapacity = {}
        self._dictLocation = {}
        for i in codeDict:
            if i.get('code_type') == 'job_type':
                self._dictJobType[i.get('code_id')] = i.get('code_name')
            if i.get('code_type') == 'disk_type':
                self._dictDiskType[i.get('code_id')] = i.get('code_name')
            if i.get('code_type') == 'disk_capacity':
                self._dictDiskCapacity[i.get('code_id')] = i.get('code_name')
            if i.get('code_type') == 'location':
                self._dictLocation[i.get('code_id')] = i.get('code_name')
        self.fillItems_JobType()
        self.fillItems_DiskType()
        self.fillItems_DiskCapacity()
        self.fillItems_Location()

        # Region
        sql = 'select region, region_name from myasset.region order by region_name'
        cursor_dict.execute(sql)
        codeDict = cursor_dict.fetchall()
        self._dictRegion = {}
        for i in codeDict:
            self._dictRegion[i.get('region')] = i.get('region_name')
        self.fillItems_Region()

        # Org
        # sql = 'select org, super_org1, super_org2 from myasset.it_user_org order by org, super_org1, super_org2'
        sql = 'select org from myasset.it_user_org order by org'
        cursor_dict.execute(sql)
        self._orgList = cursor_dict.fetchall()
        self.fillItems_Org(self._orgList)

        # Close DB Connection
        db_connection.close()

    def setSignals(self):
        # self._btnClose.clicked.connect(self.close)  # closeEvent
        self._btnNew.clicked.connect(self.__clickedNew)
        self._btnSearch.clicked.connect(self.__clickedSearch)
        self._btnSave.clicked.connect(self.__clickedSave)
        self._btnRemove.clicked.connect(self.__clickedRemove)
        self._jobComboBox.currentIndexChanged.connect(self.__jobSelected)
        self._diskTypeComboBox.currentIndexChanged.connect(self.__diskTypeSelected)
        self._diskCapacityComboBox.currentIndexChanged.connect(self.__diskCapacitySelected)
        self._diskNoButton.clicked.connect(self.__clickedDiskNo)
        self._diskYesButton.clicked.connect(self.__clickedDiskYes)
        self._userNameTextBox.returnPressed.connect(self.__userNameEntered)
        self._userTableWidget.cellClicked.connect(self.__clickedTableWidget)

    # def closeEvent(self, event):
    #     # if self._parent != None:
    #     #     self._parent.windowChildClosed(self)
    #     event.accept()
    #     print("Closed")
    #
    # def __textEdited(self):
    #     self.enableOperation(True)

    def __clickedNew(self):
        self.initUIWidgets()
        self.__CURRENT_USER_NAME = None
        self._msgLabel.setText('신규 사용자를 입력할 준비가 되었습니다.')

    def __userNameEntered(self):
        self.search()

    def __clickedSearch(self):
        self.search()

    def search(self):
        inputUserName = self._userNameTextBox.text()
        if len(inputUserName) == 0:
            QMessageBox.warning(self, 'No User Name',
                                '사용자명을 입력 후 엔터키를 누르거나 조회 버튼을 눌러 사용자 정보를 조회하십시오.')
            msg = '사용자명을 입력하세요.'
            self._msgLabel.setText(msg)
            return

        self.__CURRENT_USER_NAME = inputUserName
        self._oneUserData = self.dbLoad(inputUserName)  # List with Dictionary items
        if len(self._oneUserData) != 0:
            self.showData()
            msg = f'사용자 [{inputUserName}]을(를) 조회하였습니다.'  # f-string
            self._msgLabel.setText(msg)
            self.__USER_EXIST__ = True
            self._btnRemove.setEnabled(True)
        else:
            msg = '사용자를 조회할 수 없습니다.'
            self._msgLabel.setText(msg)
            self.initUIWidgets()
            self.__USER_EXIST__ = False
            self._btnRemove.setEnabled(False)

    def loadUsers(self, specificUserName=None):
        self._usersDataList = self.dbLoad()     # List with Dictionary items
        self.showUserTable()

    def dbLoad(self, specificUserName=None):
        try:
            db_connection = mysqlHandler.dbConnect()
            cursor_dict = mysqlHandler.dbDictCursor(db_connection)
            sql = 'select ' \
                  ' user_name, ' \
                  ' job_type, ' \
                  ' org, ' \
                  ' regular_exchange, ' \
                  ' region, ' \
                  ' location, ' \
                  ' extra_disk, ' \
                  ' extra_disk_type, ' \
                  ' extra_disk_capacity, ' \
                  ' user_note '
            if specificUserName:
                sql += ' from myasset.it_user where user_name = %s'
                cursor_dict.execute(sql, specificUserName)
            else:
                sql += ' from myasset.it_user order by user_name'
                cursor_dict.execute(sql)
        finally:
            db_connection.close()

        data = cursor_dict.fetchall()   # List with Dictionary items
        # to add key-value pairs : code id(key)에 대응하는 name(value)
        for i, row in enumerate(data):
            row['job_type_name'] = self._dictJobType.get(row.get('job_type'))
            row['location_name'] = self._dictLocation.get(row.get('location'))
            row['extra_disk_type_name'] = self._dictDiskType.get(row.get('extra_disk_type'))
            row['extra_disk_capacity_name'] = self._dictDiskCapacity.get(row.get('extra_disk_capacity'))
            row['region_name'] = self._dictRegion.get(row.get('region'))

        return data

    def showData(self):
        if len(self._oneUserData) != 1:
            return
        r = self._oneUserData[0]
        self._userNameTextBox.setText(r.get('user_name'))
        self._noteEdit.setText(r.get('user_note'))
        self._jobComboBox.setCurrentIndex(self._jobComboBox.findData(r.get('job_type')))
        self._locationComboBox.setCurrentIndex(self._locationComboBox.findData(r.get('location')))
        self._regionComboBox.setCurrentText(r.get('region'))
        self._orgComboBox.setCurrentText(r.get('org'))
        if r.get('regular_exchange') == '대상':
            self._regularYesButton.setChecked(True)
            self._regularNoButton.setChecked(False)
        elif r.get('regular_exchange') == '비대상':
            self._regularYesButton.setChecked(False)
            self._regularNoButton.setChecked(True)
        if r.get('extra_disk') == 'Y':
            self._diskYesButton.setChecked(True)
            self._diskNoButton.setChecked(False)
            self._diskTypeComboBox.setEnabled(True)
            self._diskCapacityComboBox.setEnabled(True)
            self.fillItems_DiskType()
            self.fillItems_DiskCapacity()
            self._diskTypeComboBox.setCurrentIndex(self._diskTypeComboBox.findData(r.get('extra_disk_type')))
            self._diskCapacityComboBox.setCurrentIndex(self._diskCapacityComboBox.findData(r.get('extra_disk_capacity')))
        elif r.get('extra_disk') == 'N':
            self._diskYesButton.setChecked(False)
            self._diskNoButton.setChecked(True)
            self._diskTypeComboBox.setEnabled(False)
            self._diskCapacityComboBox.setEnabled(False)
            self._diskTypeComboBox.setCurrentIndex(__NOT_SELECTED__)
            self._diskCapacityComboBox.setCurrentIndex(__NOT_SELECTED__)

    def keyReleaseEvent(self, e):
        if e.key() == Qt.Key_Down or e.key() == Qt.Key_Up:
            self.__clickedTableWidget()

    # 사용자 데이터 표시
    def __clickedTableWidget(self):
        row = self._userTableWidget.currentRow()
        userNameItem = self._userTableWidget.item(row, 0)
        inputUserName = userNameItem.text()
        theUserDict = {}
        for i in self._usersDataList:
            if i.get('user_name') == inputUserName:
                theUserDict.update(user_name = i.get('user_name'))
                theUserDict.update(job_type = i.get('job_type'))
                theUserDict.update(location = i.get('location'))
                theUserDict.update(region = i.get('region'))
                theUserDict.update(org = i.get('org'))
                theUserDict.update(regular_exchange = i.get('regular_exchange'))
                theUserDict.update(extra_disk = i.get('extra_disk'))
                theUserDict.update(extra_disk_type = i.get('extra_disk_type'))
                theUserDict.update(extra_disk_capacity = i.get('extra_disk_capacity'))
                theUserDict.update(user_note = i.get('user_note'))
                break
        self._oneUserData = []
        self._oneUserData.append(theUserDict)
        self.showData()      # List with Dictionary items
        msg = f'사용자 [{inputUserName}]을(를) 조회하였습니다.'  # f-string
        self._msgLabel.setText(msg)
        self.__USER_EXIST__ = True
        self.__CURRENT_USER_NAME = inputUserName
        # self._userNameTextBox.setEnabled(False)
        self._btnRemove.setEnabled(True)

    def updateUsersList(self, theUserData, newUserFlag):
        if newUserFlag == None:
            return

        userName = theUserData[0]
        # print(theUserData)
        theUserDict = {}
        # to make the data dictionary for the user
        theUserDict.update(user_name = theUserData[0])
        theUserDict.update(job_type = theUserData[1])
        theUserDict.update(org = theUserData[2])
        theUserDict.update(regular_exchange = theUserData[3])
        theUserDict.update(region = theUserData[4])
        theUserDict.update(location = theUserData[5])
        theUserDict.update(extra_disk = theUserData[6])
        theUserDict.update(extra_disk_type = theUserData[7])
        theUserDict.update(extra_disk_capacity = theUserData[8])
        theUserDict.update(user_note = theUserData[9])
        theUserDict.update(job_type_name = self._dictJobType.get(theUserData[1]))
        theUserDict.update(location_name = self._dictLocation.get(theUserData[5]))
        theUserDict.update(extra_disk_type_name = self._dictDiskType.get(theUserData[7]))
        theUserDict.update(extra_disk_capacity_name = self._dictDiskCapacity.get(theUserData[8]))
        theUserDict.update(region_name = self._dictRegion.get(theUserData[4]))

        if newUserFlag == False:
            for i, row in enumerate(self._usersDataList):
                if row.get('user_name') == userName:
                    break
            self._usersDataList.remove(row)
            self._usersDataList.insert(i, theUserDict)
        else:
            self._usersDataList.append(theUserDict)

    def isExistent(self, theUserName):
        for i, row in enumerate(self._usersDataList):
            if row.get('user_name') == theUserName:
                return True
        return False

    def __clickedSave(self):
        inputUserName = self._userNameTextBox.text()
        if self.__CURRENT_USER_NAME != inputUserName and self.isExistent(inputUserName) == True:
            QMessageBox.warning(self, 'Mismatched Information',
                                '기존 사용자입니다. 사용자 정보를 조회 후 (변경)저장해 주십시오.\n'
                                '사용자명을 입력 후 엔터키를 누르거나 조회 버튼을 눌러 사용자 정보를 조회하십시오.')
            msg = '잘못된 사용자와 사용자 정보입니다.'
            self._msgLabel.setText(msg)
            return

        # Set user data
        dataList = []
        dataList.append(inputUserName)
        dataList.append(str(self._jobComboBox.currentData()))
        # rowIndex = self._orgComboBox.currentIndex()
        # org = self._orgModel.item(rowIndex, 0)  # 0 - first column
        # dataList.append(org.text())
        dataList.append(self._orgComboBox.currentText())
        if self._regularYesButton.isChecked() == True:
            dataList.append('대상')
        elif self._regularNoButton.isChecked() == True:
            dataList.append('비대상')
        dataList.append(self._regionComboBox.currentData())
        dataList.append(str(self._locationComboBox.currentData()))
        if self._diskYesButton.isChecked() == True:
            dataList.append('Y')
            dataList.append(str(self._diskTypeComboBox.currentData()))
            dataList.append(str(self._diskCapacityComboBox.currentData()))
        elif self._diskNoButton.isChecked() == True:
            dataList.append('N')
            dataList.append(None)
            dataList.append(None)
        dataList.append(self._noteEdit.text())
        newUserFlag = None
        try:
            db_connection = mysqlHandler.dbConnect()
            cursor = mysqlHandler.dbCursor(db_connection)
            if self.__USER_EXIST__ == True and self.__CURRENT_USER_NAME == inputUserName:         # Run "Update"
                dataList.append(inputUserName)  # user name in where-clause
                sql = 'update myasset.it_user set ' \
                      'user_name = %s, job_type = %s, org = %s, regular_exchange = %s, region = %s, ' \
                      'location = %s, extra_disk = %s, extra_disk_type = %s, extra_disk_capacity = %s, user_note = %s ' \
                      'where user_name = %s'
                newUserFlag = False
            elif self.__USER_EXIST__ == False or self.__CURRENT_USER_NAME != inputUserName:      # Run "Insert" as a new user
                sql = 'insert into myasset.it_user ' \
                      '(user_name, job_type, org, regular_exchange, region, location, extra_disk, extra_disk_type, extra_disk_capacity, user_note) values ' \
                      '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                newUserFlag = True
            cursor.execute(sql, dataList)
            db_connection.commit()
        except Exception as e:
            newUserFlag = None
            print(e)
        finally:
            db_connection.close()

        msg = f'사용자 [{inputUserName}]을(를) 저장하였습니다.'  # f-string
        self._msgLabel.setText(msg)
        self.__USER_EXIST__ = True
        self.__CURRENT_USER_NAME = inputUserName
        self._btnRemove.setEnabled(True)

        self.updateUsersList(dataList, newUserFlag)
        self.showUserTable()

    def __clickedRemove(self):
        if self.__USER_EXIST__ == True:
            inputUserName = self._userNameTextBox.text()
            try:
                db_connection = mysqlHandler.dbConnect()
                cursor = mysqlHandler.dbCursor(db_connection)
                sql = 'delete from myasset.it_user where user_name = %s'
                cursor.execute(sql, inputUserName)
                db_connection.commit()
                # to get rid of the user in the user list object
                self.removeUserList(inputUserName)
                self.showUserTable()
                msg = f'사용자 [{inputUserName}]을(를) 삭제하였습니다.'  # f-string
                self._msgLabel.setText(msg)
                self.initUIWidgets()
                self.__USER_EXIST__ == False
                self.__CURRENT_USER_NAME = None
            finally:
                db_connection.close()

    def removeUserList(self, theUserName):
        for i, row in enumerate(self._usersDataList):
            if row.get('user_name') == theUserName:
                break
        self._usersDataList.remove(row)

    def __jobSelected(self):
        pass

    def __diskTypeSelected(self):
        pass

    def __diskCapacitySelected(self):
        pass

    def __clickedDiskNo(self):
        self._diskTypeComboBox.clear()
        self._diskTypeComboBox.setEnabled(False)
        self._diskCapacityComboBox.clear()
        self._diskCapacityComboBox.setEnabled(False)

    def __clickedDiskYes(self):
        self.fillItems_DiskType()
        self._diskTypeComboBox.setEnabled(True)
        self.fillItems_DiskCapacity()
        self._diskCapacityComboBox.setEnabled(True)

    # to initiate input controls
    def initUIWidgets(self):
        self._btnNew.setEnabled(True)
        self._btnSearch.setEnabled(True)
        self._btnSave.setEnabled(True)
        self._btnRemove.setEnabled(False)
        self._userNameTextBox.clear()
        self._userNameTextBox.setEnabled(True)
        self._regularYesButton.setChecked(True)
        self._regularNoButton.setChecked(False)
        self.fillItems_Org(self._orgList)
        self._orgComboBox.setCurrentIndex(__NOT_SELECTED__)
        self.fillItems_Region()
        self._regionComboBox.setCurrentIndex(__NOT_SELECTED__)
        self.fillItems_JobType()
        self._jobComboBox.setCurrentIndex(__NOT_SELECTED__)
        self.fillItems_Location()
        self._locationComboBox.setCurrentIndex(__NOT_SELECTED__)
        self._diskNoButton.setChecked(True)
        self._diskYesButton.setChecked(False)
        self._diskTypeComboBox.setCurrentIndex(__NOT_SELECTED__)
        self._diskCapacityComboBox.setCurrentIndex(__NOT_SELECTED__)
        self._noteEdit.clear()
        self.__USER_EXIST__ = False

    def fillItems_JobType(self):
        self._jobComboBox.clear()
        for key, value in self._dictJobType.items():
            self._jobComboBox.addItem(value, key)

    def fillItems_DiskType(self):
        self._diskTypeComboBox.clear()
        for key, value in self._dictDiskType.items():
            self._diskTypeComboBox.addItem(value, key)

    def fillItems_DiskCapacity(self):
        self._diskCapacityComboBox.clear()
        for key, value in self._dictDiskCapacity.items():
            self._diskCapacityComboBox.addItem(value, key)

    def fillItems_Location(self):
        self._locationComboBox.clear()
        for key, value in self._dictLocation.items():
            self._locationComboBox.addItem(value, key)

    def fillItems_Region(self):
        self._regionComboBox.clear()
        for key, value in self._dictRegion.items():
            self._regionComboBox.addItem(value, key)

    def fillItems_Org(self, theList):
        self._orgComboBox.clear()
        for r in theList:
            self._orgComboBox.addItem(r.get('org'))

    def showUserTable(self):
        self._userTableWidget.clearContents()
        self._userTableWidget.setRowCount(len(self._usersDataList))
        # print(self._usersDataList)
        for row, i in enumerate(self._usersDataList):
            userName = QTableWidgetItem(i.get('user_name'))
            orgName = QTableWidgetItem(i.get('org'))
            regionName = QTableWidgetItem(i.get('region_name'))
            locationName = QTableWidgetItem(i.get('location_name'))
            jobTypeName = QTableWidgetItem(i.get('job_type_name'))
            regularExchange = QTableWidgetItem(i.get('regular_exchange'))
            extraDisk = QTableWidgetItem(i.get('extra_disk'))
            extraDiskTypeName = QTableWidgetItem(i.get('extra_disk_type_name'))
            extraDiskCapacityName = QTableWidgetItem(i.get('extra_disk_capacity_name'))
            userNote = QTableWidgetItem(i.get('user_note'))
            jobTypeID = QTableWidgetItem(i.get('job_type'))
            region = QTableWidgetItem(i.get('region'))
            locationID = QTableWidgetItem(i.get('location'))
            extraDiskTypeID = QTableWidgetItem(i.get('extra_disk_type'))
            extraDiskCapacityID = QTableWidgetItem(i.get('extra_disk_capacity'))
            regularExchange.setTextAlignment(Qt.AlignCenter)
            extraDisk.setTextAlignment(Qt.AlignCenter)
            self._userTableWidget.setItem(row, 0, userName)
            self._userTableWidget.setItem(row, 1, orgName)
            self._userTableWidget.setItem(row, 2, regionName)
            self._userTableWidget.setItem(row, 3, locationName)
            self._userTableWidget.setItem(row, 4, jobTypeName)
            self._userTableWidget.setItem(row, 5, regularExchange)
            self._userTableWidget.setItem(row, 6, extraDisk)
            self._userTableWidget.setItem(row, 7, extraDiskTypeName)
            self._userTableWidget.setItem(row, 8, extraDiskCapacityName)
            self._userTableWidget.setItem(row, 9, userNote)
            # self._userTableWidget.setItem(row, 10, jobTypeID)
            # self._userTableWidget.setItem(row, 11, region)
            # self._userTableWidget.setItem(row, 12, locationID)
            # self._userTableWidget.setItem(row, 13, extraDiskTypeID)
            # self._userTableWidget.setItem(row, 14, extraDiskCapacityID)

        self._userTableWidget.resizeRowsToContents()
        self._userTableWidget.resizeColumnsToContents()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    w = UserWindow(None, '대성에너지')
    w.show()
    sys.exit(app.exec_())