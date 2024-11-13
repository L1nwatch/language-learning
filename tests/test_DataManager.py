#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" Description
"""

__author__ = '__L1n__w@tch'

from unittest import TestCase
from DataManager import DataManager

if __name__ == "__main__":
    pass


class TestDataManager(TestCase):
    def setUp(self) -> None:
        self.dm = DataManager()

    def test_add_case(self):
        # Arrange
        note_info = {
            "type": "listening",
            "answer": "This is the correct answer.",
            "file": "example.txt",
            "start_time": "00:00",
            "end_time": "15:00"
        }

        # Act: Insert the new row
        result = self.dm.insert_new_row(note_info)
        self.assertTrue(result, "Row insertion failed.")

        # Fetch the inserted row to verify it exists
        query = """
            SELECT * FROM ALLERROR 
            WHERE type = ? AND answer = ? AND file = ? AND start_time = ? AND end_time = ?
        """
        parameters = (
            note_info["type"],
            note_info["answer"],
            note_info["file"],
            note_info["start_time"],
            note_info["end_time"],
        )
        inserted_row = self.dm.execute(query, parameters).fetchone()

        self.assertIsNotNone(inserted_row, "Inserted row not found in the database.")

        # Clean up: Delete the row after test
        delete_query = "DELETE FROM ALLERROR WHERE id = ?"
        delete_parameters = (inserted_row[0],)
        self.dm.execute(delete_query, delete_parameters)

        # Verify the row was deleted
        verify_query = "SELECT * FROM ALLERROR WHERE id = ?"
        deleted_row = self.dm.execute(verify_query, delete_parameters).fetchone()
        self.assertIsNone(deleted_row, "Row deletion after test failed.")

    def test_load_cases(self):
        result = self.dm.load_cases()
        self.assertIsInstance(result, list)
        if len(result) > 0:
            self.assertIsInstance(result[0], dict)
            self.assertIn("file", result[0])
            self.assertIn("answer", result[0])
            self.assertIn("type", result[0])
            self.assertIn("start_time", result[0])
            self.assertIn("end_time", result[0])
