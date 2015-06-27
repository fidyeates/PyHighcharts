#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
3d_chart.py

Highcharts 3d Chart Examples
"""

__author__  = "Fin"

# Stdlib Imports

# Third Party Imports
from pyhighcharts import Chart, ChartTypes

chart = Chart()
chart.make_3d()
chart.set_title("3D Column Demo")
chart.set_yaxis_title("Units Sold")
chart.add_data_series(
    ChartTypes.column,
    [
        ["Jan", 1054],
        ["Feb",  124],
        ["Mar",  254],
        ["Apr",  465],
        ["May",  343],
        ["Jun",  534],
        ["Jul",  835],
        ["Aug",  434],
        ["Sep",  543],
        ["Oct",  304],
        ["Nov", 1623],
        ["Dec", 2032],
    ],
    name="Monthly Sales")
chart.set_options(chart={"margin": 75})
chart.show()
