#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" Description
"""
import os
from pydub import AudioSegment
from gtts import gTTS
from utils.common import get_audio_path, RESOURCE_ROOT

__author__ = '__L1n__w@tch'


class Reviewer:
    listening_root = "/Users/watch/PycharmProjects/language-learning/data/listening"

    def _time_to_milliseconds(self, time_str):
        minutes, seconds = map(int, time_str.split(":"))
        return (minutes * 60 + seconds) * 1000

    def prepare_audio_segment(self, info):
        if info["type"] == "listening":
            audio_file = os.path.join(self.listening_root, info["file"])
            start_time, end_time = info["start_time"], info["end_time"]
            audio = AudioSegment.from_file(audio_file)
            segment = audio[self._time_to_milliseconds(start_time):self._time_to_milliseconds(end_time)]
            temp_file = get_audio_path()
            segment.export(os.path.join(RESOURCE_ROOT, temp_file), format="mp3")
            return temp_file
        elif info["type"] == "word":
            word = info["answer"]
            tts = gTTS(text=word, lang="en")
            temp_file = get_audio_path()
            tts.save(os.path.join(RESOURCE_ROOT, temp_file))
            return temp_file
