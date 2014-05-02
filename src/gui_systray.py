#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, with_statement, print_function, unicode_literals

from future_builtins import *

import sys, time

try:
    from PySide import QtGui
except ImportError:
    try:
        from PyQt4 import QtGui
    except ImportError:
        sys.stderr.write('Unable to import GUI code. Please install PySide or PyQt.')
        QtGui = None


def main(args):
    
    app = QtGui.QApplication(args)

    w = QtGui.QWidget()

    ico = QtGui.QIcon('img/drive_simple_plain_svg.svg')

    sti = QtGui.QSystemTrayIcon(ico, parent=w)

    sti.show()

    for i in range(10):
        app.processEvents()
        time.sleep(0.25)

    app.exit()
    sys.exit()


if __name__ == '__main__':
    sys.exit(main(sys.argv))
