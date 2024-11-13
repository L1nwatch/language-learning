#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" Description
"""

__author__ = '__L1n__w@tch'

import os.path

ROOT = os.path.dirname(os.path.dirname(__file__))
RESOURCE_ROOT = os.path.join(ROOT, "static")
TEMPLATES_ROOT = os.path.join(ROOT, "templates")


def get_audio_path():
    return "segment.mp3"


def get_review_html_path():
    return "review.html"
