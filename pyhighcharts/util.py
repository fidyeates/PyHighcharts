#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
util.py

util.py Module Docstring
"""

__author__  = "Fin"

# Stdlib Imports
from datetime import datetime
import collections
import string
from types import *

# Third Party Imports

# pyhighcharts Imports


class JS_TYPE(object):

    def __init__(self, raw):
        self.raw = raw


def safe_update(target, origin):
    for key, value in origin.iteritems():
        if isinstance(value, collections.Mapping):
            target[key] = safe_update(target.get(key, {}), value)
        else:
            target[key] = value
    return target


SCRIPT_TEMPLATE = """$$(function () {
    $$('#$container').highcharts($options);
});"""
SCRIPT_TEMPLATE = string.Template(SCRIPT_TEMPLATE)
SCRIPT_TEMPLATE_DEFAULTS = {
    "container": "container",
    "options": "",
}


def format_script_tag(**format_options):
    format_options = safe_update(SCRIPT_TEMPLATE_DEFAULTS.copy(), format_options)
    return SCRIPT_TEMPLATE.safe_substitute(**format_options)


MAP_SCRIPT_TEMPLATE = """$$(function () {
    $$('#$container').highcharts('Map', $options);
});"""
MAP_SCRIPT_TEMPLATE = string.Template(MAP_SCRIPT_TEMPLATE)
MAP_SCRIPT_TEMPLATE_DEFAULTS = {
    "container": "container",
    "options": "",
}


def format_map_tag(**format_options):
    format_options = safe_update(MAP_SCRIPT_TEMPLATE_DEFAULTS.copy(), format_options)
    return MAP_SCRIPT_TEMPLATE.safe_substitute(**format_options)


OPTION_TEMPLATE = "$data"
OPTION_TEMPLATE = string.Template(OPTION_TEMPLATE)


def format_options(data):
    formatted_data = dict_to_js(data)
    return OPTION_TEMPLATE.safe_substitute(data=formatted_data)

# Custom Formatters
FORMATTERS = {
    bool: lambda v: "true" if v else "false",
    NoneType: lambda _: "null",
    datetime: lambda d: "Date.UTC({}, {}, {})".format(d.year, (d.month - 1), d.day),
    JS_TYPE: lambda js: js.raw
}

INDENT = "  "


def format_value(value, depth=2):
    value_type = type(value)
    if value_type in FORMATTERS:
        return FORMATTERS[value_type](value)
    else:
        if isinstance(value, basestring):
            value = str(value)
        return "%r" % value


def list_to_js(l, depth=2):
    s = "["
    l_len = len(l)
    for index, item in enumerate(l, 1):
        if isinstance(item, collections.Mapping):
            s += dict_to_js(item, depth=depth)
        elif isinstance(item, (list, tuple)):
            s += list_to_js(item, depth=depth+1)
        else:
            item = format_value(item, depth=depth)
            s += "%s" % (item)
        s += "%s" % (", " if index != l_len else "")
    s += "]"
    return s


def dict_to_js(d, depth=2):
    s = "{\n"
    d_size = len(d)
    for index, (key, value) in enumerate(d.items(), 1):
        s += (INDENT * depth)
        s += ("%s: " % key)
        if isinstance(value, collections.Mapping):
            s += dict_to_js(value, depth=depth+1)
        elif isinstance(value, (list, tuple)):
            s += list_to_js(value, depth=depth+1)
        else:
            value = format_value(value, depth=depth)
            s += "%s" % value
        s += "%s\n" % ("," if index != d_size else "")
    s += (INDENT * (depth - 1)) + "}"
    return s
