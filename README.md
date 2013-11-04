# PyHighcharts

A convenient wrapper for Highchart generation procedurally or on the command-line to browser output.

For documentation on highcharts visit: <a href="http://api.highcharts.com/highcharts" target="_blank">Highcharts API</a>

And remember Highcharts is only free for non-commercial use: Pop over to <a href="http://shop.highsoft.com/highcharts.html" target="_blank">Highcharts Licensing</a> for more info!

## General Usage

Using Highcharts is so simple: You can even do it on the command line!

<pre><code>from PyHighcharts import Highchart
H = Highchart(width=500, height=500, renderTo='container')
data = [1,2,3,4,5,6,7,8,9,10]
H.add_data_set(data,type='line',name='test_data')
H.show()</code></pre>

This show() function generates a temporary HTML file and opens up the chart for viewing in your default browser


This Highcharts codebase was primarily developed for use within templating: And that is easy to do also!

	<html>
	<head>
		{ Highcharts.need() }
	</head>
	<body>
	<div id='container'></div>
	<script>
		{ test_highchart_content }
	</script>
	</body>
	</html>

All you need to do is pass in the highcharts pre-generated with the generate() function to your templates within some script tags (And don't forget to correctly name the id's of the divs!)

## Currently Supoorts

- Line
- Spline
- Area
- AreaRange
- AreaSpline
- AreaSplineRange
- Gauge
- Bar
- Column
- Scatter
- ColumnRange
- Pie
- Series

## Examples

There is a few examples within /highcharts/examples.py to try out

<img src="https://raw.github.com/fidyeates/PyHighcharts/master/images/chart.png">
