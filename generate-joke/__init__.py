import logging

import azure.functions as func
from textgenrnn import textgenrnn
import tempfile

import urllib.request
import os
import logging
import json


def write_http_response(status, body_dict):
    return_dict = {
        "status": status,
        "body": json.dumps(body_dict),
        "headers": {
            "Content-Type": "application/json"
        }
    }
    return json.dumps(return_dict)


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    tempFilePath = tempfile.gettempdir()
    jokesfile = os.path.join(tempFilePath, "jokes.hdf5")
    urllib.request.urlretrieve(
        "https://trickters.blob.core.windows.net/jokes/jokes.hdf5", jokesfile)
    textgen = textgenrnn(jokesfile)
    joke = textgen.generate(return_as_list=True)[0]
    logging.info(f"joke: {joke}")
    return write_http_response(
        200,
        {'joke': joke}
    )
