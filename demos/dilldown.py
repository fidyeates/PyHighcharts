#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
timeseries.py

Highcharts timeseries example
"""

__author__  = "Fin"

# Stdlib Imports
from datetime import datetime

# Third Party Imports
from pyhighcharts import Chart, ChartTypes

drilldown_data = [{
    "name": 'Animals',
    "y": 5,
    "drilldown": 'animals'
}, {
    "name": 'Fruits',
    "y": 2,
    "drilldown": 'fruits'
}, {
    "name": 'Cars',
    "y": 4,
    "drilldown": 'cars'
}]

drilldown = {
    "series": [{
        "id": 'animals',
        "type": "column",
            "data": [
                ['Cats', 4],
                ['Dogs', 2],
                ['Cows', 1],
                ['Sheep', 2],
                ['Pigs', 1]
            ]
        }, {
            "id": 'fruits',
            "type": "column",
            "data": [
                ['Apples', 4],
                ['Oranges', 2]
            ]
        }, {
            "id": 'cars',
            "type": "column",
            "data": [
                ['Toyota', 4],
                ['Opel', 2],
                ['Volkswagen', 2]
            ]
        }
    ]
}
chart = Chart()
chart.set_title("Drilldown Example")
chart.set_yaxis_title("Count")
chart.add_data_series(
    ChartTypes.column,
    drilldown_data,
    colorByPoint=True,
    name="Things")
chart.set_options(drilldown=drilldown)
chart.show()
