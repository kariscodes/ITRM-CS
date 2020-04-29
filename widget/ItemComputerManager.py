import sys
from PyQt5.QtWidgets import *

from interface import mysqlHandler
from widget import CommonWidget, ItemMonitorManager, AssetItemCreator


__NOT_SELECTED__ = -1

class ItemComputerWindow(QWidget):
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
        self.setSignals()

    def composeLayout(self):

        lbl_Model = CommonWidget.SubtitleLabel('전산자원(Model)')
        lbl_Type = QLabel('품목 구분')
        self._typeComboBox = QComboBox()

        save1BtnFrame = QFrame()
        save1BtnLayout = QHBoxLayout()
        self.btn1Save = QPushButton('저장')
        save1BtnLayout.addWidget(self.btn1Save)
        save1BtnFrame.setLayout(save1BtnLayout)

        cmd1BtnFrame = QFrame()
        cmd1BtnLayout = QHBoxLayout()
        self._btn1Add = QPushButton('추가')
        self._btn1Copy = QPushButton('복사')
        self._btn1Modify = QPushButton('수정')
        self._btn1Remove = QPushButton('삭제')
        cmd1BtnLayout.addWidget(self._btn1Add)
        cmd1BtnLayout.addWidget(self._btn1Copy)
        cmd1BtnLayout.addWidget(self._btn1Modify)
        cmd1BtnLayout.addWidget(self._btn1Remove)
        cmd1BtnFrame.setLayout(cmd1BtnLayout)

        self._btnMultiAdd = QPushButton('다중 추가')

        save2BtnFrame = QFrame()
        save2BtnLayout = QHBoxLayout()
        self.btn2Save = QPushButton('저장')
        save2BtnLayout.addWidget(self.btn2Save)
        save2BtnFrame.setLayout(save2BtnLayout)

        cmd2BtnFrame = QFrame()
        cmd2BtnLayout = QHBoxLayout()
        self._btn2Add = QPushButton('추가')
        self._btn2Copy = QPushButton('복사')
        self._btn2Modify = QPushButton('수정')
        self._btn2Remove = QPushButton('삭제')
        cmd2BtnLayout.addWidget(self._btn2Add)
        cmd2BtnLayout.addWidget(self._btn2Copy)
        cmd2BtnLayout.addWidget(self._btn2Modify)
        cmd2BtnLayout.addWidget(self._btn2Remove)
        cmd2BtnFrame.setLayout(cmd2BtnLayout)

        cmd1Layout = QGridLayout()
        cmd1Layout.addWidget(lbl_Model, 0, 0, 1, 2)
        cmd1Layout.addWidget(save1BtnFrame, 0, 7)
        cmd1Layout.addWidget(lbl_Type, 1, 0)
        cmd1Layout.addWidget(self._typeComboBox, 1, 1)
        cmd1Layout.addWidget(cmd1BtnFrame, 1, 4, 1, 4)
        cmd1Layout.setColumnStretch(2, 1)   # 컬럼[2] stretch=1 / 나머지 컬럼은 width 고정, stretch=0 (default)

        self._modelTableWidget = QTableWidget()
        self._modelTableWidget.setSortingEnabled(True)            # 컬럼 헤더를 클릭하면 정렬이 되게 한다.
        self._modelTableWidget.setAlternatingRowColors(True)      # 행 색상이 번갈아 구분 표시되게 한다.
        # self._modelTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)      # Edit 금지
        # self._modelTableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)     # Row 단위로 선택이 표시되게 한다.
        self._modelTableWidget.setSelectionMode(QAbstractItemView.SingleSelection)    # 하나의 Row만 선택하게 함.
        self._modelTableWidget.setColumnCount(8)
        modelHeaderLabels = ['모델명', '품목', '세부구분', '프로세서', '타입', '운영체제',
                             '모니터크기', '비고']
        self._modelTableWidget.setHorizontalHeaderLabels(modelHeaderLabels)

        bodyTopLayout = QVBoxLayout()
        bodyTopLayout.addLayout(cmd1Layout)
        bodyTopLayout.addWidget(self._modelTableWidget)

        bodyTopFrame = QFrame()
        bodyTopFrame.setLayout(bodyTopLayout)
        bodyTopFrame.setFrameShape(QFrame.StyledPanel)
        bodyTopFrame.setFrameShadow(QFrame.Raised)
        bodyTopFrame.setLineWidth(3)
        bodyTopFrame.setMidLineWidth(3)

        lbl_SerialNo = CommonWidget.SubtitleLabel('전산자원(Serial Number)')

        cmd2Layout = QGridLayout()
        cmd2Layout.addWidget(lbl_SerialNo, 0, 0, 1, 2)
        cmd2Layout.addWidget(save2BtnFrame, 0, 7)
        cmd2Layout.addWidget(self._btnMultiAdd, 1, 3)
        cmd2Layout.addWidget(cmd2BtnFrame, 1, 4, 1, 4)
        cmd2Layout.setColumnStretch(2, 1)   # 컬럼[2] stretch=1 / 나머지 컬럼은 width 고정, stretch=0 (default)

        self._assetTableWidget = QTableWidget()
        self._assetTableWidget.setSortingEnabled(True)            # 컬럼 헤더를 클릭하면 정렬이 되게 한다.
        self._assetTableWidget.setAlternatingRowColors(True)      # 행 색상이 번갈아 구분 표시되게 한다.
        # self._assetTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)      # Edit 금지
        # self._assetTableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)     # Row 단위로 선택이 표시되게 한다.
        self._assetTableWidget.setSelectionMode(QAbstractItemView.SingleSelection)    # 하나의 Row만 선택하게 함.
        self._assetTableWidget.setColumnCount(12)
        assetHeaderLabels = ['일련번호', '자산명', '관리부문', '제조일', '입고일', '메모리', '디스크',
                             'MS Office', 'Hancom Office', '회계관리번호', '바코드', '비고']
        self._assetTableWidget.setHorizontalHeaderLabels(assetHeaderLabels)

        bodyBottomLayout = QVBoxLayout()
        bodyBottomLayout.addLayout(cmd2Layout)
        bodyBottomLayout.addWidget(self._assetTableWidget)

        bodyBottomFrame = QFrame()
        bodyBottomFrame.setLayout(bodyBottomLayout)
        bodyBottomFrame.setFrameShape(QFrame.StyledPanel)
        bodyBottomFrame.setFrameShadow(QFrame.Raised)
        bodyBottomFrame.setLineWidth(3)
        bodyBottomFrame.setMidLineWidth(3)

        winLayout = QVBoxLayout()
        winLayout.addWidget(bodyTopFrame)
        winLayout.addWidget(bodyBottomFrame)

        self.setLayout(winLayout)

    def initUIData(self):
        self._typeComboBox.setCurrentIndex(__NOT_SELECTED__)
        pass

    def setSignals(self):
        self._btnMultiAdd.clicked.connect(self.__clickedMultiAddItems)

    def __clickedMultiAddItems(self):
        try:
            # Modal Dialog
            self._assetItemCreatorDialog = AssetItemCreator.AssetItemCreatorWindow()
            self._assetItemCreatorDialog.exec_()
        except Exception as e:
            print(e)

    # to initiate input controls
    def initUIWidgets(self):
        self._typeComboBox.setCurrentIndex(__NOT_SELECTED__)
        self._btn1Add.setEnabled(True)
        self._btn1Copy.setEnabled(True)
        self._btn1Modify.setEnabled(True)
        self._btn1Remove.setEnabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    w = ItemComputerWindow(None, '대성에너지')
    w.show()
    sys.exit(app.exec_())