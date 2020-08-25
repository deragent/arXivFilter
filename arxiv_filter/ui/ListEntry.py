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

        self.setStyleSheet("font-size: 15pt; font-weight: bold;");

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



class ListEntry(QFrame):

    def __init__(self, entry, filtered=True, parent=None):
        super().__init__(parent)

        self._entry = entry
        self._filtered = filtered

        self.initUI()

    def initUI(self):

        self.setContentsMargins(0, 0, 0, 0)
        self.setFrameStyle(QFrame.Panel | QFrame.Raised);
        self.setLineWidth(1);

        lo = QVBoxLayout(self)

        self._header = QFrame()
        self._content = QWidget()

        # Color the header if filtered
        if self._filtered:
            color = int(self._entry.score/100 * 255)
            if color > 255: color = 255
            self._header.setStyleSheet("background-color: rgb(%i, %i, %i);"%(255- color, 255 - color, 255));

        self._content.setVisible(False)

        lo.addWidget(self._header)
        lo.addWidget(self._content)

        # Create the header layout
        header_lo = QHBoxLayout()

        self._fold = FoldLabel()
        header_lo.addWidget(self._fold)
        header_lo.setStretch(0, 0.01)

        title = EntryLabel(self._entry.entry.title)
        header_lo.addWidget(title)
        header_lo.setStretch(1, 1)

        title.clicked.connect(self.openLink)
        self._fold.clicked.connect(self.toggleContent)

        if self._filtered:
            hits = [key[0].upper() for key, value in self._entry.hits.items() if value]
            reason = QLabel("Score: %i\n\n%s"%(self._entry.score, ''.join(hits)))
            header_lo.addWidget(reason)
            header_lo.setStretch(2, 0.01)

        self._header.setLayout(header_lo)

        # Create the content
        content_lo = QHBoxLayout()

        ## Authors and categories
        meta_widget = QWidget()
        meta_lo = QVBoxLayout()

        collaboration = QLabel(self._entry.entry.collaboration)
        authors = QLabel('\n\n'.join(self._entry.matched_authors))
        categories = QLabel('\n\n'.join(self._entry.matched_categories))

        collaboration.setStyleSheet("font-weight: bold; font-style: italic")
        authors.setStyleSheet("font-weight: bold")
        categories.setStyleSheet("font-style: italic")

        meta_lo.addWidget(collaboration)
        meta_lo.addWidget(authors)
        meta_lo.addWidget(categories)

        meta_lo.insertSpacing(1, 20)
        meta_lo.insertSpacing(3, 20)

        meta_widget.setLayout(meta_lo)

        ## Abstract


        abstract = QLabel(self._entry.entry.abstract)
        abstract.setWordWrap(True)
        abstract.setStyleSheet("font-size: 11pt; line-height: 160%; text-align: justify;")

        content_lo.addWidget(meta_widget)
        content_lo.addWidget(abstract)

        content_lo.setStretch(0, 1)
        content_lo.setStretch(1, 4)

        self._content.setLayout(content_lo)

        self.setLayout(lo)

    def toggleContent(self):
        self._fold.toggle()
        self._content.setVisible(not self._content.isVisible())

    def openLink(self):
        QDesktopServices.openUrl(QUrl(self._entry.entry.link))
