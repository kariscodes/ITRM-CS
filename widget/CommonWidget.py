from PyQt5.QtWidgets import QHBoxLayout, QLabel
# from PyQt5.QtCore import Qt
# from PyQt5.QtGui import QKeyEvent, QKeySequence

class TitleLayout(QHBoxLayout):
    def __init__(self, headerTitle):
        super().__init__()
        self._headerTitle = headerTitle
        self.initUI()

    def initUI(self):
        theLabel = QLabel(self._headerTitle)
        theLabel.setStyleSheet("color: rgb(26, 4, 160);"
                               "font: bold 18px;"
                               "padding: 6px;"
                               "background-color: #87CEFA;"
                               "border-style: outset;"
                               "border-width: 1px;"
                               "border-radius: 5px;"
                               "border-color: #1E90FF")
        theLabel.setFixedHeight(30)
        self.addWidget(theLabel)

class SubtitleLabel(QLabel):
    def __init__(self, subtitle):
        super().__init__()
        self.setText(subtitle)
        theFont = self.font()
        theFont.setFamily('Times New Roman')
        theFont.setPointSize(13)
        theFont.setBold(True)
        self.setFont(theFont)