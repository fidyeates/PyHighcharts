#!/usr/bin/python
# -*- coding: UTF-8 -*-
""" PyHighcharts common.py
Common Functions For PyHighcharts
"""

FORMATTER_TYPE_MAPPINGS = {
    "default": "function() { return this.value }",
    "date": "function() { return''+Highcharts.dateFormat('%e. %b %Y \
        %H:00:00',this.x) + ': '+ this.y; }",
    "pie": "function() { return '<b>'+ this.point.name +'</b>: '+ \
    this.percentage +' %'; }",
    "pound_yAxis": "function() { '&#163' + return this.value }",
    "pound_tooltip": "function() { return''+ this.x + ': '+ '&#163' +this.y; }",
    "percent": "function() { return this.value + ' %' }",
    "default_tooltip": "function () { return'<b>'+ this.series.name + '</b>: ' + this.y; }",
    "percent_tooltip": "function () { return'<b>'+ this.series.name + '</b>: ' + this.y + ' %'; }",
    "date_percent_tooltip": "function () { return''+Highcharts.dateFormat('%e. %b %Y',this.x) + '<br><b>'+ this.series.name + '</b>: ' + this.y + ' %'; }",
}

class Formatter(object):
    """ Base Formatter Class """

    def __init__(self, format_type):
        self.__dict__.update({
            'formatter':FORMATTER_TYPE_MAPPINGS[format_type]
            })

def path_to_array(path):
    print path
    path = path.replace(r'/([A-Za-z])/g', r' $1 ')
    path = path.replace(r'/^\s*/', "").replace(r'/\s*$/', "")
    path = path.split(" ");
    for i, v in enumerate(path):
        try:
            path[i] = float(v)
        except:
            pass
    """
    for (var i = 0; i < path.length; i++) {
        if (!/[a-zA-Z]/.test(path[i])) {
            path[i] = parseFloat(path[i]);
        }
    }
    """
    return path


if __name__ == '__main__':
    print path_to_array("M 4687 2398 L 4679 2402 4679 2398 Z")