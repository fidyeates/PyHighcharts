try:	
	import ujson as json
except ImportError:
	try:
		import json
	except ImportError:
		import simplejson as json





PLOT_OPTION_ALLOWED_ARGS = {
	"common": {
		"animation": bool,
		"color": str,
		"cursor": str,
		"dataLabels": NotImplemented,
		"enableMouseTracking": bool,
		"events": NotImplemented,
		"id": str,
		"point": NotImplemented,
		"selected": bool,
		"showCheckbox": bool,
		"showInLegend": bool,
		"states": NotImplemented,
		"stickyTracking": bool,
		"tooltip": NotImplemented,
		"visible": bool,
		"zIndex": int,
		"marker": dict
	},
	"area": {
		"allowPointSelect": bool,
		"connectEnds": bool,
		"connectNulls": bool,
		"cropThreshold": int,
		"dashStyle": str,
		"fillColor": str,
		"fillOpacity": float,
		"lineColor": str,
		"lineWidth": int,
		"marker": dict,
		"pointInterval": int,
		"pointPlacement": str,
		"pointStart": (int,str),
		"shadow": bool,
		"stacking": str,
		"threshold": int,
		"turboThreshold": int,
		"trackByArea": bool,
	},
	"arearange": {
		"allowPointSelect": bool,
		"connectNulls": bool,
		"cropThreshold": int,
		"dashStyle": str,
		"fillColor": str,
		"fillOpacity": float,
		"lineColor": str,
		"lineWidth": int,
		"pointInterval": int,
		"pointPlacement": str,
		"pointStart": (int,str),
		"shadow": bool,
		"turboThreshold": int,
		"trackByArea": bool,
	},
	"areaspline": {
		"allowPointSelect": bool,
		"cropThreshold": int,
		"connectEnds": bool,
		"connectNulls": bool,
		"dashStyle": str,
		"fillColor": str,
		"fillOpacity": float,		
		"lineColor": str,
		"lineWidth": int,
		"marker": dict,
		"pointInterval": int,
		"pointPlacement": str,
		"pointStart": (int,str),
		"shadow": bool,
		"stacking": str,
		"threshold": int,
		"turboThreshold": int,
		"trackByArea": bool,
	},
	"areasplinerange": {
		"allowPointSelect": bool,
		"connectNulls": bool,
		"cropThreshold": int,
		"dashStyle": str,
		"fillColor": str,
		"fillOpacity": float,
		"lineColor": str,
		"lineWidth": int,
		"pointInterval": int,
		"pointPlacement": str,
		"pointStart": (int,str),
		"shadow": bool,
		"turboThreshold": int,
		"trackByArea": bool,	
	},
	"bar": {
		"allowPointSelect": bool,
		"borderColor": str,
		"borderRadius": int,
		"borderWidth": int,
		"colorByPoint": bool,
		"cropThreshold": int,
		"groupPadding": float,
		"grouping": bool,
		"lineColor": str,
		"lineWidth": int,
		"minPointLength": int,
		"pointPadding": float,
		"pointRange": int,
		"pointWidth": int,
		"pointInterval": int,
		"pointPlacement": str,
		"pointStart": (int,str),
		"shadow": bool,
		"stacking": str,
		"turboThreshold": int,
	},
	"column": {
		"allowPointSelect": bool,
		"borderColor": str,
		"borderRadius": int,
		"borderWidth": int,
		"colorByPoint": bool,
		"cropThreshold": int,
		"groupPadding": (float, int),
		"grouping": bool,
		"lineColor": str,
		"lineWidth": int,
		"minPointLength": int,
		"pointPadding": float,
		"pointRange": int,
		"pointWidth": (int, float),
		"pointInterval": int,
		"pointPlacement": str,
		"pointStart": (int,str),
		"shadow": bool,
		"stacking": str,
		"turboThreshold": int,
	},
	"columnrange": {
		"allowPointSelect": bool,
		"borderColor": str,
		"borderRadius": int,
		"borderWidth": int,
		"colorByPoint": bool,
		"cropThreshold": int,
		"groupPadding": float,
		"grouping": bool,
		"lineColor": str,
		"lineWidth": int,
		"minPointLength": int,
		"pointPadding": float,
		"pointRange": int,
		"pointWidth": int,
		"pointInterval": int,
		"pointPlacement": str,
		"pointStart": (int,str),
		"shadow": bool,
		"stacking": str,
		"turboThreshold": int,
		"showInLegend": bool,

	},
	"gauge": {
		"dial": NotImplemented,
		"animation": bool,
		"color": NotImplemented,
		"cursor": NotImplemented,
		"dataLabels": NotImplemented,
		"dial": NotImplemented,
		"enableMouseTracking": bool,
		"events": NotImplemented,
		"id": NotImplemented,
		"linkedTo": NotImplemented,
		"negativeColor": NotImplemented,
		"pivot": NotImplemented,
		"point": NotImplemented,
		"selected": bool,
		"showCheckbox": bool,
		"showInLegend": NotImplemented,
		"states": NotImplemented,
		"stickyTracking": bool,
		"threshold": int,
		"tooltip": NotImplemented,
		"visible": bool,
		"wrap": bool,
		"zIndex": NotImplemented,
	},
	"line": {
		"allowPointSelect": bool,
		"connectEnds": bool,
		"connectNulls": bool,
		"cropThreshold": int,
		"dashStyle": str,
		"lineWidth": int,
		"marker": dict,
		"pointInterval": int,
		"pointPlacement": str,
		"pointStart": (int,str),
		"shadow": NotImplemented,
		"stacking": str,
		"step": str,
		"turboThreshold": int,
	},
	"pie": {
		"allowPointSelect": bool,
		"borderColor": str,
		"borderWidth": int,
		"center": list,
		"ignoreHiddenPoint": bool,
		"innerSize": int,
		"lineWidth": int,
		"marker": dict,
		"pointPlacement": str,
		"shadow": bool,
		"size": (int,str),
		"slicedOffset": int,
		"startAngle": int,
		"dataLabels": dict,
		"showInLegend": bool
	},
	"boxplot": {
		"allowPointSelect": bool,
		"borderColor": str,
		"borderWidth": int,
		"center": list,
		"ignoreHiddenPoint": bool,
		"innerSize": int,
		"lineWidth": int,
		"marker": dict,
		"pointPlacement": str,
		"shadow": bool,
		"size": (int,str),
		"slicedOffset": int,
		"startAngle": int,
		"dataLabels": dict,
		"showInLegend": bool
	},
	"scatter": {
		"allowPointSelect": bool,
		"connectNulls": bool,
		"cropThreshold": int,
		"dashStyle": str,
		"lineWidth": int,
		"marker": dict,
		"pointInterval": int,
		"pointPlacement": str,
		"pointStart": (int,str),
		"shadow": bool,
		"turboThreshold": int,
	},
	"series": {
		"allowPointSelect": bool,
		"connectEnds": bool,
		"connectNulls": bool,
		"cropThreshold": int,
		"dashStyle": str,
		"lineWidth": int,
		"marker": dict,
		"pointInterval": int,
		"pointPlacement": str,
		"pointStart": (int,str),
		"shadow": bool,
		"stacking": str,
		"turboThreshold": int,
	},
	"spline": {
		"allowPointSelect": bool,
		"connectEnds": bool,
		"connectNulls": bool,
		"cropThreshold": int,
		"dashStyle": str,
		"lineWidth": int,
		"marker": dict,
		"pointInterval": int,
		"pointPlacement": str,
		"pointStart": (int,str),
		"shadow": bool,
		"stacking": str,
		"turboThreshold": int,
	},
}

DATA_SERIES_ALLOWED_OPTIONS = {
    'color': str,
	"dataParser": NotImplemented,
	"dataURL": NotImplemented,
	"index": int,
	"legendIndex": int,
	"name": str,
	"stack": str,
	"type": str,
	"xAxis": int,
	"yAxis": int,
	"marker": dict,
    'showInLegend': bool,
    "visible": bool,
}

DEFAULT_OPTIONS = {

}

class OptionTypeError(Exception):

	def __init__(self,*args):
		self.args = args


class SeriesOptions(object):

	def __init__(self,series_type="line",supress_errors=False,**kwargs):
		self.load_defaults(series_type)
		self.process_kwargs(kwargs,series_type=series_type,supress_errors=supress_errors)

	@staticmethod
	def __validate_options__(k,v,ov):
		if isinstance(ov,list):
			for o in ov:
				if isinstance(v,o): return True
			else:
				raise OptionTypeError("Option Type Currently Not Supported: %s" % k)
		else:
			if ov == NotImplemented: raise OptionTypeError("Option Type Currently Not Supported: %s" % k)
			if isinstance(v,ov): return True
			else: return False

	def __options__(self):
		return self.__dict__

	def __display_options__(self):
		print json.dumps(self.__options__(),indent=4,sort_keys=True)

	def process_kwargs(self,kwargs,series_type,supress_errors=False):
		allowed_args = PLOT_OPTION_ALLOWED_ARGS[series_type]
		for k, v in kwargs.items():
			if k in allowed_args:
				if SeriesOptions.__validate_options__(k,v,allowed_args[k]):
					self.__dict__.update({k:v})
				else: 
					if not supress_errors: raise OptionTypeError("Option Type Mismatch: Expected: %s" % allowed_args[k])
			else: 
				if not supress_errors: raise OptionTypeError("Option: %s Not Allowed For Series Type: %s" % (k,series_type))

	def load_defaults(self,series_type):
		self.process_kwargs(DEFAULT_OPTIONS.get(series_type,{}),series_type)


class HighchartsError(Exception):

	def __init__(self, *args):
		self.args = args


class MultiAxis(object):

	def __init__(self, axis):
		self.axis = axis


class Series(object):

	def __init__(self,data,series_type="line",supress_errors=False,**kwargs):
		self.__dict__.update({
			"data": data,
			"type": series_type,
			})
		for k, v in kwargs.items():
			if k in DATA_SERIES_ALLOWED_OPTIONS:
				if SeriesOptions.__validate_options__(k,v,DATA_SERIES_ALLOWED_OPTIONS[k]):
					self.__dict__.update({k:v})
				else:
					if not supress_errors: raise OptionTypeError("Option Type Mismatch: Expected: %s" % DATA_SERIES_ALLOWED_OPTIONS[k])
			else:
				if not supress_errors: raise OptionTypeError("Option: %s Not Allowed For Data Series: %s" % (k, series_type))

