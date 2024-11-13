#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" Description
"""

__author__ = '__L1n__w@tch'

import os.path

ROOT = os.path.dirname(os.path.dirname(__file__))
RESOURCE_ROOT = os.path.join(ROOT, "static")


def get_audio_path():
    global RESOURCE_ROOT
    return os.path.join(RESOURCE_ROOT, "segment.mp3")
