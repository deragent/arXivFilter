from PyQt5.QtWidgets import *

from .ParserThread import ParserThread
from .ListView import ListView

class ArxivFilter(QMainWindow):

    def __init__(self):
        super().__init__()

        self._loading = False

        self.initUI()

        self.setAcceptDrops(True)

    def initUI(self):

        self.setWindowTitle('Arxiv Daily E-Mail Filter')

        lo = QVBoxLayout()

        labelFiltered = QLabel("Filtered Entries", self)
        labelOther = QLabel("Other Entries", self)

        # Construct Filtered Table
        self.tableFiltered = ListView(filtered = True, parent=self)

        # Construct Other Table
        self.tableOther = ListView(filtered = False, parent=self)

        lo.addWidget(labelFiltered)
        lo.addWidget(self.tableFiltered)
        lo.addWidget(labelOther)
        lo.addWidget(self.tableOther)

        lo.setStretch(1, 2)
        lo.setStretch(3, 1)

        widget = QWidget()
        widget.setLayout(lo)
        self.setCentralWidget(widget)


    def dragEnterEvent(self, e):
        if self._loading:
            e.ignore()
        elif e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        text = e.mimeData().text()

        self.statusBar().showMessage("Loading ... ")

        self._parser = ParserThread(text, self)
        self._parser.finished.connect(self.parsedCallback)
        self._parser.start()
        self._loading = True



    def parsedCallback(self):

        # Clear the status bar and show potential errors
        self.statusBar().clearMessage()

        if self._parser.error() is not None:
            self.statusBar.showMessage(self._parser.error(), 5000)

        # Clear the tables
        self.tableFiltered.clear()

        for entry in self._parser.entries():
            self.tableFiltered.addEntry(entry)

        self._loading = False
