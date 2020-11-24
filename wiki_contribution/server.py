# -*- coding: utf-8 -*-
import os
import hashlib

from dash import Dash
from flask import Flask, redirect, escape, request
from flask_caching import Cache


external_stylesheets = [
    "//stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css",
    "//fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i",
    "/static/css/base.css",
]

app = Dash(
    __name__,
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
