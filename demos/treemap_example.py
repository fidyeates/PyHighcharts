#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
treemap_example.py
"""

__author__  = "Fin"

# Stdlib Imports

# Third Party Imports
from pyhighcharts import Chart, ChartTypes

chart = Chart()
chart.set_title("Highcharts Treemap")
chart.set_colour_axis()
chart.add_data_series(
    ChartTypes.treemap,
    [{
        "name": "A",
        "value": 6,
        "colorValue": 1
    }, {
        "name": "B",
        "value": 6,
        "colorValue": 2
    }, {
        "name": "C",
        "value": 4,
        "colorValue": 3
    }, {
        "name": "D",
        "value": 3,
        "colorValue": 4
    }, {
        "name": "E",
        "value": 2,
        "colorValue": 5
    }, {
        "name": "F",
        "value": 2,
        "colorValue": 6
    }, {
        "name": "G",
        "value": 1,
        "colorValue": 7
    }],
    layoutAlgorithm="squarified",
    name="Sales per employee",
    borderWidth=1,
    dataLabels={"enabled": True, "color": "black"})
chart.show()
