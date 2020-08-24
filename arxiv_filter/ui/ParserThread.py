import time

from PyQt5.QtCore import QThread

from ..arxiv import parser

class ParserThread(QThread):

    def __init__(self, str, parent=None):
        super().__init__(parent)

        self._str = str
        self._parser = parser()

    def entries(self):
        return self._parser.entries()

    def error(self):
        if self._parser.error is not None:
            return self._parser.error
        elif self._parser.warning is not None:
            return self._parser.warning
        else:
            return None

    def run(self):

        self._parser.fromText(self._str)
