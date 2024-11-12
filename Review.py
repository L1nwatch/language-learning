#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" Description
"""
import os
from pydub import AudioSegment


__author__ = '__L1n__w@tch'


class Review:
    listening_root = "/Users/watch/PycharmProjects/language-learning/data/listening"

    def _time_to_milliseconds(self, time_str):
        minutes, seconds = map(int, time_str.split(":"))
        return (minutes * 60 + seconds) * 1000

    def prepare_audio_segment(self, info):
        audio_file = os.path.join(self.listening_root, info["file"])
        start_time, end_time = info["start_time"], info["end_time"]
        audio = AudioSegment.from_file(audio_file)
        segment = audio[self._time_to_milliseconds(start_time):self._time_to_milliseconds(end_time)]
        temp_file = "static/segment.mp3"
        segment.export(temp_file, format="mp3")
        return temp_file


