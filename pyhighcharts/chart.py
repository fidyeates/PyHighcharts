#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
chart.py

chart.py Module Docstring
"""
__all__ = ["ChartTypes", "Chart"]
__version__ = 0.1
__author__  = "Fin"

# Stdlib Imports
import string
import os
import tempfile
import webbrowser
import copy

# Third Party Imports

# pyhighcharts Imports
from util import safe_update, format_script_tag, \
    format_options, JS_TYPE


SHOW_TEMPLATE = """<html>
<head>
<meta charset="UTF-8">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js"></script>
<script src="http://code.highcharts.com/highcharts.js"></script>
<script src="http://code.highcharts.com/highcharts-more.js"></script>
<script src="http://code.highcharts.com/highcharts-3d.js"></script>
<script src="http://code.highcharts.com/modules/heatmap.js"></script>
<script src="http://code.highcharts.com/modules/treemap.js"></script>
<script src="http://code.highcharts.com/modules/funnel.js"></script>
<script src="https://code.highcharts.com/modules/drilldown.js"></script>
</head>
<body>
<div id="$container" style="height: 100%; width: 100%;"></div>

<script type='text/javascript'>
$chart
</script>

<body>
"""
SHOW_TEMPLATE = string.Template(SHOW_TEMPLATE)


class ChartTypes:
    area            = "area"
    arearange       = "arearange"
    areaspline      = "areaspline"
    areasplinerange = "areasplinerange"
    bar             = "bar"
    boxplot         = "boxplot"
    bubble          = "bubble"
    column          = "column"
    columnrange     = "columnrange"
    errorbar        = "errorbar"
    funnel          = "funnel"
    gauge           = "gauge"
    heatmap         = "heatmap"
    line            = "line"
    pie             = "pie"
    polygon         = "polygon"
    pyramid         = "pyramid"
    scatter         = "scatter"
    series          = "series"
    solidgauge      = "solidgauge"
    spline          = "spline"
    treemap         = "treemap"
    waterfall       = "waterfall"


class Chart(object):
    """
    A Chart object is a container for one or more data series, the chart itself
    will contain the setting and configuration for its children.
    """
    GLOBAL_OPTIONS = {}
    options = {}
    series = []

    def __init__(self, *series, **options):
        self.options = options
        self.series = list(series)
        self.container = "container"

        # Update this charts global options into its settings
        safe_update(self.options, self.GLOBAL_OPTIONS)

    def new(self):
        options = copy.deepcopy(self.options)
        series = copy.deepcopy(self.series)
        return Chart(*series, **options)

    def set_container(self, container):
        self.container = container

    def add_data_series(self, chart_type, data_points, **options):
        """
        add_data_series will add the provided data series to the chart object.

        Arguments:
            :param ChartTypes chart_type: The type of series we're adding
            :param list data_points: A list of data points, can be a list of
                values or a list of [x, y] values or [x, category] values.
            :param str name: The name of the data series
            :returns: None
            :raises: NotImplementedError
        """
        # Make sure we have the series option in the options dictionary
        if "series" not in self.options:
            self.options["series"] = self.series

        # Grab the series name
        new_series = {
            "data": data_points,
            "type": chart_type
        }

        # Logic to check if we're working as a timeseries
        if ('pointStart' in options) or ('pointInterval' in options):
            self.set_timeseries()

        new_series.update(options)
        self.series.append(new_series)

    def set_options(self, **options):
        """
        set_options will take the provided keyword arguments and update them
        into the internal settings dictionary of the chart.
        """
        safe_update(self.options, options)

    def show(self):
        """
        Show will open up a browser window and display the chart in browser.
        Use Chart.cleanup_temporary_files to remove these files, as they will
        not automatically clean up after themselves
        """
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        chart_content = self.script()
        file_content = SHOW_TEMPLATE.safe_substitute(container=self.container,
                                                     chart=chart_content)
        temp_file.write(file_content)
        temp_file.flush()
        handler = webbrowser.get()
        handler.open("file://" + temp_file.name)

    @staticmethod
    def cleanup_temporary_files(self):
        """
        cleanup_temporary_files will remove all the files created by the show
        method.
        """
        temp_dir = tempfile.gettempdir()
        file_list = os.listdir(temp_dir)
        file_names = filter(lambda s: s.startswith(tempfile.gettempprefix()),
                            file_list)
        map(lambda fn: os.remove(os.path.join(temp_dir, fn)), file_names)

    def script(self):
        return format_script_tag(container=self.container,
                                 options=format_options(self.options))

    # Helper Functions Just To Make Life Easier

    def set_title(self, text):
        """
        Sets the chart title to: text
        """
        safe_update(self.options, {"title": {"text": text}})

    def set_subtitle(self, text):
        """
        Sets the chart subtitle to: text
        """
        safe_update(self.options, {"subtitle": {"text": text}})

    def set_zoomable(self, axis="x"):
        """
        Sets the chart to be zoom-able and allows selection as to which axis it
        will zoom on. Available options, x, y, xy
        """
        safe_update(self.options, {"chart": {"zoomType": axis}})

    def set_timeseries(self):
        safe_update(self.options, {"xAxis": {"type": "datetime"}})

    def invert_axis(self):
        options = {
            "chart": {
                "inverted": True
            },
            "xAxis": {
                "reversed": False
            }
        }
        safe_update(self.options, options)

    def set_colours(self, colours):
        """
        Sets the colour pallet of the data series to the provided list:

        Example: ['#000', '#888', '#FFF']

        Arguments:
            :param list colours: A list of colours
        """
        safe_update(self.options, {"colors": colours})

    set_colors = set_colours  # For Americans

    def set_credits(self, enabled=True):
        """
        Sets the credits, to url or change if it is enabled or not:

        Arguments:
            :param bool enabled: If the credits are to be enabled or not
        """
        safe_update(self.options, {"credits": {"enabled": enabled}})

    def set_exporting(self, enabled=True):
        """
        Sets the exporting to enabled.

        Arguments:
            :param bool enabled: If exporting is enabled or not
        """
        safe_update(self.options, {"exporting": {"enabled": enabled}})

    def set_legend(self, enabled=True):
        """
        Sets the legend's visibility to enabled.

        Arguments:
            :param bool enabled: If the legend is to be visible or not.
        """
        safe_update(self.options, {"legend": {"enabled": enabled}})

    def set_yaxis_limits(self, ymin=None, ymax=None):
        to_update = {"yAxis": {}}
        if ymin is not None:
            to_update["yAxis"]["min"] = ymin
        if ymax is not None:
            to_update["yAxis"]["max"] = ymax
        safe_update(self.options, to_update)

    def set_yaxis_title(self, title):
        safe_update(self.options, {"yAxis": {"title": {"text": title}}})

    def set_xaxis_title(self, title):
        safe_update(self.options, {"xAxis": {"title": {"text": title}}})

    def set_categories(self, categories, axis="x"):
        to_update = {"%sAxis" % axis: {"categories": categories}}
        safe_update(self.options, to_update)

    def set_tooltip(self, **options):
        safe_update(self.options, {"tooltip": options})

    def make_3d(self, **options):
        """
        Makes a chart 3d
        """
        new_options = {
            "enabled": True,
            "alpha": 15,
            "beta": 15,
            "depth": 50,
            "viewDistance": 25
        }
        new_options.update(options)
        safe_update(self.options, {"chart": {"options3d": new_options}})

    def set_colour_axis(self, **options):
        defaults = {
            "min": 0,
            "minColor": "#FFFFFF",
            "maxColor": JS_TYPE("Highcharts.getOptions().colors[0]")
        }
        defaults.update(options)
        safe_update(self.options, {"colorAxis": defaults})

    # Alias
    set_color_axis = set_colour_axis
