import sys

from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from .ParserThread import ParserThread
from .ListView import ListView
from ..config import DefinitionLoader
from ..arxiv import filter

class ArxivFilter(QMainWindow):

    def __init__(self, config=None):
        super().__init__()

        self._config = config

        configLoader = DefinitionLoader()
        if self._config is not None:
            configOK = configLoader.loadFromFile(self._config)
        else:
            configOK = configLoader.loadDefault()

        if not configOK:
            error = QErrorMessage()
            if configLoader.error is not None:
                error.showMessage(configLoader.error)
            else:
                error.showMessage("Error while loading the config!")
            error.exec_()

            sys.exit(-1)

        self._filter = filter(configLoader.definition)

        self._loading = False

        self.initUI()

        self.setAcceptDrops(True)

    def initUI(self):

        self.setWindowTitle('Arxiv Daily E-Mail Filter')

        self.lo = QVBoxLayout()

        labelFiltered = QLabel("Filtered Entries", self)
        labelFiltered.setStyleSheet("font-weight: bold; font-size: 12pt");
        labelOther = QLabel("Other Entries", self)
        labelOther.setStyleSheet("font-weight: bold; font-size: 12pt");

        # Construct Filtered Table
        self.tableFiltered = ListView(filtered = True)

        # Construct Other Table
        self.tableOther = ListView(filtered = False)

        # Construct the Usage Hint
        self.hint = QLabel("Drag-and-drop or paste (Ctrl+V) the text of the daily Arxiv E-Mail")
        self.hint.setStyleSheet("font-weight: bold; font-size: 14pt; color: #3e3e3e; background-color: white")
        self.hint.setWordWrap(True)
        self.hint.setAlignment(QtCore.Qt.AlignCenter)
        self._hintShown = True

        self.lo.addWidget(labelFiltered)
        self.lo.addWidget(self.hint)
        self.lo.addWidget(labelOther)
        self.lo.addWidget(self.tableOther)

        self.lo.setStretch(1, 2)
        self.lo.setStretch(3, 1)

        self.lo.insertSpacing(2, 20)

        widget = QWidget()
        widget.setLayout(self.lo)
        self.setCentralWidget(widget)

        # Enable pasting of E-Mail text
        self.shortcutPaste = QShortcut(QKeySequence('Ctrl+V'), self)
        self.shortcutPaste.activated.connect(self.pasteEvent)


    # Drag and Drop handling of E-Mail text
    def dragEnterEvent(self, e):
        if self._loading:
            e.ignore()
        elif e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        text = e.mimeData().text()
        self._setArxivText(text)


    def pasteEvent(self):
        text = QGuiApplication.clipboard().mimeData().text()
        self._setArxivText(text)


    def _setArxivText(self, text):

        self.statusBar().showMessage("Loading ... ")

        self._parser = ParserThread(text, self)
        self._parser.finished.connect(self.parsedCallback)
        self._parser.start()
        self._loading = True


    def _hideHint(self):
        if self._hintShown:
            self.lo.replaceWidget(self.hint, self.tableFiltered)
            self._hintShown = False

    def parsedCallback(self):

        self._hideHint()

        # Clear the status bar and show potential errors
        self.statusBar().clearMessage()

        if self._parser.error() is not None:
            self.statusBar().showMessage(self._parser.error(), 5000)

        filtered = []
        other = []

        for entry in self._parser.entries():
            scored = self._filter.score(entry)

            if scored.score > 0:
                filtered.append(scored)
            else:
                other.append(scored)

        self.tableFiltered.setEntries(filtered)
        self.tableOther.setEntries(other)

        self._loading = False
