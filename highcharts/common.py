#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Base Formatters

FORMATTER_TYPE_MAPPINGS = {
	"default": "function() { return this.value }",
	"date": "function() { return''+Highcharts.dateFormat('%e. %b %Y %H:00:00',this.x) + ': '+ this.y; }",
	"pie": "function() { return '<b>'+ this.point.name +'</b>: '+ this.percentage +' %'; }",
	"pound_yAxis": "function() { '&#163' + return this.value }",
	"pound_tooltip": "function() { return''+ this.x + ': '+ '&#163' +this.y; }"
}

class Formatter(object):

	def __init__(self,type):
		self.__dict__.update({'formatter':FORMATTER_TYPE_MAPPINGS[type]})