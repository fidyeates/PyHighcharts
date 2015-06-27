#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
map_example.py
"""

__author__  = "Fin"

# Stdlib Imports

# Third Party Imports
from pyhighcharts import Map, JS_TYPE

map_chart = Map()
map_chart.set_title("Highmaps Basic lat/lon demo")
map_chart.allow_navigation(True)
map_chart.set_map_base(mapData=JS_TYPE("Highcharts.maps['countries/gb/gb-all']"))
map_chart.set_seperators(data=JS_TYPE("Highcharts.geojson(Highcharts.maps['countries/gb/gb-all'], 'mapline')"))
map_chart.add_data_points(
    type="mappoint",
    name="Cities",
    color=JS_TYPE("Highcharts.getOptions().colors[1]"),
    data=[{
        "name": "London",
        "lat": 51.507222,
        "lon": -0.1275
    }, {
        "name": "Birmingham",
        "lat": 52.483056,
        "lon": -1.893611
    }, {
        "name": "Leeds",
        "lat": 53.799722,
        "lon": -1.549167
    }, {
        "name": "Glasgow",
        "lat": 55.858,
        "lon": -4.259
    }, {
        "name": "Sheffield",
        "lat": 53.383611,
        "lon": -1.466944
    }, {
        "name": "Liverpool",
        "lat": 53.4,
        "lon": -3
    }, {
        "name": "Bristol",
        "lat": 51.45,
        "lon": -2.583333
    }, {
        "name": "Belfast",
        "lat": 54.597,
        "lon": -5.93
    }, {
        "name": "Lerwick",
        "lat": 60.155,
        "lon": -1.145,
        "dataLabels": {
            "align": "left",
            "x": 5,
            "verticalAlign": "middle"
        }
    }])
map_chart.show()
