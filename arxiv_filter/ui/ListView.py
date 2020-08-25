from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from .ListEntry import ListEntry

class ListView(QScrollArea):

        def __init__(self, filtered=True, parent=None):
            super().__init__(parent)

            self._filtered = filtered
            self._widgets = []

            self.initUI()

        def initUI(self):

            self.setBackgroundRole(QPalette.Light)
            self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

            widget = QWidget(self)

            self._layout = QVBoxLayout(self)

            widget.setLayout(self._layout)

            self.setWidget(widget)
            self.setWidgetResizable(True) # This line took me ca. 1 hour....

        def clear(self):
            for widget in self._widgets:
                self._layout.removeWidget(widget)
                widget.setParent(None)

            self._widgets = []


        def setEntries(self, entries):
            self.clear()

            if self._filtered:
                scores = [e.score for e in entries]
                indexes = sorted(range(len(scores)), key=scores.__getitem__)
                indexes.reverse()
            else:
                indexes = range(0, len(entries))

            for idx in indexes:
                entry = entries[idx]
                widget = ListEntry(entry, self._filtered)
                self._layout.addWidget(widget)
                self._widgets.append(widget)
