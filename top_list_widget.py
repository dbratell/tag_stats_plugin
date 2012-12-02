#!/usr/bin/env python
from __future__ import (unicode_literals, division, absolute_import,
                        print_function)

__license__   = 'Free to use for personal use'
__copyright__ = '2012, Daniel Bratell <bratell@lysator.liu.se>'
__docformat__ = 'restructuredtext en'

import PyQt4.Qt as qt

# class NumericStandardItem(qt.QStandardItem):
#     ''' A QStandardItem that knows how to do numeric sorting '''
#     def __init__(self, number):
#         self._number = number
#         qt.QStandardItem(self, str(number))
    
#     def __gt__(self, other):
#         return self._number > other._number
    
#     def __lt__(self, other):
#         return self._number < other._number

class TopListWidget(qt.QWidget):

    def __init__(self, gui, top_list, label_label):
        ''' top_list is a list of Label value pairs. '''
        qt.QWidget.__init__(self)
        self.gui = gui

        self.l = qt.QVBoxLayout()
        self.setLayout(self.l)

        model = qt.QStandardItemModel(len(top_list), 3)

        row = 0
        for (label, value) in top_list:
            model.setItem(row, 0, self.create_number_item(row + 1))
            model.setItem(row, 1, self.create_string_item(label))
            model.setItem(row, 2, self.create_number_item(value))
#            self.l.addWidget(qt.QLabel(label))
#            self.l.addWidget(qt.QLabel(str(value)))
            row = row + 1

        # model.setHeaderData(0, qt.Qt.Horizontal, "Pos", qt.Qt.DisplayRole)
        # model.setHeaderData(1, qt.Qt.Horizontal, label_label, qt.Qt.DisplayRole)
        # model.setHeaderData(2, qt.Qt.Horizontal, "Count", qt.Qt.DisplayRole)

        model.setHorizontalHeaderLabels(["Pos", label_label, "Count"])
        table = qt.QTableView(self)
        table.setModel(model)
#        table.setGridStyle(qt.Qt.NoPen)
        table.setShowGrid(False)
        table.resizeColumnToContents(0)
        table.verticalHeader().hide()
        text_height = qt.QFontMetrics(table.font()).lineSpacing()
        table.verticalHeader().setDefaultSectionSize(text_height + max(1, int(text_height * 0.1)))
        table.setSortingEnabled(True)
        table.sortByColumn(0, qt.Qt.AscendingOrder)
        table.setSelectionBehavior(qt.QAbstractItemView.SelectRows)
        self.l.addWidget(table)
        self.resize(self.sizeHint())
       

    def create_string_item(self, the_string):
        item = qt.QStandardItem(the_string)
        item.setEditable(False)
        # if right_align:
        #     #        item.setData(qt.Qt.AlignRight, qt.Qt.TextAlignmentRole)
        #     item.setTextAlignment(qt.Qt.AlignRight)
        # else:
        item.setTextAlignment(qt.Qt.AlignLeft)
        return item

    def create_number_item(self, the_number):
        item = qt.QStandardItem(the_number)
        item.setEditable(False)
        item.setData(str(the_number) + ".", qt.Qt.DisplayRole)
        item.setData(the_number, qt.Qt.EditRole)
        #        item.setData(qt.Qt.AlignRight, qt.Qt.TextAlignmentRole)
        item.setTextAlignment(qt.Qt.AlignRight)
        return item
    
