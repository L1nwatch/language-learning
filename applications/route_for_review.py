#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" Description
"""
import os
from applications.app import app
from DataManager import DataManager
from Reviewer import Reviewer
from flask import render_template, request, redirect, url_for
from utils.common import get_audio_path, get_review_html_path
from difflib import Differ

__author__ = '__L1n__w@tch'

reviewer = Reviewer()
# Load cases
DM = DataManager()
CASES = DM.load_cases()
# Global variables
CURRENT_CASE_INDEX = -1  # Start without any active case
CURRENT_CASE = dict()  # Active case
TOTAL_CASES = len(CASES)  # Total number of audio cases
PROGRESS = {"completed": CURRENT_CASE_INDEX + 1, "total": TOTAL_CASES}


def _highlight_differences(user_input, correct_answer):
    differ = Differ()
    comparison = list(differ.compare(correct_answer.split(), user_input.split()))
    highlighted = []
    for word in comparison:
        if word.startswith("+"):
            highlighted.append(f"<span style='color: green;'>{word[2:]}</span>")
        elif word.startswith("-"):
            highlighted.append(f"<span style='color: red;'>{word[2:]}</span>")
        else:
            highlighted.append(word[2:])
    return " ".join(highlighted)


def _initialize_index():
    global CURRENT_CASE_INDEX, CASES, CURRENT_CASE, PROGRESS, TOTAL_CASES

    # Load the first listening case if no case is active
    if CURRENT_CASE_INDEX == -1:
        CURRENT_CASE_INDEX = 0
        CURRENT_CASE = CASES[CURRENT_CASE_INDEX]
        reviewer.prepare_audio_segment(CURRENT_CASE)
        PROGRESS["completed"] = CURRENT_CASE_INDEX + 1

    return render_template(
        get_review_html_path(),
        feedback=None,
        audio_file=url_for('static', filename='segment.mp3', q=str(os.path.getmtime(get_audio_path()))),
        user_input="",
        progress=PROGRESS,
        case_info=CURRENT_CASE
    )


def _index_next():
    global CURRENT_CASE_INDEX, CASES, CURRENT_CASE, PROGRESS
    CURRENT_CASE_INDEX += 1
    if CURRENT_CASE_INDEX >= len(CASES):
        CURRENT_CASE_INDEX = 0  # Loop back to the first case
    CURRENT_CASE = CASES[CURRENT_CASE_INDEX]
    reviewer.prepare_audio_segment(CURRENT_CASE)
    PROGRESS["completed"] = CURRENT_CASE_INDEX + 1
    return render_template(
        get_review_html_path(),
        feedback=None,
        audio_file=url_for('static', filename='segment.mp3', q=str(os.path.getmtime(get_audio_path()))),
        user_input="",
        progress=PROGRESS,
        case_info=CURRENT_CASE
    )


def _get_feedback(user_answer, correct_answer):
    if user_answer == correct_answer:
        return "<span style='color: green;'>Correct! 🎉</span>"
    return _highlight_differences(user_answer, correct_answer)


def _index_post(user_input):
    global CURRENT_CASE_INDEX, CASES, CURRENT_CASE, PROGRESS
    if "next" in request.form:  # Handle "Next Audio" button click
        return _index_next()

    # Handle form submission (user's answer)
    user_answer = user_input.lower()
    correct_answer = CURRENT_CASE.get("answer", "").strip().lower()
    feedback = _get_feedback(user_answer, correct_answer)
    DM.save_result(CURRENT_CASE, user_answer == correct_answer, feedback)

    return render_template(
        get_review_html_path(),
        feedback=feedback,
        audio_file=url_for('static', filename='segment.mp3', q=str(os.path.getmtime(get_audio_path()))),
        user_input=user_input,
        progress=PROGRESS,
        case_info=CURRENT_CASE
    )


@app.route("/review", methods=["GET", "POST"])
def review():
    global CURRENT_CASE_INDEX, CASES, CURRENT_CASE

    if request.method == "POST":
        user_input = request.form.get("answer", "").strip()  # Get user input
        return _index_post(user_input)

    return _initialize_index()


@app.route("/replay")
def replay_audio():
    return redirect(url_for('review'))
