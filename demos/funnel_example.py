#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
funnel_example.py
"""

__author__  = "Fin"

# Stdlib Imports

# Third Party Imports
from pyhighcharts import Chart, ChartTypes

chart = Chart()
chart.set_title("Sales Funnel")
chart.set_legend(enabled=False)
chart.add_data_series(
    ChartTypes.funnel,
    [
        ['Website visits',   15654],
        ['Downloads',       4064],
        ['Requested price list', 1987],
        ['Invoice sent',    976],
        ['Finalized',    846]
    ],
    layoutAlgorithm="squarified",
    name="Unique Users")
chart.show()
