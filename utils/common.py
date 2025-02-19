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
LISTENING_ROOT = "/Volumes/MyExternalDisk/the_big_bang_theory/S1"


def get_audio_files():
    global LISTENING_ROOT
    return os.listdir(LISTENING_ROOT)


def get_audio_path():
    global RESOURCE_ROOT
    os.makedirs(RESOURCE_ROOT, exist_ok=True)
    return os.path.join(RESOURCE_ROOT, "segment.mp3")


def get_review_html_path():
    return "review.html"
