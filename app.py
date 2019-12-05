#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Arne Neumann <nlpbox.programming@arne.cl>

"""This module contains a REST API for a mock RST parser.
"""

import io
import tempfile
from pathlib import Path

from flask import Flask, request, send_file
from flask_restplus import Resource, Api
import werkzeug


app = Flask(__name__)  # create a Flask app
api = Api(app)  # create a Flask-RESTPlus API

RS3_OUTPUT_TEMPLATE = """
<rst>
  <header>
    <relations>
      <rel name="elaboration" type="rst" />
    </relations>
  </header>
  <body>
    <segment id="1">{begin}</segment>
    <segment id="2" parent="1" relname="elaboration">... {end}</segment>
  </body>
</rst>
"""


def get_inputfile_as_string(request):
    """Returns the input file from the POST request as a string,
    no matter if it was sent as a file named 'input' or a form field
    named 'input'.

    Returns None if the POST request does not have an 'input' file.
    """
    if 'input' in request.files:
        input_bytes = request.files['input'].read()
        return str(input_bytes, 'utf-8')
    elif 'input' in request.form:
        return request.form['input']


def cors_response(response, status=200):
    """Returns the given response with CORS='*' and the given status code."""
    response.status_code = status
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@api.route('/parse')
class MockRSTParser(Resource):
    def post(self):
        """Convert an input file (plain text) into a fake RST analysis as an rs3 file.

        Usage example:

            curl -XPOST "http://localhost:5000/parse" -F input=@source.txt
        """      
        input_string = get_inputfile_as_string(request)
        if input_string is None:
            res = jsonify(
                error=("Please upload a file using the key "
                       "'input' or the form field 'input'. "
                       "Used file keys: {}. Used form fields: {}").format(request.files.keys(), request.form.keys()))
            return cors_response(res, 500)

        with tempfile.NamedTemporaryFile() as temp_outputfile:
            output_string = RS3_OUTPUT_TEMPLATE.format(begin=input_string[:20], end=input_string[-20:])
            temp_outputfile.write(output_string.encode())
            temp_outputfile.flush()

            res = send_file(temp_outputfile.name, as_attachment=True,
                            attachment_filename='output.rs3')

        return cors_response(res)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
