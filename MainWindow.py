import sys
from datetime import datetime
from PyQt5.QtWidgets import *
# from SubAcctWindow import SubAcctWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QIcon

from widget import CodeManager, UserManager, AcctManager, InfoManager, AssetManager, SQLReport, AnalysisReport, SystemManager

import Constants

__author__ = "Kyungho Lim <kyungho.lim@gmail.com>"

# create menu, tool bar, status bar
class MainWindow(QMainWindow):
    def __init__(self, company=None):
        super().__init__()
        if company:
            self._company = company
        else:
            self._company = 'DEMO'
        self.dockLogWindow = QDockWidget(self)
        # self.dockRunWindow = QDockWidget(self)
        # self.stateBar = QToolBar(self)
        # self.mainLayout = QStackedLayout(self)
        # self.mainWidget = QStackedWidget(self)
        # Multiple Document Interface
        self.mdi = QMdiArea()
        self.initUI()

    def initUI(self):
        # self.setFont(QFont('Times New Roman', 10))
        self.setWindowTitle(self._company + ' - ' + 'ITRM')
        # self.setWindowIcon(QIcon('./img/daesung.ico'))
        self.setWindowIcon(QIcon(Constants.BASE_PATH + '/img/daesung.ico'))
        self.statusBar().showMessage('Message in status bar')

        # Menus and Actions
        mainMenu = self.menuBar()

        fileMenu = mainMenu.addMenu('파일')
        editMenu = mainMenu.addMenu('등록')
        searchMenu = mainMenu.addMenu('조회')
        # self.workMenu = mainMenu.addMenu('작업창')
        setupMenu = mainMenu.addMenu('설정')
        helpMenu = mainMenu.addMenu('도움말')

        exitMenu = QAction(QIcon(Constants.BASE_PATH + '/img/exit.png'), '종료', self)
        # exitMenu.setStatusTip('Exit application')
        exitMenu.triggered.connect(self.close)
        fileMenu.addAction(exitMenu)

        acctMenu = QAction(QIcon(Constants.BASE_PATH + '/img/acct.png'), '자산취득등록', self)
        acctMenu.triggered.connect(self.acctWindow)
        editMenu.addAction(acctMenu)

        hwMenu = QAction(QIcon(Constants.BASE_PATH + '/img/hw.png'), '전산자원등록', self)
        hwMenu.triggered.connect(self.assetWindow)
        editMenu.addAction(hwMenu)

        swMenu = QAction(QIcon(Constants.BASE_PATH + '/img/sw.png'), '소프트웨어등록', self)
        # hwMenu.triggered.connect(self.softwareWindow)
        editMenu.addAction(swMenu)

        barcodeMenu = QAction(QIcon(Constants.BASE_PATH + '/img/barcode.png'), '바코드등록', self)
        # hwMenu.triggered.connect(self.tagAttachmentWindow)
        editMenu.addAction(barcodeMenu)

        view1Menu = QAction(QIcon(Constants.BASE_PATH + '/img/report_hw.png'), '전산자원현황', self)
        searchMenu.addAction(view1Menu)

        view2Menu = QAction(QIcon(Constants.BASE_PATH + '/img/report_sw.png'), '소프트웨어현황', self)
        searchMenu.addAction(view2Menu)

        analysisMenu = QAction(QIcon(Constants.BASE_PATH + '/img/sql.png'), 'Analysis Report', self)
        analysisMenu.triggered.connect(self.analysisWindow)
        searchMenu.addAction(analysisMenu)

        viewQueryMenu = QAction(QIcon(Constants.BASE_PATH + '/img/sql.png'), 'SQL Query Report', self)
        viewQueryMenu.triggered.connect(self.sqlReportWindow)
        searchMenu.addAction(viewQueryMenu)

        codeMenu = QAction(QIcon(Constants.BASE_PATH + '/img/code.png'), '공통코드관리', self)
        codeMenu.triggered.connect(self.codeWindow)
        setupMenu.addAction(codeMenu)

        userMenu = QAction(QIcon(Constants.BASE_PATH + '/img/user.png'), '사용자등록', self)
        userMenu.triggered.connect(self.userWindow)
        setupMenu.addAction(userMenu)

        passwordMenu = QAction(QIcon(Constants.BASE_PATH + '/img/user.png'), '비밀번호 변경', self)
        # passwordMenu.triggered.connect(self.userWindow)
        setupMenu.addAction(passwordMenu)

        sysMenu = QAction(QIcon(Constants.BASE_PATH + '/img/info.png'), '시스템 환경설정', self)
        sysMenu.triggered.connect(self.sysWindow)
        setupMenu.addAction(sysMenu)

        winStyleCascadeMenu = QAction('Window Cascade', self)
        winStyleCascadeMenu.triggered.connect(self.winStyleCascade)
        setupMenu.addAction(winStyleCascadeMenu)

        winStyleTileMenu = QAction('Window Tile', self)
        winStyleTileMenu.triggered.connect(self.winStyleTile)
        setupMenu.addAction(winStyleTileMenu)

        self._stateLogWindowMenu = QAction('작업로그 보이기/감추기', self)
        self._stateLogWindowMenu.setCheckable(True)
        self._stateLogWindowMenu.triggered.connect(self.stateLogWindow)
        setupMenu.addAction(self._stateLogWindowMenu)

        infoMenu = QAction(QIcon(Constants.BASE_PATH + '/img/info.png'), '정보', self)
        # infoMenu.setStatusTip("시스템 정보")
        infoMenu.triggered.connect(self.infoWindow)
        helpMenu.addAction(infoMenu)

        # Toolbar
        toolbar = QToolBar("Main Toolbar")
        toolbar.setAllowedAreas(Qt.TopToolBarArea)
        self.addToolBar(Qt.TopToolBarArea, toolbar)
        toolbar.addAction(acctMenu)
        toolbar.addAction(hwMenu)
        toolbar.addAction(swMenu)
        toolbar.addAction(barcodeMenu)
        toolbar.addAction(view1Menu)
        toolbar.addAction(view2Menu)
        toolbar.addAction(viewQueryMenu)
        toolbar.addAction(userMenu)
        toolbar.addAction(codeMenu)
        toolbar.addAction(infoMenu)
        toolbar.addAction(exitMenu)

        # # 중앙 위젯
        # # self.setCentralWidget(QWidget())
        # self.setCentralWidget(QTextEdit())

        # Dock - Log Window 설정
        self.dockLogWindow.setWindowTitle("System Log")
        self.txtLog = QTextEdit()
        self.txtLog.setTextBackgroundColor(QColor(255,255,255))
        self.txtLog.setTextColor(QColor(0,0,0))
        # self.txtLog.append('Waiting your input')
        self.dockLogWindow.setWidget(self.txtLog)
        # Dock이 붙을 수 있는 구역 설정
        # self.dockWorkingWindows.setAutoFillBackground(True)
        self.dockLogWindow.setAllowedAreas(
            Qt.TopDockWidgetArea | Qt.BottomDockWidgetArea | Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        # Dock의 처음 위치 설정
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dockLogWindow)

        if Constants.SHOW_LOG_VIEWER == True:            # 작업로그 윈도우 보이기
            self._stateLogWindowMenu.setChecked(True)
            self.dockLogWindow.show()
        elif Constants.SHOW_LOG_VIEWER == False:         # 작업로그 윈도우 감추기
            self._stateLogWindowMenu.setChecked(False)
            self.dockLogWindow.hide()

        # self.stateBar = QToolBar('Running Window')
        # self.stateBar.setAllowedAreas(Qt.LeftToolBarArea)
        # self.stateBar.setToolButtonStyle(Qt.ToolButtonTextOnly)
        # self.addToolBar(Qt.LeftToolBarArea, self.stateBar)

        # self.stateBar.addWidget(QPushButton('Test1'))
        # self.stateBar.addWidget(QPushButton('Test test tset 222'))
        # self.stateBar.addAction(QAction('Test2', self))
        # self.stateBar.addAction(QAction('Test3', self))

        # view = QListView()
        # view.setFixedWidth(120)
        # self.model = QStandardItemModel()
        # view.setModel(self.model)
        # self.stateBar.addWidget(view)
        # view.clicked.connect(self.slot_clicked_item)

        # view.resize(view.minimumSizeHint())
        # view.setResizeMode(QListView.Adjust)
        # view.showMinimized()
        # self.stateBar.resize(self.stateBar.minimumSizeHint())

        # self.setCentralWidget(self.mainWidget)
        self.setCentralWidget(self.mdi)

        # self.show()

    # @pyqtSlot(QModelIndex)
    # def slot_clicked_item(self, QModelIndex):
    #     self.mainWidget.setCurrentIndex(QModelIndex.row())

    def winStyleCascade(self):
        self.mdi.cascadeSubWindows()

    def winStyleTile(self):
        self.mdi.tileSubWindows()

    def stateLogWindow(self):
        if self._stateLogWindowMenu.isChecked():
            self.dockLogWindow.show()
        else:
            self.dockLogWindow.hide()

    # def windowChildClosed(self, childWindow):
    #     idx = self.mainWidget.indexOf(childWindow)
    #     self.mainWidget.removeWidget(childWindow)
    #     self.model.removeRow(idx)

    def sqlReportWindow(self):
        sub = QMdiSubWindow()
        childWindow = SQLReport.SQLReportWindow(self)
        sub.setWidget(childWindow)
        self.mdi.addSubWindow(sub)
        sub.show()
            # windowItem = QStandardItem('SQL Query Report')
            # self.model.appendRow(windowItem)
            # self.mainWidget.addWidget(childWindow)
            # self.mainWidget.setCurrentWidget(childWindow)
            # childWindow.show()
            # idx = self.mainWidget.currentIndex()
            # self.txtLog.append('SQL Query Report 실행' + '-- Current Index: ' + str(idx))
            # self.txtLog.append(str(datetime.now()) + '\t' + 'SQL Query Report 실행')

    def codeWindow(self):
        sub = QMdiSubWindow()
        childWindow = CodeManager.CodeWindow(self)
        sub.setWidget(childWindow)
        self.mdi.addSubWindow(sub)
        sub.show()
        # self.mainWidget.addWidget(childWindow)
        # self.mainWidget.setCurrentWidget(childWindow)
        # windowItem = QStandardItem('공통코드관리')
        # self.model.appendRow(windowItem)
        # childWindow.show()
        # self.txtLog.append(str(datetime.now()) + '\t' + '공통코드관리 화면 실행')

    def userWindow(self):
        sub = QMdiSubWindow()
        childWindow = UserManager.UserWindow(self)
        sub.setWidget(childWindow)
        self.mdi.addSubWindow(sub)
        sub.show()
        # self.mainWidget.addWidget(childWindow)
        # self.mainWidget.setCurrentWidget(childWindow)
        # windowItem = QStandardItem('사용자등록')
        # self.model.appendRow(windowItem)
        # childWindow.show()
        # self.txtLog.append(str(datetime.now()) + '\t' + '사용자등록 화면 실행')

    def acctWindow(self):
        sub = QMdiSubWindow()
        childWindow = AcctManager.AcctWindow(self)
        sub.setWidget(childWindow)
        self.mdi.addSubWindow(sub)
        sub.show()
            # self.model.appendRow(QStandardItem('자산취득등록'))
            # self.mainWidget.addWidget(childWindow)
            # self.mainWidget.setCurrentWidget(childWindow)
            # childWindow.show()
            # idx = self.mainWidget.currentIndex()
            # self.txtLog.append('자산취득등록 화면 실행' + '-- Current Index: ' + str(idx))
            # self.txtLog.append(str(datetime.now()) + '\t' + '자산취득등록 화면 실행')

    def assetWindow(self):
        sub = QMdiSubWindow()
        childWindow = AssetManager.AssetWindow(self)
        sub.setWidget(childWindow)
        self.mdi.addSubWindow(sub)
        sub.show()
        # self.model.appendRow(QStandardItem('전산자원등록'))
        # self.mainWidget.addWidget(childWindow)
        # self.mainWidget.setCurrentWidget(childWindow)
        # childWindow.show()
        # idx = self.mainWidget.currentIndex()
        # self.txtLog.append('전산자원등록 화면 실행' + '-- Current Index: ' + str(idx))
        # self.txtLog.append(str(datetime.now()) + '\t' + '전산자원등록 화면 실행')

    # Non-modal Dialog
    def analysisWindow(self):
        try:
            self._analysisWindow = AnalysisReport.AnalysisWindow(self)
            self._analysisWindow.show()
        except Exception as e:
            print(e)
        finally:
            self.txtLog.append(str(datetime.now()) + '\t' + 'Analysis Report 실행')

    # Modal Dialog
    def sysWindow(self):
        try:
            self.sysWin = SystemManager.SystemWindow(self)
            self.sysWin.exec_()
        except Exception as e:
            print(e)

    # Modal Dialog
    def infoWindow(self):
        try:
            self.infoWin = InfoManager.InfoWindow(self)
            self.infoWin.exec_()
        except Exception as e:
            print(e)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'Are you sure to quit?', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def show(self):
        self.showMaximized()
        super().show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    w = MainWindow('대성에너지')
    w.show()
    sys.exit(app.exec_())