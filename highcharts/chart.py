#!/usr/bin/env python
""" PyHighcharts chart.py
A Wrapper around the Highcharts JS objects to dynamically generate
browser enabled charts on the fly.

For Highcharts Licencing Visit: 
http://shop.highsoft.com/highcharts.html
"""
from PyHighcharts.highcharts.options import ChartOptions, \
    ColorsOptions, CreditsOptions, ExportingOptions, \
    GlobalOptions, LabelsOptions, LangOptions, \
    LegendOptions, LoadingOptions, NavigationOptions, PaneOptions, \
    PlotOptions, SeriesData, SubtitleOptions, TitleOptions, \
    TooltipOptions, xAxisOptions, yAxisOptions 

from PyHighcharts.highcharts.highchart_types import Series, SeriesOptions, HighchartsError, MultiAxis
from PyHighcharts.highcharts.common import Formatter



# Stdlib Imports
import datetime, random, webbrowser, os, inspect
from _abcoll import Iterable

global TMP_DIR
TMP_DIR = "/tmp/highcharts_tmp/"
DEFAULT_HEADERS = """<script type='text/javascript' src=\
'https://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js'></script>
<script src="http://code.highcharts.com/highcharts.js"></script>
<script src="http://code.highcharts.com/highcharts-more.js"></script>
<script src="http://code.highcharts.com/modules/exporting.js"></script>"""

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
# Static Vars
BASE_TEMPLATE = ROOT_PATH + "/templates/base.tmp"
SHOW_TEMPLATE = ROOT_PATH + "/templates/show_temp.tmp"
GECKO_TEMPLATE = ROOT_PATH + "/templates/gecko_temp.tmp"

DEFAULT_POINT_INTERVAL = 86400000

FORMAT_SPECIAL_CASES = {
    "formatter": "formatter",
    "labelFormatter": "formatter",
    "pointStart": "skip_quotes",
    "events": "skip_quotes",
    "load": "skip_quotes",
    "multiaxis": "multiaxis"
}

def set_temp_dir(temp_dir):
    globals()['TMP_DIR'] = temp_dir

class HighchartError(Exception):
    """ Highcharts Error Class """
    def __init__(self, *args):
        Exception.__init__(self, *args)
        self.args = args

def color_formatter(data):
    """ Nothing to see here """
    return str(data['colors'])


def update_template(tmp, key, val, tab_depth=1):
    """ Generate Json Dicts """
    if key not in FORMAT_SPECIAL_CASES:
        # Value Checking
        if isinstance(val, dict):
            tmp += "\t%s: {\n" % key
            for subkey, subval in val.items():
                tmp = update_template(tmp, subkey, subval, tab_depth=3)
            tmp += "\t\t" + "},\n"
            return tmp
        elif isinstance(val, Iterable) and not isinstance(val, str):
            new_vals = []
            for item in val:
                if isinstance(item, dict):
                    ntmp = "{"
                    for k,v in item.items():
                        ntmp = update_template(ntmp, k, v, tab_depth=0)
                    ntmp += "}"
                    new_vals.append(ntmp)
                elif isinstance(item, Iterable) and not isinstance(item, str):
                    new_items = []
                    for subitem in item:
                        if isinstance(subitem, datetime.datetime):
                            utc = subitem.utctimetuple()
                            new_items.append("Date.UTC({year},{month},{day},{hours},{minutes},{seconds},{millisec})"
                                        .format(year=utc[0], month=utc[1]-1, day=utc[2], hours=utc[3], 
                                                minutes=utc[4], seconds=utc[5], millisec=subitem.microsecond/1000))
                        elif isinstance(subitem, bool):
                            # Convert Bool to js equiv.
                            bool_mapping = {
                                False: 'false',
                                True: 'true',
                            }
                            new_items.append(bool_mapping[subitem])
                        elif isinstance(subitem, str):
                            # Need to keep string quotes
                            new_items.append("\'" + subitem + "\'")
                        else:
                            new_items.append(str(subitem))
                    new_vals.append("[{}]".format(",".join(new_items)))
                elif isinstance(item, datetime.datetime):
                    utc = item.utctimetuple()
                    new_vals.append("Date.UTC({year},{month},{day},{hours},{minutes},{seconds},{millisec})"
                           .format(year=utc[0], month=utc[1], day=utc[2], hours=utc[3],
                                   minutes=utc[4], seconds=utc[5], millisec=item.microsecond/1000))
                elif isinstance(item, bool):
                    # Convert Bool to js equiv.
                    bool_mapping = {
                        False: 'false',
                        True: 'true',
                    }
                    new_vals.append(bool_mapping[item])
                elif item == None:
                    new_vals.append('null')
                elif isinstance(item, str):
                    # Need to keep string quotes
                    new_vals.append("\'" + item + "\'")
                else:
                    new_vals.append(str(item))
            return tmp + "{tabs}{key}:[{vals}],\n".format(tabs="\t"*tab_depth, key=key, vals=",".join(new_vals))
        elif isinstance(val, datetime.datetime):
            utc = val.utctimetuple()
            val = ("Date.UTC({year},{month},{day},{hours},{minutes},{seconds},{millisec})"
                    .format(year=utc[0], month=utc[1], day=utc[2], hours=utc[3],
                            minutes=utc[4], seconds=utc[5], millisec=val.microsecond/1000))
        elif isinstance(val, bool):
            # Convert Bool to js equiv.
            bool_mapping = {
                False: 'false',
                True: 'true',
            }
            val = bool_mapping[val]
        elif val == None:
            val = 'null'
        elif isinstance(val, str):
            # Need to keep string quotes
            val = "\'" + val + "\'"
        tmp += "\t"*tab_depth + "%s: %s,\n" % (key, val)
    else:
        if FORMAT_SPECIAL_CASES[key] == "skip_quotes":
            tmp += "\t"*tab_depth + "%s: %s,\n" % (key, val)
        elif FORMAT_SPECIAL_CASES[key] == "formatter":
            tmp += "\t"*tab_depth + "%s: %s,\n" % (key, val.formatter)
        elif FORMAT_SPECIAL_CASES[key] == "multiaxis":
            st = ""
            for k, v in val.__dict__.iteritems():
                st = update_template(st, k, v, tab_depth=tab_depth+1)
            return st
        else:
            raise NotImplementedError
    return tmp

def series_formatter(data):
    """ Special Formatting For Series """
    temp = ""
    for data_set in data['data']:
        temp += "{\n"
        for key, val in  data_set.__dict__.items():
            temp = update_template(temp, key, val, tab_depth=1)    
        temp += "\t},"
    return temp


def chart_formatter(option_type, data):
    """ Formatter Function """
    # Special Cases
    special_cases = {
        "colors": color_formatter,
        "series": series_formatter,
    }
    tmp = ""
    #print option_type, data
    if option_type in special_cases:
        tmp += special_cases[option_type](data)
    elif option_type == "yAxis" and data.get('axis'):
        tmp += "[{\n"
        for i, ax in enumerate(data['axis'], 1):
            tmp += update_template("", 'multiaxis', ax, tab_depth=1)
            if not i == len(data['axis']):
                tmp += "\t},{\n"
        tmp += "\t}]"
        print tmp
    else:
        tmp += "{\n" 
        for key, val in data.items():
            if isinstance(val, dict):
                tmp += "\t%s: {\n" % key
                for subkey, subval in val.items():
                    tmp = update_template(tmp, subkey, subval, tab_depth=3)
                tmp += "\t\t" + "},\n"
            elif isinstance(val, SeriesOptions):
                tmp += "\t%s: {\n" % key
                for subkey, subval in val.__dict__.items():
                    tmp = update_template(tmp, subkey, subval, tab_depth=3)
                tmp += "\t\t" + "},\n"
            else:
                tmp = update_template(tmp, key, val, tab_depth=2)
        tmp += "\t}"
    return tmp


class Highchart(object):
    """ Highchart Wrapper """

    def __init__(self, **kwargs):

        # Default Nulls // ? 
        self.hold_point_start = None
        self.hold_point_interval = None
        self.start_date_set = None

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
        allowed_kwargs = [
            "width", 
            "height", 
            "renderTo", 
            "backgroundColor", 
            "events", 
            "marginTop", 
            "marginRight", 
            "marginLeft"
        ]

        for keyword in allowed_kwargs:
            if keyword in kwargs:
                if keyword == 'events':
                    self.options['chart'].update_dict(**{'events':{kwargs['events'].event_type:kwargs['events'].event_method}})
                else:
                    self.options['chart'].update_dict(**{keyword:kwargs[keyword]})
        # Some Extra Vals to store: 
        self.data_set_count = 0


    def __render__(self, ret=False, template="base"):
        if template == "base":
            TEMPLATE = BASE_TEMPLATE
        elif template == "gecko":
            TEMPLATE = GECKO_TEMPLATE
        with open(TEMPLATE,"rb") as template_file:
            tmp = template_file.read()
        rendered = tmp.format(**self.__export_options__())
        if ret: 
            return rendered


    def __export_options__(self):
        bind = self.options.items()
        data = {k:chart_formatter(k, opClass.__dict__) \
            for k, opClass in bind}
        return data


    def __load_defaults__(self):
        self.options["chart"].update_dict(renderTo='container')
        self.options["title"].update_dict(text='A New Highchart')
        self.options["yAxis"].update_dict(title_text='units') 
        self.options["credits"].update_dict(enabled=False)


    def title(self, title=None):
        """ Bind Title """
        if not title:
            return self.options["title"].text
        else:
            self.options["title"].update_dict(text=title)


    def colors(self, colors=None):
        """ Bind Color Array """
        if not colors:
            return self.options["colors"].__dict__.values() if self.options['colors'] is not None else []
        else:
            self.options["colors"].set_colors(colors)


    def chart_background(self, background=None):
        """ Apply Chart Background """
        if not background:
            return self.options["chart"].backgroundColor
        else:
            self.options["chart"].update_dict(backgroundColor=background)


    def set_start_date(self, date):
        """ Set Plot Start Date """
        if isinstance(date, (int, float)):
            date = datetime.datetime.fromtimestamp(date)
        elif not isinstance(date, datetime.datetime):
            error = "Start Date Format Currently Not Supported: %s" % date
            raise HighchartError(error)
        date_dict = {
            "year": date.year,
            "month": date.month - 1,
            "day": date.day,
            "hour": date.hour,
            "minute": date.minute,
            "second": date.second,
        }
        formatted_date = "Date.UTC({year}, {month}, {day}, {hour}, {minute}, {second})"
        formatted_date = formatted_date.format(**date_dict)
        if not self.options['plotOptions'].__dict__: 
            self.hold_point_start = formatted_date
            self.hold_point_interval = DEFAULT_POINT_INTERVAL
        hold_iterable = self.options['plotOptions'].__dict__.items()
        for series_type, series_options in hold_iterable:
            series_options.process_kwargs({'pointStart':formatted_date},
                series_type=series_type)
            if not 'pointInterval' in series_options.__dict__: 
                series_options.process_kwargs({
                    'pointInterval':DEFAULT_POINT_INTERVAL},
                    series_type=series_type,
                    supress_errors=True)
        self.options['tooltip'].update_dict(formatter=Formatter('date'))
        self.options['xAxis'].update_dict(type='datetime')
        self.start_date_set = True


    def set_interval(self, interval):
        """ Set Plot Step Interval """
        if not isinstance(interval, int): 
            raise HighchartError("Interval Value Must Be An Integer")
        # Unset Any Held Values To Avoid Them Overwriting This Value
        if self.hold_point_interval: 
            self.hold_point_interval = None
        if not self.options['plotOptions'].__dict__: 
            self.hold_point_interval = interval
        for hold_item in self.options['plotOptions'].__dict__.items():
            series_type, series_options = hold_item
            series_options.process_kwargs({'pointInterval':interval},
                series_type=series_type)
        if not self.start_date_set:
            print "Set The Start Date With .set_start_date(date)"


    def add_data_set(self, data, series_type="line", name=None, **kwargs):
        """ Update Plot Options With Defaults If None Exist """
        self.data_set_count += 1      
        if not name: 
            name = "Series %d" % self.data_set_count
        kwargs.update({'name':name})
        if self.hold_point_start: 
            kwargs.update({"pointStart":self.hold_point_start})
            self.hold_point_start = None
        if self.hold_point_interval: 
            kwargs.update({"pointInterval":self.hold_point_interval})
            self.hold_point_interval = None
        if series_type not in self.options["plotOptions"].__dict__:
            to_update = {series_type:SeriesOptions(series_type=series_type,
                supress_errors=True, **kwargs)}
            self.options["plotOptions"].update_dict(**to_update)
        series_data = Series(data, series_type=series_type, \
            supress_errors=True, **kwargs)
        self.options["series"].data.append(series_data)


    def set_options(self, options, force_options=False):
        """ Set Plot Options """
        if force_options:
            for k, v in options.items():
                self.options.update({k:v})
        else:
            new_options = {}
            for key, option_data in options.items():
                data = {}
                for key2, val in option_data.items():
                    if isinstance(val, dict):
                        for key3, val2 in val.items():    
                            data.update({key2+"_"+key3:val2})
                    else:   
                        data.update({key2:val})
                new_options.update({key:data})
            for key, val in new_options.items():
                self.options[key].update_dict(**val)


    def show(self):
        """ Show Function """
        handle = webbrowser.get()
        if not os.path.exists(TMP_DIR): 
            os.mkdir(TMP_DIR)
        new_filename = "%x.html" % (random.randint(pow(16, 5), pow(16, 6)-1))
        temp_dir = globals()['TMP_DIR']
        if not temp_dir[-1] == "/":
            temp_dir += "/"
        new_fn = temp_dir + new_filename
        with open(SHOW_TEMPLATE, 'rb') as file_open:
            tmp = file_open.read()
        html = tmp.format(chart_data=self.__render__(ret=True))
        with open(new_fn, 'wb') as file_open:
            file_open.write(html)
        handle.open("file://"+new_fn)


    def generate(self):
        """ __render__ Wrapper """
        return self.__render__(ret=True)


    def set_yAxis(self, *axis):
        if all(map(lambda a: isinstance(a, yAxisOptions), axis)):
            self.options['yAxis'] = MultiAxis(axis)
        else:
            raise HighchartsError("All Axis Must Be Of Type: yAxisOptions")



    @staticmethod
    def need():
        """ Returns Header """
        return DEFAULT_HEADERS

