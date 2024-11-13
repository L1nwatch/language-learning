#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" Description
"""

__author__ = '__L1n__w@tch'

from flask import Flask, render_template
from utils.common import TEMPLATES_ROOT, RESOURCE_ROOT

# Flask App Initialization
app = Flask(__name__, template_folder=TEMPLATES_ROOT, static_folder=RESOURCE_ROOT)


@app.route("/")
def home():
    return render_template("index.html")
