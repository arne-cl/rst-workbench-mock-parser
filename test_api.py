#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Author: Arne Neumann <nlpbox.programming@arne.cl>

"""Tests for the mock RST parser."""

from __future__ import print_function
import os
import pexpect
import pytest
import requests

from app import RS3_OUTPUT_TEMPLATE


@pytest.fixture(scope="session", autouse=True)
def start_api():
    """Starts the REST API in the background."""
    print("starting API...")
    child = pexpect.spawn('python app.py')
    yield child.expect('(?i)Running on http://0.0.0.0:5000/') # provide the fixture value
    print("stopping API...")
    child.close()

def post_input(input_text):
    """Posts a file to the REST API and converts between the given formats."""
    url = 'http://localhost:5000/parse'
    return requests.post(url, files={'input': input_text})

def test_rst_parser():
    """API generates rs3 file from plain text input"""
    input_string = 'foo'
    res = post_input(input_string)
    expected_output = RS3_OUTPUT_TEMPLATE.format(begin=input_string, end=input_string)

    assert res.content.decode('utf-8') == expected_output

def test_missing_input():
    """Calling the API with missing results in an error"""
    # no input file
    url = 'http://localhost:5000/parse'
    res = requests.post(url)
    assert res.status_code != 200
