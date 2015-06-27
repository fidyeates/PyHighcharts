#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
maps.py
"""

__all__ = ["Map"]
__author__  = "Fin"

# Stdlib Imports
import string
import tempfile
import webbrowser

# Third Party Imports

# DSP Imports
from util import format_map_tag, format_options, safe_update
from chart import Chart

SHOW_TEMPLATE = """<html>
<head>
<meta charset="UTF-8">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js"></script>
<script src="http://cdnjs.cloudflare.com/ajax/libs/proj4js/2.2.2/proj4.js"></script>
<script src="http://code.highcharts.com/maps/highmaps.js"></script>
<script src="http://code.highcharts.com/maps/modules/exporting.js"></script>
<script src="http://code.highcharts.com/mapdata/countries/gb/gb-all.js"></script>
</head>
<body>
<div id="$container" style="height: 100%; width: 100%;"></div>

<script type='text/javascript'>
$chart
</script>

<body>
"""
SHOW_TEMPLATE = string.Template(SHOW_TEMPLATE)


class Map(Chart):

    def script(self):
        return format_map_tag(container=self.container,
                              options=format_options(self.options))

    def allow_navigation(self, b):
        safe_update(self.options, {"mapNavigation": {"enabled": b}})

    def set_map_base(self, **options):
        # Make sure we have the series option in the options dictionary
        if "series" not in self.options:
            self.options["series"] = self.series

        defaults = {
            "name": "Basemap",
            "borderColor": "#A0A0A0",
            "nullColor": "rgba(200, 200, 200, 0.3)",
            "showInLegend": False
        }
        defaults.update(options)
        self.series.insert(0, defaults)

    def set_seperators(self, **options):
        # Make sure we have the series option in the options dictionary
        if "series" not in self.options:
            self.options["series"] = self.series

        defaults = {
            "name": "Separators",
            "type": "mapline",
            "color": "#707070",
            "showInLegend": False,
            "enableMouseTracking": False
        }
        defaults.update(options)
        print self.series
        if len(self.series) > 0:
            self.series.insert(1, defaults)

    def add_data_points(self, **options):
        # Make sure we have the series option in the options dictionary
        if "series" not in self.options:
            self.options["series"] = self.series

        self.series.append(options)

    def show(self):
        """
        Show will open up a browser window and display the chart in browser.
        Use Chart.cleanup_temporary_files to remove these files, as they will
        not automatically clean up after themselves

        TODO: Map data
        """
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        chart_content = self.script()
        file_content = SHOW_TEMPLATE.safe_substitute(container=self.container,
                                                     chart=chart_content)
        temp_file.write(file_content)
        temp_file.flush()
        handler = webbrowser.get()
        handler.open("file://" + temp_file.name)
