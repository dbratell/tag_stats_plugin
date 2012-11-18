#!/usr/bin/env python
from __future__ import (unicode_literals, division, absolute_import,
                        print_function)

__license__   = 'Free to use for personal use'
__copyright__ = '2012, Daniel Bratell <bratell@lysator.liu.se>'
__docformat__ = 'restructuredtext en'

import PyQt4.Qt as qt

#from calibre_plugins.tag_stats_plugin.config import prefs

class ChartDialog(qt.QDialog):

    def __init__(self, gui, icon, max_value, result_list):
        qt.QDialog.__init__(self, gui)
        self.gui = gui

        # The current database shown in the GUI
        # db is an instance of the class LibraryDatabase2 from database.py
        # This class has many, many methods that allow you to do a lot of
        # things.
        self.db = gui.current_db

#        qt.QMessageBox.information(self, 'Distribution of genres', result_text)
        self.l = qt.QVBoxLayout()
        self.setLayout(self.l)

        tab_widget = qt.QTabWidget()
        self.l.addWidget(tab_widget)
        
        for (title,  results) in result_list:
#            self.l.addWidget(qt.QLabel(title))
            view = self.create_tab_content(title, max_value, results)
            tab_widget.addTab(view, title)

        self.resize(self.sizeHint())
        
    def create_tab_content(self, title, max_value, results):
        ''' Creates a chart area with the results in them and returns it. '''

        scene = qt.QGraphicsScene()
#        scene.addText(result_text)

        view = qt.QGraphicsView(scene)
#        self.l.addWidget(view)

        bar_width = 40
        spacing = 30
        chart_height = 300
        scaler = max_value
        spacing_below_bars = 10
        hue = 160
        x = spacing / 2

        # Frame for the chart.
        chart_width = len(results) * (bar_width + spacing)
        scene.addRect(qt.QRectF(0, 0, chart_width, chart_height))
        dashed_pen = qt.QPen()
        dashed_pen.setStyle(qt.Qt.DotLine)
        for percentile in range(10, 100, 10):
            percentile_y = percentile * chart_height / 100
            scene.addLine(0, percentile_y, chart_width, percentile_y, dashed_pen)

        # Bars.
        for (label, value) in results:
            color = qt.QColor()
            color.setHsv(hue, 160, 255)
            hue = (hue + 91) % 256

            # Bar.
            bar_height = value * chart_height / scaler
            rect = qt.QRectF(x, chart_height - bar_height, bar_width, bar_height)
            scene.addRect(rect, qt.QPen(), qt.QBrush(color))

            # Label.
            label_obj = scene.addText(label)
            text_width = label_obj.textWidth()
            # print(text_width)
            # I would like to center the text but for that I need to
            # know how wide it is and textWidth() keeps returning
            # -1.0.
            if text_width > 0:
                label_x_pos = x + bar_width / 2 - text_width / 2
            else:
                label_x_pos = x
            label_obj.setPos(label_x_pos, chart_height + spacing_below_bars)

            x += bar_width + spacing

#        view.show()
        return view

            
