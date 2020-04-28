import os
import sys

import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QAbstractTableModel, pyqtSlot
from PyQt5.QtGui import QIcon

from interface import mysqlHandler
from widget import CommonWidget

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import Constants

class pandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role:Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

class SQLReportWindow(QWidget):
    def __init__(self, parent=None, company=None):
        super().__init__(parent)
        # self.setWindowModality(Qt.NonModal)     # to set non-modal dialog

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
        self.setWindowTitle(self._company + ' - ' + 'Dynamic SQL Report')
        self.setWindowIcon(QIcon(Constants.BASE_PATH + '/img/daesung.ico'))

        titleLayout = CommonWidget.TitleLayout('Dynamic SQL Report')

        topLeftFrame = QFrame()
        topRightFrame = QFrame()
        bottomFrame = QFrame()

        splitHorizontal = QSplitter(Qt.Horizontal)
        splitHorizontal.addWidget(topLeftFrame)
        splitHorizontal.addWidget(topRightFrame)

        mainFrame = QSplitter(Qt.Vertical)
        # mainFrame.addWidget(title)
        mainFrame.addWidget(splitHorizontal)
        mainFrame.addWidget(bottomFrame)

        buttonLayout = QHBoxLayout()
        self._sujectLabel = CommonWidget.SubtitleLabel('SQL Query')
        btnRun = QPushButton('쿼리 실행')
        btnRun.resize(btnRun.sizeHint())
        btnRun.clicked.connect(self.__btnRunClicked)
        btnExcel = QPushButton('엑셀 저장')
        btnExcel.resize(btnExcel.sizeHint())
        btnExcel.clicked.connect(self.__btnExcelClicked)
        buttonLayout.addWidget(self._sujectLabel)
        buttonLayout.addWidget(btnRun)
        buttonLayout.addWidget(btnExcel)

        queryLayout = QVBoxLayout()
        self._inputQuery = QTextEdit()
        queryLayout.addWidget(self._inputQuery)

        topLeftLayout = QVBoxLayout()
        self._queryTableWidget = QTableWidget()
        self._queryTableWidget.cellClicked.connect(self.__cellClicked)
        self._queryTableWidget.setSortingEnabled(True)            # 컬럼 헤더를 클릭하면 정렬이 되게 한다.
        self._queryTableWidget.setAlternatingRowColors(True)      # 행 색상이 번갈아 구분 표시되게 한다.
        self._queryTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)      # Edit 금지
        self._queryTableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)     # Row 단위로 선택이 표되게 한다.
        self._queryTableWidget.setSelectionMode(QAbstractItemView.SingleSelection)    # 하나의 Row만 선택하게 함.
        self.setTableWidgetData()

        topLeftLayout.addWidget(self._queryTableWidget)
        topLeftFrame.setLayout(topLeftLayout)

        topRightLayout = QVBoxLayout()
        topRightLayout.addLayout(buttonLayout)
        topRightLayout.addLayout(queryLayout)
        topRightFrame.setLayout(topRightLayout)

        resultLayout = QVBoxLayout()
        self._tableView = QTableView()
        resultLayout.addWidget(self._tableView)
        bottomFrame.setLayout(resultLayout)

        mainFrameLayout = QVBoxLayout()
        mainFrameLayout.addWidget(mainFrame)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(titleLayout)
        mainLayout.addLayout(mainFrameLayout)
        self.setLayout(mainLayout)

    def setTableWidgetData(self):
        try:
            db_connection = mysqlHandler.dbConnect()
            cursor = mysqlHandler.dbDictCursor(db_connection)
            sql = 'select report_id, report_class, report_name, query_stmt' \
                  ' from myasset.sql_report order by report_class, report_name'
            rowCount = cursor.execute(sql)
        finally:
            db_connection.close()

        self._queryTableWidget.setRowCount(rowCount)
        self._queryTableWidget.setColumnCount(4)
        column_headers = ['Report Class', 'Report Name', 'Query Statement', 'Report ID']
        self._queryTableWidget.setHorizontalHeaderLabels(column_headers)
        result = cursor.fetchall()
        for r, row in enumerate(result):
            self._queryTableWidget.setItem(r, 0, QTableWidgetItem(row.get('report_class')))
            self._queryTableWidget.setItem(r, 1, QTableWidgetItem(row.get('report_name')))
            self._queryTableWidget.setItem(r, 2, QTableWidgetItem(row.get('query_stmt')))
            self._queryTableWidget.setItem(r, 3, QTableWidgetItem(str(row.get('report_id'))))

        self._queryTableWidget.resizeColumnsToContents()
        self._queryTableWidget.resizeRowsToContents()

    # Show selected query statement in the query input box
    @pyqtSlot(int, int)
    def __cellClicked(self, row, col):
        queryStmt = self._queryTableWidget.item(row, 2)  # Query Statement
        if queryStmt:
            self._inputQuery.setText(queryStmt.text())
        reportID = self._queryTableWidget.item(row, 3)  # Report ID
        if reportID:
            self._sujectLabel.setText('SQL Query #' + reportID.text())
        return

    # Run sql query
    def __btnRunClicked(self):
        db_connection = mysqlHandler.dbConnect()
        cursor = mysqlHandler.dbDictCursor(db_connection)
        sql = self._inputQuery.toPlainText()
        cursor.execute(sql)
        result = cursor.fetchall()
        self._dataframe = pd.DataFrame(result)
        model = pandasModel(self._dataframe)
        self._tableView.setModel(model)
        db_connection.close()

    # Write excel file
    def __btnExcelClicked(self):
        # if self._dataframe.empty:
        #     QMessageBox.question(self, 'Message', 'No data found', QMessageBox.Ok)
        #     return

        inputText, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter the output file name: ')
        if ok:
            filename = str(inputText)
            try:
                self._dataframe.to_excel(filename + '.xlsx', sheet_name='result')
                QMessageBox.question(self, 'Message', 'The file creation is succeed', QMessageBox.Ok)
            except Exception as e:
                QMessageBox.question(self, 'Message', 'The file creation is failed', QMessageBox.Ok)
        return

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    w = SQLReportWindow(None, '대성에너지')
    w.show()
    sys.exit(app.exec_())