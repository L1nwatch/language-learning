#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" Description
"""

__author__ = '__L1n__w@tch'

import pytest
from main import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_get(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"progress" in response.data


def test_index_show_practice_times(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Practice Times" in response.data
