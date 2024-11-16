#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" Description
"""

__author__ = '__L1n__w@tch'

from applications.app import app
import applications.route_for_review
import applications.route_for_add

if __name__ == "__main__":
    app.run(debug=True, host="192.168.2.14")
