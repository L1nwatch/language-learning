#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" Description
"""
from DataManager import DataManager
from applications.app import app
from utils.common import get_audio_path, get_audio_files
from werkzeug.utils import secure_filename
from AudioProvider import AudioProvider
from flask import render_template, request, redirect, url_for, jsonify, send_file

__author__ = '__L1n__w@tch'


@app.route("/preview_audio", methods=["POST"])
def preview_audio():
    data = request.json
    file_name = secure_filename(data.get("file"))
    start_time = data.get("start_time")
    end_time = data.get("end_time")

    if not file_name or not start_time or not end_time:
        return jsonify({"error": "Invalid parameters"}), 400

    try:
        ap = AudioProvider()
        ap.prepare_audio_segment(
            {"file": file_name, "type": "listening", "start_time": start_time, "end_time": end_time}
        )
        return jsonify({"audio_url": f"/preview_audio_path"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route(f"/preview_audio_path")
def serve_audio():
    return send_file(get_audio_path())


@app.route("/add", methods=["GET", "POST"])
def add():
    db_handler = DataManager()

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
            success = db_handler.insert_new_row(note_info)
            if success:
                return redirect(url_for("add"))
        except Exception as e:
            return f"An error occurred: {e}"

    default_file = db_handler.get_last_listening_file()
    return render_template("add.html", files=get_audio_files(), default_file=default_file)


# So if a photon is directed through a plane with two slits in ti and either slit is observed, it will not go through both slits. If it's unobserved, it will.
