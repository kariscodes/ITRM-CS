import os
import sys
import configparser

from PyQt5.QtWidgets import *
# from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import Constants

# 시스템 설정 유형별로 Tab 구성 (Tab 클래스 생성, Tab Widget에 추가)
# 환경설정 구성(setting) 저장(config.ini)
class SystemWindow(QDialog):
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

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self._company + ' - ' + '시스템 설정')
        self.setWindowIcon(QIcon(Constants.BASE_PATH + '/img/daesung.ico'))

        btnSave = QPushButton('저장')
        tabs = QTabWidget()
        self.tabAppSetup = SetupAppWindow()
        self.tabLogSetup = SetupLogWindow()
        tabs.addTab(self.tabAppSetup, 'Window')
        tabs.addTab(self.tabLogSetup, 'Log')

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(btnSave)
        mainLayout.addWidget(tabs)
        self.setLayout(mainLayout)

        btnSave.clicked.connect(self._clickedSave)

    def _clickedSave(self):
        self.saveConfiguration()

    def saveConfiguration(self):
        appValues = self.tabAppSetup.getValues()
        logValues = self.tabLogSetup.getValues()
        config = configparser.ConfigParser()
        # writing method 1
        config['window_style'] = {}
        config['window_style']['application_style'] = appValues.get('application_style')
        # writing method 2
        config['log'] = {
            'show_log_viewer': logValues.get('show_log_viewer')
        }
        # # writing method 1
        # config['window_style'] = {}
        # config['window_style']['application_style'] = 'Fusion'
        # # writing method 2
        # config['log'] = {
        #     'show_log_viewer': True         # 여러 항목일 경우에는 콤마(,)하고 다음줄에 작성
        # }
        with open(Constants.CONFIG_FILE, 'w') as configfile:
            config.write(configfile)  # clear file and rewrite

    """
    [window_style]
    application_style = Fusion

    [log]
    show_log_viewer = False
    """


class SetupAppWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initUIData()
        self.setSignals()

    def initUI(self):
        winLayout = QHBoxLayout()
        gridLayout = QGridLayout()
        self.lblWindowSyle = QLabel('윈도우 스타일')
        self.cmbWindowStyle = QComboBox()
        # self.lblWindowArray = QLabel('멀티윈도우 스타일')
        # self.cmbWindowArray = QComboBox()
        gridLayout.addWidget(self.lblWindowSyle, 0, 0)
        gridLayout.addWidget(self.cmbWindowStyle, 0, 1)
        # gridLayout.addWidget(self.lblWindowArray, 1, 0)
        # gridLayout.addWidget(self.cmbWindowArray, 1, 1)
        winLayout.addLayout(gridLayout)
        self.setLayout(winLayout)

    def initUIData(self):
        self.cmbWindowStyle.addItems(QStyleFactory.keys())
        self.cmbWindowStyle.setCurrentText(Constants.APPLICATION_STYLE)
        # self.cmbWindowArray.addItems(['cascade', 'tile'])
        # self.cmbWindowArray.setCurrentText(Constants.MULTI_WINDOW_STYLE)

    def setSignals(self):
        self.cmbWindowStyle.currentIndexChanged.connect(self._changeWindowStyle)
        # self.cmbWindowArray.currentIndexChanged.connect(self._changeWindowArray)

    def _changeWindowStyle(self):
        winStyle = self.cmbWindowStyle.currentText()
        QApplication.setStyle(winStyle)

    def getValues(self):
        values = {}
        values.update(application_style = self.cmbWindowStyle.currentText())
        return values
    # def _changeWindowArray(self):
    #     winArray = self.cmbWindowArray.currentText()

class SetupLogWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initUIData()

    def initUI(self):
        winLayout = QHBoxLayout()
        gridLayout = QGridLayout()
        viewLogBox = QGroupBox()
        viewLogLayout = QVBoxLayout()
        self.showLog = QRadioButton('로그 보이기')
        self.hideLog = QRadioButton('로그 감추기')
        viewLogLayout.addWidget(self.showLog)
        viewLogLayout.addWidget(self.hideLog)
        viewLogBox.setTitle('로그 표시')
        viewLogBox.setLayout(viewLogLayout)
        gridLayout.addWidget(viewLogBox, 0, 0)
        winLayout.addLayout(gridLayout)
        self.setLayout(winLayout)

    def initUIData(self):
        if Constants.SHOW_LOG_VIEWER == True:
            self.showLog.setChecked(True)
        elif Constants.SHOW_LOG_VIEWER == False:
            self.hideLog.setChecked(True)

    def getValues(self):
        values = {}
        if self.showLog.isChecked():
            logViewer = True
        elif self.hideLog.isChecked():
            logViewer = False
        values.update(show_log_viewer = logViewer)
        return values


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = SystemWindow(None, '대성에너지')
    # w = InfoWindow()
    w.show()
    sys.exit(app.exec_())