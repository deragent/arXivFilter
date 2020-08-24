from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class EntryLabel(QLabel):

    clicked = pyqtSignal()
    doubleClicked = pyqtSignal()

    def __init__(self, text, parent=None):
        super().__init__(text, parent)

        self.setWordWrap(True)
        self.setStyleSheet("font-weight: bold;");

    def mouseReleaseEvent(self, event):
        self.clicked.emit()

    def mouseDoubleClickEvent(self, event):
        self.doubleClicked.emit()

    def enterEvent(self, event):
        self.setStyleSheet("font-weight: bold; text-decoration: underline;")
        self.setCursor(Qt.PointingHandCursor)

    def leaveEvent(self, event):
        self.setStyleSheet("font-weight: bold; text-decoration: none;")
        self.unsetCursor()


class FoldLabel(QLabel):

    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(">", parent)

        self._closed = True

        self.setStyleSheet("font-size: 18pt; font-weight: bold;");

    def toggle(self):
        if self._closed:
            self.setText("v")
        else:
            self.setText(">")

        self._closed = not self._closed

    def mouseReleaseEvent(self, event):
        self.clicked.emit()

    def enterEvent(self, event):
        self.setCursor(Qt.PointingHandCursor)

    def leaveEvent(self, event):
        self.unsetCursor()



class ListEntry(QWidget):

    def __init__(self, entry, filtered=True, parent=None):
        super().__init__(parent)

        self._entry = entry
        self._filtered = filtered

        self.initUI()

    def initUI(self):

        lo = QVBoxLayout(self)

        self._header = QWidget()
        self._content = QWidget()

        self._content.setVisible(False)

        lo.addWidget(self._header)
        lo.addWidget(self._content)

        # Create the header layout
        header_lo = QHBoxLayout()

        self._fold = FoldLabel()
        header_lo.addWidget(self._fold)
        header_lo.setStretch(0, 0.01)

        title = EntryLabel(self._entry.title)
        header_lo.addWidget(title)
        header_lo.setStretch(1, 1)

        title.clicked.connect(self.openLink)
        self._fold.clicked.connect(self.toggleContent)

        if self._filtered:
            reason = QLabel("[A]B[C][D]")
            header_lo.addWidget(reason)
            header_lo.setStretch(2, 0.01)

        self._header.setLayout(header_lo)

        # Create the content
        content_lo = QVBoxLayout()

        content_lo.addWidget(QLabel("Test"))

        self._content.setLayout(content_lo)


        self.setLayout(lo)

    def toggleContent(self):
        self._fold.toggle()
        self._content.setVisible(not self._content.isVisible())

    def openLink(self):
        QDesktopServices.openUrl(QUrl(self._entry.link))
