#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, with_statement, print_function, unicode_literals

from future_builtins import *

import sys, time

try:
    import threading
except ImportError:
    import dummy_threading as threading

try:
    from PySide import QtGui, QtCore
except ImportError:
    try:
        from PyQt4 import QtGui, QtCore
    except ImportError:
        sys.stderr.write('Unable to import GUI code. Please install PySide or PyQt.\n')
        QtGui = None

class PrefWindow(QtGui.QMainWindow):
    def __init__(self, **kwargs):
        super(PrefWindow, self).__init__(**kwargs)

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Google Drive Preferences')
        b = QtGui.QPushButton('Center', self)
        b.clicked.connect(self.center)
        b.resize(b.sizeHint())
        b.move(50, 50)

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

class DaemonGui(QtGui.QWidget):
    def __init__(self, icon, *args, **kwargs):
        super(DaemonGui, self).__init__()
        self.tico = QtGui.QSystemTrayIcon(icon, parent=self)
        self.pwin = PrefWindow(parent=self)
        menu = self.initMenu()
        self.tico.setContextMenu(menu)

    def initMenu(self):
        menu = QtGui.QMenu(self)

        folderaction = menu.addAction('&Open Drive Folder')
        folderaction.triggered.connect(self.close)

        prefAct = menu.addAction('&Preferences...')
        prefAct.triggered.connect(self.pwin.show)

        exitAction = menu.addAction('&Quit Google Drive')
        exitAction.triggered.connect(self.close)

        return menu

    def show(self):
        self.tico.show()

def main(args):
    
    app = QtGui.QApplication(args)

    icon = QtGui.QIcon('img/drive_simple_plain_svg.svg')

    sti = DaemonGui(icon)

    sti.show()

    return app.exec_()

if __name__ == '__main__':
    sys.exit(main(sys.argv))

