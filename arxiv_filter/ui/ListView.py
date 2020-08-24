from PyQt5.QtWidgets import *

class ListView(QTableWidget):

        def __init__(self, filtered=True, parent=None):
            super().__init__(parent)

            self._filtered = filtered
            self._entries = []
            self._priorities = []

            self.initUI()

        def initUI(self):

            if self._filtered:
                self.setColumnCount(2)
                self.setHorizontalHeaderLabels(['Title', 'Reasons'])
                self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
                self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
            else:
                self.setColumnCount(1)
                self.setHorizontalHeaderLabels(['Title'])
                self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        def clear(self):
            self.setRowCount(0)

        def addEntry(self, entry, priority=-1):
            self.insertRow(self.rowCount())
            self.setItem(self.rowCount()-1, 0, QTableWidgetItem(entry.title))
