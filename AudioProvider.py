#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" Description
"""
import os
from pydub import AudioSegment
from gtts import gTTS
from utils.common import get_audio_path, RESOURCE_ROOT, LISTENING_ROOT

__author__ = '__L1n__w@tch'


class AudioProvider:
    listening_root = LISTENING_ROOT

    def get_audio_file(self, file_name):
        roots = [self.listening_root, "./data/listening", "/Volumes/MyExternalDisk/the_big_bang_theory/S1"]
        for root in roots:
            path = os.path.join(root, file_name)
            if os.path.exists(path):
                return path
        return None

    def _minute_time_to_milliseconds(self, time_str):
        minutes, seconds = map(int, time_str.split(":"))
        return (minutes * 60 + seconds) * 1000

    def get_segment(self, audio, start_time, end_time):
        if start_time.count(":") == 1:
            return audio[self._minute_time_to_milliseconds(start_time):self._minute_time_to_milliseconds(end_time)]
        elif start_time.count(":") == 2:
            return audio[self._hour_time_to_milliseconds(start_time):self._hour_time_to_milliseconds(end_time)]

    def prepare_audio_segment(self, info):
        if info["type"] == "listening":
            audio_file = self.get_audio_file(info["file"])
            start_time, end_time = info["start_time"], info["end_time"]
            audio = AudioSegment.from_file(audio_file)
            segment = self.get_segment(audio, start_time, end_time)
            temp_file = get_audio_path()
            segment.export(os.path.join(RESOURCE_ROOT, temp_file), format="mp3")
            return temp_file
        elif info["type"] == "word":
            word = info["answer"]
            tts = gTTS(text=word, lang="en")
            temp_file = get_audio_path()
            tts.save(os.path.join(RESOURCE_ROOT, temp_file))
            return temp_file

    def _hour_time_to_milliseconds(self, time_str):
        """Convert HH:MM:SS format to milliseconds"""
        h, m, s = map(int, time_str.split(":"))
        return (h * 3600 + m * 60 + s) * 1000

    def extract_audio_segment(self, input_file, start_time, end_time, output_file):
        """
        Extracts a specific audio segment from a video file.

        :param input_file: Path to the input video file (MKV/MP4)
        :param start_time: Start time in HH:MM:SS format
        :param end_time: End time in HH:MM:SS format
        :param output_file: Path to save the extracted audio segment
        """
        # Load the audio from the video file
        audio = AudioSegment.from_file(input_file)

        # Convert HH:MM:SS to milliseconds
        start_ms = self._hour_time_to_milliseconds(start_time)
        end_ms = self._hour_time_to_milliseconds(end_time)

        # Extract the audio segment
        segment = audio[start_ms:end_ms]

        # Export the extracted audio
        segment.export(output_file, format="mp3")


if __name__ == "__main__":
    input_video = "/Volumes/MyExternalDisk/the_big_bang_theory/S1/S01E01.mkv"
    output_audio = "output_segment.mp3"
    ap = AudioProvider()
    ap.extract_audio_segment(input_video, start_time="00:00:10", end_time="00:00:20", output_file=output_audio)
