#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" Description
"""

__author__ = '__L1n__w@tch'

import os
import json
from Review import Review
from flask import Flask, render_template, request, redirect, url_for
from difflib import Differ

# Flask App Initialization
app = Flask(__name__)
review = Review()

# Load cases
with open("data/cases.json", "r") as f:
    CASES = json.load(f)

# Global variables
CURRENT_CASE_INDEX = -1  # Start without any active case
CURRENT_CASE = None  # Active case
TOTAL_CASES = len(CASES)  # Total number of audio cases
PROGRESS = f"{CURRENT_CASE_INDEX + 1}/{TOTAL_CASES}" if CURRENT_CASE_INDEX >= 0 else "0/0"


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
        review.prepare_audio_segment(CURRENT_CASE)
        PROGRESS = f"{CURRENT_CASE_INDEX + 1}/{TOTAL_CASES}"

    return render_template(
        "index.html",
        feedback=None,
        audio_file=url_for('static', filename='segment.mp3', q=str(os.path.getmtime("static/segment.mp3"))),
        user_input="",
        progress=PROGRESS
    )


def _index_post(user_input):
    global CURRENT_CASE_INDEX, CASES, CURRENT_CASE, PROGRESS
    if "next" in request.form:  # Handle "Next Audio" button click
        CURRENT_CASE_INDEX += 1
        if CURRENT_CASE_INDEX >= len(CASES):
            CURRENT_CASE_INDEX = 0  # Loop back to the first case
        CURRENT_CASE = CASES[CURRENT_CASE_INDEX]
        review.prepare_audio_segment(CURRENT_CASE)
        progress = f"{CURRENT_CASE_INDEX + 1}/{TOTAL_CASES}"
        return render_template(
            "index.html",
            feedback=None,
            audio_file=url_for('static', filename='segment.mp3', q=str(os.path.getmtime("static/segment.mp3"))),
            user_input="",
            progress=progress
        )

        # Handle form submission (user's answer)
    user_answer = user_input.lower()
    correct_answer = CURRENT_CASE.get("answer", "").strip().lower()

    if user_answer == correct_answer:
        feedback = "<span style='color: green;'>Correct! 🎉</span>"
    else:
        feedback = _highlight_differences(user_answer, correct_answer)

    return render_template(
        "index.html",
        feedback=feedback,
        audio_file=url_for('static', filename='segment.mp3', q=str(os.path.getmtime("static/segment.mp3"))),
        user_input=user_input,
        progress=PROGRESS
    )


@app.route("/", methods=["GET", "POST"])
def index():
    global CURRENT_CASE_INDEX, CASES, CURRENT_CASE

    if request.method == "POST":
        user_input = request.form.get("answer", "").strip()  # Get user input
        return _index_post(user_input)

    return _initialize_index()


@app.route("/replay")
def replay_audio():
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
