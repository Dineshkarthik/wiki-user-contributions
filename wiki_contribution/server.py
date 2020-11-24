# -*- coding: utf-8 -*-
import os
import hashlib

from dash import Dash
from flask import Flask, redirect, escape, request
from flask_caching import Cache


external_stylesheets = [
    "//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css",
    "//fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i",
    "/static/css/base.css",
]

external_scripts = [
    "//code.jquery.com/jquery-3.2.1.slim.min.js",
    "//cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js",
    "//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js",
]

app = Dash(
    __name__,
    external_scripts=external_scripts,
    external_stylesheets=external_stylesheets,
    update_title="Loading...",
)
server = app.server
server.secret_key = hashlib.sha1(os.urandom(128)).hexdigest()

app.title = "Wiki User Contribution"
app.config.suppress_callback_exceptions = True
app.scripts.config.serve_locally = False

cache = Cache(
    app.server, config={"CACHE_TYPE": "filesystem", "CACHE_DIR": "cache"}
)


# @app.server.route("/static/<path:path>")
# def static_file(path):
#     """Funciton that returns static files css/js."""
#     static_folder = os.path.join(os.getcwd(), "static")
#     return send_from_directory(static_folder, path)
