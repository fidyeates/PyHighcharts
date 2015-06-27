#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
inverted_axis.py

Highcharts inverted_axis example
"""

__author__  = "Fin"

# Stdlib Imports

# Third Party Imports
from pyhighcharts import Chart, ChartTypes

inverted_axis = Chart()
inverted_axis.invert_axis()
inverted_axis.set_title("Atmosphere Temperature by Altitude")
inverted_axis.set_subtitle("According to the Standard Atmosphere Model")
inverted_axis.set_xaxis_title("Altitude")
inverted_axis.set_yaxis_title("Temperature")
inverted_axis.set_tooltip(headerFormat="<b>{series.name}</b></br>",
                          pointFormat="{point.x} km: {point.y}°C")
inverted_axis.add_data_series(
    ChartTypes.spline,
    [
        [0, 15],
        [10, -50],
        [20, -56.5],
        [30, -46.5],
        [40, -22.1],
        [50, -2.5],
        [60, -27.7],
        [70, -55.7],
        [80, -76.5]
    ],
    name="Temperature")
inverted_axis.show()
