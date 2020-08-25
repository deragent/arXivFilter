import sys
import argparse

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from arxiv_filter import ui

def main():
    app = QApplication(sys.argv)

    argv = [str(aa) for aa in app.arguments()]

    # Parse our command line arguments
    parser = argparse.ArgumentParser(description='''
        arXiv Filter
        Simple utility for filtering arXiv daily E-Mail.
        Just drag and drop the E-Mail text into the window and the magic happens :)''')

    parser.add_argument("-c", "--config", type=str, help="Alternative filter config file.")

    args = parser.parse_args(argv[1:])

    window = ui.ArxivFilter(config=args.config)
    window.show()

    app.exec_()

if __name__ == '__main__':
    main()
