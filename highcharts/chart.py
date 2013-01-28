
from options import ChartOptions, ColorsOptions, CreditsOptions, \
	ExportingOptions, GlobalOptions, LabelsOptions, LangOptions, \
	LegendOptions, LoadingOptions, NavigationOptions, PaneOptions, \
	PlotOptions, SeriesData, SubtitleOptions, TitleOptions, \
	TooltipOptions, xAxisOptions, yAxisOptions 

from highchart_types import Series, SeriesOptions
from common import Formatter

# Stdlib Imports
import time, datetime, random, webbrowser, os

TMP_DIR = "/tmp/highcharts_tmp/"
DEFAULT_HEADERS = """<script type='text/javascript' src='https://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js'></script>\n<script src="http://code.highcharts.com/highcharts.js"></script>\n<script src="http://code.highcharts.com/modules/exporting.js"></script>"""

# Static Vars
base_template = "/development/PyHighcharts/templates/base.tmp"
show_template = "/development/PyHighcharts/templates/show_temp.tmp"

class HighchartError(Exception):

	def __init__(self, *args):
		self.args = args

class HighchartDefaults:
	pointInterval = 86400000


class Highchart(object):

	def __init__(self, **kwargs):

		# Bind Base Classes to self
		self.options = {
			"chart": ChartOptions(),
			"colors": ColorsOptions(),
			"credits": CreditsOptions(),
			"exporting": ExportingOptions(),
			"global": GlobalOptions(),
			"labels": LabelsOptions(),
			"lang": LangOptions(),
			"legend": LegendOptions(),
			"loading": LoadingOptions(),
			"navigation": NavigationOptions(),
			"pane": PaneOptions(),
			"plotOptions": PlotOptions(),
			"series": SeriesData(),
			"subtitle": SubtitleOptions(),
			"title": TitleOptions(),
			"tooltip": TooltipOptions(),
			"xAxis": xAxisOptions(),
			"yAxis": yAxisOptions(),
		}

		self.__load_defaults__()

		# Process kwargs
		allowed_kwargs = ["width","height","renderTo","backgroundColor"]

		for kw in allowed_kwargs:
			if kw in kwargs:
				self.options['chart'].update_dict(**{kw:kwargs[kw]})

		# Some Extra Vals to store: 
		self.data_set_count = 0

	def __render__(self,ret=False):
		with open(base_template,"rb") as f:
			tmp = f.read()
		rendered = tmp.format(**self.__export_options__())
		if ret: return rendered
		print rendered


	def __formatter__(self,option_type,data):

		FORMAT_SPECIAL_CASES = {
			"formatter": "formatter",
			"pointStart": "skip_quotes"
		}

		def update_tmp(tmp,k,v,type=None,tab_depth=1):
			if k not in FORMAT_SPECIAL_CASES:
				# Value Checking
				if isinstance(v,bool):
					# Convert Bool to js equiv.
					bool_mapping = {
						False: 'false',
						True: 'true',
					}
					v = bool_mapping[v]
				elif isinstance(v,str):
					# Need to keep string quotes
					v = "\'" + v + "\'"

				tmp+="\t"*tab_depth + "%s: %s,\n" % (k, v)
			else:
				if FORMAT_SPECIAL_CASES[k] == "skip_quotes":
					tmp+="\t"*tab_depth + "%s: %s,\n" % (k, v)
				elif k == "formatter":
					tmp+="\t"*tab_depth + "%s: %s,\n" % (k, v.formatter)
				else:
					raise NotImplementedError
			return tmp

		def color_formatter(data):
			return str(data['colors'])

		def series_formatter(data):
			t = ""
			for i, s in enumerate(data['data']):
				t+="{\n"
				for k, v in  s.__dict__.items():
					t = update_tmp(t,k,v,tab_depth=2)
				t+="\t},"
			return t

		# Special Cases
		SPECIAL_CASES = {
			"colors": color_formatter,
			"series": series_formatter,
		}
		tmp = ""


		if option_type in SPECIAL_CASES:
			tmp += SPECIAL_CASES[option_type](data)

		else:
			for k, v in data.items():
				if isinstance(v,dict):
					tmp += "\t%s: {\n" % k
					for sk, sv in v.items():
						tmp = update_tmp(tmp,sk, sv, tab_depth=3)
					tmp += "\t\t" + "},\n"

				elif isinstance(v,SeriesOptions):
					tmp += "\t%s: {\n" % k
					for sk, sv in v.__dict__.items():
						tmp = update_tmp(tmp,sk,sv, tab_depth=3)
					tmp += "\t\t" + "},\n"

				else:
					tmp = update_tmp(tmp,k, v)

		return tmp


	def __export_options__(self):
		d = {k:self.__formatter__(k,opClass.__dict__) for k, opClass in self.options.items()}
		return d


	def __load_defaults__(self):
		self.options["chart"].update_dict(renderTo='container')
		self.options["title"].update_dict(text='A New Highchart')
		self.options["yAxis"].update_dict(title_text='units') # Test Default Formatter Here
		self.options["credits"].update_dict(enabled=False)


	""" Standard Functions For Editing The Highchart: """

	def title(self, title=None):
		if not title:
			return self.options["title"].text
		else:
			self.options["title"].update_dict(text=title)

	def colors(self, colors=None):
		if not colors:
			return self.options["colors"].list()
		else:
			self.options["colors"].set_colors(colors)

	def chart_background(self,background=None):
		if not background:
			return self.options["chart"].backgroundColor
		else:
			self.options["chart"].update_dict(backgroundColor=background)

	def set_start_date(self,date):
		# Process Date and make sure chart is in Datetime mode, Need to set defaults
		if isinstance(date,float):
			date = datetime.datetime.fromtimestamp(date)
		elif not isinstance(date,datetime):	raise HighchartError("Start Date Format Currently Not Supported: %s" % date)
		date_dict = {
			"year": date.year,
			"month": date.month - 1,
			"day": date.day,
			"hour": date.hour,
		}
		formatted_date = "Date.UTC({year}, {month}, {day}, {hour}, 0, 0)".format(**date_dict)
		if not self.options['plotOptions'].__dict__: 
			self.hold_pointStart = formatted_date
			self.hold_pointInterval = HighchartDefaults.pointInterval
		for series_type, series_options in self.options['plotOptions'].__dict__.items():
			 series_options.process_kwargs({'pointStart':formatted_date},series_type=series_type)
			 if not 'pointInterval' in series_options.__dict__: series_options.process_kwargs({'pointInterval':HighchartDefaults.pointInterval},series_type=series_type,supress_errors=True)
		self.options['tooltip'].update_dict(formatter=Formatter('date'))
		self.options['xAxis'].update_dict(type='datetime')
		self.start_date_set = True


	def set_interval(self,interval):
		if not isinstance(interval,int): raise HighchartError("Interval Value Must Be An Integer")
		# Unset Any Held Values To Avoid Them Overwriting This Value
		if hasattr(self,'hold_pointInterval'): del self.hold_pointInterval
		if not self.options['plotOptions'].__dict__: self.hold_pointInterval = interval
		for series_type, series_options in self.options['plotOptions'].__dict__.items():
			 series_options.process_kwargs({'pointInterval':interval},series_type=series_type)

		if not self.start_date_set:
			print "Warning: If You Are Using A Date Interval: Make Sure You Set The Start Date With .set_start_date(date)"



	def add_data_set(self,data,series_type="line",name=None,**kwargs):
		# Update Plot Options With Defaults If None Exist
		self.data_set_count+=1		
		if not name: name = "Series %d" % self.data_set_count
		kwargs.update({'name':name})

		""" Could Do With A Convenient Wrapper Around This Part """
		if hasattr(self,'hold_pointStart'): 
			kwargs.update({"pointStart":self.hold_pointStart})
			del self.hold_pointStart
		if hasattr(self,'hold_pointInterval'): 
			kwargs.update({"pointInterval":self.hold_pointInterval})
			del self.hold_pointInterval
		if series_type not in self.options["plotOptions"].__dict__:
			self.options["plotOptions"].update_dict(**{series_type:SeriesOptions(series_type=series_type,supress_errors=True,**kwargs)})
		s = Series(data,series_type=series_type,supress_errors=True,**kwargs)
		self.options["series"].data.append(s)


	def set_options(self, options):
		""" Basic function for indexing stuff I haven't written convenience functions for yet """
		new_options = {}
		for k, option_data in options.items():
			d = {}
			for k2, v in option_data.items():
				if isinstance(v,dict):
					for k3, v2 in v.items():	d.update({k2+"_"+k3:v2})
				else:	d.update({k2:v})
			new_options.update({k:d})
		for k, v in new_options.items():
			self.options[k].update_dict(**v)


	def show(self):
		handle = webbrowser.get()
		if not os.path.exists(TMP_DIR): os.mkdir(TMP_DIR)
		new_fn = TMP_DIR + "%x.html" % (random.randint(pow(16,5),pow(16,6)-1))
		with open(show_template,'rb') as f:
			tmp = f.read()
		html = tmp.format(chart_data=self.__render__(ret=True))
		with open(new_fn,'wb') as f:
			f.write(html)
		handle.open("file://"+new_fn)


	def generate(self):
		return self.__render__(ret=True)


	@staticmethod
	def need():
		return DEFAULT_HEADERS

