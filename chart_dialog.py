#!/usr/bin/env python
from __future__ import (unicode_literals, division, absolute_import,
                        print_function)

__license__   = 'Free to use for personal use'
__copyright__ = '2012, Daniel Bratell <bratell@lysator.liu.se>'
__docformat__ = 'restructuredtext en'

import PyQt4.Qt as qt
from math import sqrt
from calibre_plugins.tag_stats_plugin.top_list_widget import TopListWidget

#from calibre_plugins.tag_stats_plugin.config import prefs

class ChartDialog(qt.QDialog):

    def __init__(self, gui, icon, result_list):
        qt.QDialog.__init__(self, gui)
        self.gui = gui

        # The current database shown in the GUI
        # db is an instance of the class LibraryDatabase2 from database.py
        # This class has many, many methods that allow you to do a lot of
        # things.
        self.db = gui.current_db

        self.l = qt.QVBoxLayout()
        self.setLayout(self.l)

        tab_widget = qt.QTabWidget()
        self.l.addWidget(tab_widget)
        
        for section in result_list:
            chart_type = section[0]
            if chart_type == 'bar' or chart_type == 'histogram':
                (chart_type, title, results, max_value) = section;
                vary_colours = chart_type == 'bar'
                view = self.create_tab_content(title, max_value, results, vary_colours)
                tab_widget.addTab(view, title)
            elif chart_type == 'list':
                (chart_type, title, results, label_label) = section
                tab_widget.addTab(TopListWidget(self.gui, results, label_label), title)
            else:
                qt.QMessageBox(gui, "Unknown chart type " + str(chart_type));

        self.resize(self.sizeHint())
        
    def create_tab_content(self, title, max_value, results, vary_colours):
        ''' Creates a chart area with the results in them and returns it. '''

        scene = qt.QGraphicsScene()

        view = qt.QGraphicsView(scene)

        start_hue = 225 # 170 is cyan, 160 is greenish cyan, 190 is sky blue, 230 is deep blue (acceptable), 240 is also deep blue, maybe with a hint of purple, 250 is blue with a strong hint of purple, 220 is a slightly pale deep blue
        top_margin = 5
        max_bar_width = 40
        preferred_chart_width = 700
        relative_spacing = 2 / 3
        if results:
            preferred_bar_width = int(round(preferred_chart_width / len(results) / (1 + relative_spacing)))
            bar_width = max(1, min(max_bar_width, preferred_bar_width))
        else:
            bar_width = max_bar_width
        spacing = int(round(relative_spacing * bar_width))
        chart_height = 400
        scaler = max_value
        hue = start_hue
        x = 0
        last_label_x_pos = -1000000 # Enough to trigger a label at x = 0.

        # Frame for the chart.
        if results:
            chart_width = len(results) * (bar_width + spacing)
        else:
            chart_width = spacing # One half before and one half after.
        dashed_pen = qt.QPen()
        dashed_pen.setStyle(qt.Qt.DotLine)
        # Find good places to put horizontal lines. We prefer_ to have
        # the lines corresponding to integers.
        if max_value > 30 or max_value < 1:
            horizontal_line_gap = 10 # 10 percent lines
        else:
            horizontal_line_gap = 100.0 / max_value
            while horizontal_line_gap < 8:
                horizontal_line_gap = horizontal_line_gap * 2
        line_number = 1
        widest_label_width = 0
        horizontal_lines = []
        y_axis_labels = []
        while round(line_number * horizontal_line_gap) <= 100:
            percentile = line_number * horizontal_line_gap
            percentile_y = top_margin + chart_height - round(percentile * chart_height / 100) # Grid fit.
            horizontal_lines.append(scene.addLine(x, percentile_y, chart_width, percentile_y, dashed_pen))
            # Y axis label.
            label_text = str(int(round(percentile * max_value / 100)))
            label_obj = scene.addSimpleText(label_text)
            y_axis_labels.append((label_text, label_obj))
            
            metrics = qt.QFontMetrics(label_obj.font())
            # The x position is adjusted after the loop when we know the width of the
            # widest label.
            label_obj.setPos(x, percentile_y - metrics.ascent() / 2)
            widest_label_width = max(widest_label_width, metrics.width(label_text))
            
            line_number = line_number + 1

        # Move frame so it doesn't overlap with labels and right align labels.
        if widest_label_width > 0:
            x_gap_between_labels_and_frame = 1
            x = x + widest_label_width + x_gap_between_labels_and_frame
            # Move horizontal lines to the right so they don't overlap with the labels.
            for horizontal_line in horizontal_lines:
                horizontal_line.setPos(x, horizontal_line.pos().y())
            # Move labels so that they are right aligned.
            for (label_text, y_axis_label) in y_axis_labels:
                metrics = qt.QFontMetrics(y_axis_label.font())
                diff_to_widest = widest_label_width - metrics.width(label_text)
                y_axis_label.setPos(y_axis_label.pos().x() + diff_to_widest, y_axis_label.pos().y()) 

        # Outer frame.
        scene.addRect(qt.QRectF(x, top_margin, chart_width, chart_height))
        chart_bottom_y = top_margin + chart_height
        x = x + int(round(spacing / 2))

        # Bars.
        for (label, value) in results:
            # Select colors so that there is distinct gaps but they never overlap.
            # Looking at the hue scale as a circle and rotating around it in 1/phi
            # (~220 degree) steps turn out to be very good. Thanks to http://vihart.com/
            # and her spirals and fibonacci number video for reminding me of this.
            color = qt.QColor()
            color.setHsv(hue, 180, 255)
            if vary_colours:
                phi = (1 + sqrt(5)) / 2
                hue = (hue + 256 / phi) % 256

            # Bar.
            bar_height = value * chart_height / scaler
            rect = qt.QRectF(x, chart_bottom_y - bar_height, bar_width, bar_height)
            scene.addRect(rect, qt.QPen(), qt.QBrush(color))

            # X axis label.
            if (bar_width > 20 or x - last_label_x_pos > 50):
                label_obj = scene.addSimpleText(label)
                metrics = qt.QFontMetrics(label_obj.font())
                text_width = metrics.width(label)
                label_x_pos = x + bar_width / 2 - text_width / 2
                # TODO Truncate over-wide labels.
                label_obj.setPos(label_x_pos, chart_bottom_y)
                last_label_x_pos = label_x_pos

            x += bar_width + spacing

#        view.show()
        return view

            
