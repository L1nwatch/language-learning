#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" Description
"""
from DataManager import DataManager
from applications.app import app
from utils.common import get_audio_files
from flask import render_template, request, redirect, url_for

__author__ = '__L1n__w@tch'


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        note_info = {
            "type": request.form.get("type"),
            "answer": request.form.get("answer"),
            "question": request.form.get("question"),
            "file": request.form.get("file"),
            "start_time": request.form.get("start_time"),
            "end_time": request.form.get("end_time"),
        }

        # Backend validation
        if note_info["type"] == "listening":
            # All fields are required for "listening"
            required_fields = ["type", "answer", "file", "start_time", "end_time"]
        elif note_info["type"] == "word":
            # Only "type" and "answer" are required for "word"
            required_fields = ["type", "answer"]
        elif note_info["type"] == "writing":
            # Only "type" and "answer" are required for "word"
            required_fields = ["type", "answer", "question"]
        else:
            return "Invalid type value. Please select 'listening'/'word'/'writing'.", 400

        for field in required_fields:
            if not note_info.get(field):
                return f"{field} is required for {note_info['type']} type.", 400

        # Insert into database
        try:
            db_handler = DataManager()
            success = db_handler.insert_new_row(note_info)
            if success:
                return redirect(url_for("add"))
        except Exception as e:
            return f"An error occurred: {e}"

    return render_template("add.html", files=get_audio_files())
