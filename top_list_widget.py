#!/usr/bin/env python
from __future__ import (unicode_literals, division, absolute_import,
                        print_function)

__license__   = 'Free to use for personal use'
__copyright__ = '2012, Daniel Bratell <bratell@lysator.liu.se>'
__docformat__ = 'restructuredtext en'

import PyQt4.Qt as qt

class TopListWidget(qt.QWidget):

    def __init__(self, gui, top_list):
        ''' top_list is a list of Label value pairs. '''
        qt.QWidget.__init__(self)
        self.gui = gui

        self.l = qt.QVBoxLayout()
        self.setLayout(self.l)

        for (label, value) in top_list:
            self.l.addWidget(qt.QLabel(label))
            self.l.addWidget(qt.QLabel(str(value)))

        self.resize(self.sizeHint())
       
