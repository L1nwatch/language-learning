#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" Description
"""
import json
import os
import sqlite3

__author__ = '__L1n__w@tch'


class DataManager:
    def __init__(self):
        root_path = os.path.dirname(__file__)
        self.db_path = os.path.join(root_path, "data", "cases.db")
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()

    def _connect(self):
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()

    def _close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None

    def _create_table(self):
        self._connect()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS ALLERROR (
    id INTEGER PRIMARY KEY,
    type TEXT NOT NULL,
    answer TEXT,
    file TEXT,
    start_time TEXT,
    end_time TEXT,
    error_rate REAL,
    error_num INTEGER DEFAULT 0,
    practice_num INTEGER DEFAULT 0
    );
""")
        # try:
        #     self.cursor.execute("ALTER TABLE ALLERROR ADD COLUMN practice_num INTEGER DEFAULT 0;")
        # except sqlite3.OperationalError as e:
        #     if "duplicate column name" in str(e):
        #         print("Column 'error_rate' already exists.")
        #     else:
        #         raise e
        self.connection.commit()
        self._close()

    def _read_table(self):
        self._connect()
        # Enable dictionary-style access for rows
        self.connection.row_factory = sqlite3.Row
        # Create a fresh cursor after setting row_factory
        cursor = self.connection.cursor()

        # Use custom sorting to rank NULLs at the top
        result = cursor.execute("""
            SELECT * 
            FROM ALLERROR 
            ORDER BY 
                CASE WHEN error_rate IS NULL THEN 0 ELSE 1 END, 
                error_rate DESC;
        """)

        # Convert rows to dictionaries
        data = [dict(row) for row in result.fetchall()]
        self._close()
        return data

    def _update_table_from_json(self, json_path):
        self._connect()
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for each_data in data:
            if each_data["type"] == "listening":
                self.cursor.execute(
                    "INSERT INTO ALLERROR (type, answer, file, start_time, end_time) VALUES (?, ?, ?, ?, ?);",
                    (each_data["type"], each_data["answer"], each_data["file"], each_data["start_time"],
                     each_data["end_time"]))
            elif each_data["type"] == "word":
                self.cursor.execute("INSERT INTO ALLERROR (type, answer) VALUES (?, ?);",
                                    (each_data["type"], each_data["answer"]))
        self.connection.commit()
        self._close()

    def save_result(self, result, correct, feedback):
        update_error_rate_template = "UPDATE ALLERROR SET error_rate = error_num / practice_num WHERE id = ?;"
        self._connect()
        self.cursor.execute("UPDATE ALLERROR SET practice_num = practice_num + 1 WHERE id = ?;", (result["id"],))
        if not correct:
            self.cursor.execute("UPDATE ALLERROR SET error_num = error_num + 1 WHERE id = ?;", (result["id"],))
        self.cursor.execute(update_error_rate_template, (result["id"],))
        self.connection.commit()
        self._close()

    def load_cases(self) -> list:
        self._create_table()
        data = self._read_table()

        return data


if __name__ == "__main__":
    # dm = DataManager()
    # print(dm._update_table_from_json("data/cases.json"))
    pass
