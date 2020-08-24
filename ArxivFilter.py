import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from arxiv_filter import ui

def main():
   app = QApplication(sys.argv)

   window = ui.ArxivFilter()
   window.show()

   app.exec_()

if __name__ == '__main__':
   main()
