#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" PyHighcharts: examples.py
Basic Examples 
"""
from PyHighcharts.highcharts.chart import Highchart
import math, random

EXAMPLE_CONFIG = {
    "xAxis": {
        "gridLineWidth": 0,
        "lineWidth": 0,
        "tickLength": 0,
    },
    "yAxis": {
            "gridLineWidth": 0,
    }
}

def pie_example_unicode_chars():
    """ Basic Piechart Example """
    chart = Highchart()
    chart.title(u"Pac Man Highchart with non-ascii chars ą")
    chart.add_data_set([[u"Does Not Resemble Pac Man ą", 25],
        ["Resembes Pac Man", 75]],
        series_type="pie",
        name="",
        startAngle=45)
    chart.colors(["#99CCFF", "#FFFF66"])
    chart.set_options(EXAMPLE_CONFIG)
    chart.show()


def spline_example():
    """ Basic Spline Example """
    chart = Highchart()
    data = [math.sin(x/100.0) \
        for x in range(0, int(4*math.pi*100), int(math.pi/16*100))]
    chart.title("Sin Spline")
    chart.add_data_set(data, series_type="spline", name="Sin")
    chart.set_options(EXAMPLE_CONFIG)
    chart.show()


def area_example():
    """ Basic Area Exampls """
    chart = Highchart()
    data = [i**2 for i in range(10)]
    chart.title("Area Example")
    chart.add_data_set(data, series_type="area", name="Area")
    chart.set_options(EXAMPLE_CONFIG)
    chart.show()


def multiple_example():
    """ Basic Multiple Exampls """
    chart = Highchart()
    revenue = [random.randint(1000, 7000) for i in range(24)]
    spend = [random.randint(2000, 4000) for i in range(24)]
    profit = [r - spend[i] for i, r in enumerate(revenue)]
    cumulative_profit = [sum(profit[:i])+5000 for i in range(len(profit))]
    chart.title("Multiple Example")
    chart.add_data_set(revenue, series_type="line", name="Revenue", index=2)
    chart.add_data_set(spend, series_type="line", name="Spend", index=3)
    chart.add_data_set(cumulative_profit, 
        series_type="area", 
        name="Balance",
        index=1)
    chart.set_options(EXAMPLE_CONFIG)
    chart.show()


if __name__ == '__main__':
    multiple_example()