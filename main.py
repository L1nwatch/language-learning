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

# Flask App Initialization
app = Flask(__name__)
review = Review()

# Load cases
with open("data/cases.json", "r") as f:
    cases = json.load(f)

# Global variables
current_case_index = -1  # Start without any active case
current_case = None  # Active case


@app.route("/", methods=["GET", "POST"])
def index():
    global current_case_index, cases, current_case

    user_input = ""  # Initialize user input variable
    total_cases = len(cases)  # Total number of audio cases
    progress = f"{current_case_index + 1}/{total_cases}" if current_case_index >= 0 else "0/0"

    if request.method == "POST":
        user_input = request.form.get("answer", "").strip()  # Get user input

        if "next" in request.form:  # Handle "Next Audio" button click
            current_case_index += 1
            if current_case_index >= len(cases):
                current_case_index = 0  # Loop back to the first case
            current_case = cases[current_case_index]
            review.prepare_audio_segment(current_case)
            progress = f"{current_case_index + 1}/{total_cases}"
            return render_template(
                "index.html",
                feedback=None,
                audio_file=url_for('static', filename='segment.mp3', q=str(os.path.getmtime("static/segment.mp3"))),
                user_input="",
                progress=progress
            )

        # Handle form submission (user's answer)
        user_answer = user_input.lower()
        correct_answer = current_case.get("answer", "").strip().lower()

        if user_answer == correct_answer:
            feedback = "<span style='color: green;'>Correct! 🎉</span>"
        else:
            feedback = review.highlight_differences(user_answer, correct_answer)

        return render_template(
            "index.html",
            feedback=feedback,
            audio_file=url_for('static', filename='segment.mp3', q=str(os.path.getmtime("static/segment.mp3"))),
            user_input=user_input,
            progress=progress
        )

    # Load the first listening case if no case is active
    if current_case_index == -1:
        current_case_index = 0
        current_case = cases[current_case_index]
        review.prepare_audio_segment(current_case)
        progress = f"{current_case_index + 1}/{total_cases}"

    return render_template(
        "index.html",
        feedback=None,
        audio_file=url_for('static', filename='segment.mp3', q=str(os.path.getmtime("static/segment.mp3"))),
        user_input="",
        progress=progress
    )


@app.route("/replay")
def replay_audio():
    # Replay the audio file
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
