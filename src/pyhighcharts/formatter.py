#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
formatter.py
"""

__author__  = "Fin"

# Stdlib Imports

# Third Party Imports
from util import dict_to_js


class Formatter:

    @staticmethod
    def format(dictionary):
        """
        Format will take a python dictionary and turn it into
        a javascript object for rendering within a page.

        Arguments:
            :param dict dictionary: the dictionary to convert
            :returns: str
            :raises: TypeError
        """
        return dict_to_js(dictionary)
