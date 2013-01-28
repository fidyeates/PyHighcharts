# PyHighcharts

A convenient wrapper for Highchart generation procedurally or on the command-line to browser output.


## General Usage

Using Highcharts is so simple: You can even doing it on the command line!

<pre><code>H = Highchart(width='500 px',height='500 px',renderTo='container')
data = [1,2,3,4,5,6,7,8,9,10]
H.add_data_set(data,type='line',name='test_data')
H.show()</code></pre>

This show() function generates a temporary HTML file and opens up the chart for viewing in your default browser


This Highcharts codebase was primarily developed for use within templating: And that is easy to do also!

<pre>
<code> 
\<html>
\<head>
{ Highcharts.need() }
\</head>
\<body>
\<div id='container'></div>
\<script>
{ test_highchart_content }
\</script>
\</body>
\</html>
</code>
</pre>

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
