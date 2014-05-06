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

class DaemonGui(QtGui.QSystemTrayIcon):
    def __init__(self, icon, parent=None, **kwargs):
        super(DaemonGui, self).__init__(icon, parent)

        menu = self.initMenu(parent)
        self.setContextMenu(menu)

    def initMenu(self, parent):
        menu = QtGui.QMenu(parent)

        folderaction = menu.addAction('&Open Drive Folder')
        folderaction.triggered.connect(parent.close)

        prefAct = menu.addAction('&Preferences...')
        prefAct.triggered.connect(parent.close)

        exitAction = menu.addAction('&Quit Google Drive')
        exitAction.triggered.connect(parent.close)

        return menu

def main(args):
    
    app = QtGui.QApplication(args)

    w = QtGui.QWidget()

    icon = QtGui.QIcon('img/drive_simple_plain_svg.svg')

    sti = DaemonGui(icon, parent=w, app=app)

    mainwin = QtGui.QMainWindow(parent=w)

    mainwin.show()

    sti.show()

    return app.exec_()

if __name__ == '__main__':
    sys.exit(main(sys.argv))
