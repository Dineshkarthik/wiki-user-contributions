# -*- coding: utf-8 -*-
import os
import hashlib

import dash_bootstrap_components as dbc
from dash import Dash
from flask import Flask, redirect, escape, request
from flask_caching import Cache


external_stylesheets = [
    "//tools-static.wmflabs.org/cdnjs/ajax/libs/bootstrap-v4-rtl/4.5.2-1/css/bootstrap.min.css",
    "//tools-static.wmflabs.org/fontcdn/css?family=Product+Sans:400,400i,700,700i",
    "//tools-static.wmflabs.org/cdnjs/ajax/libs/font-awesome/5.15.1/css/all.min.css",
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
app.scripts.config.serve_locally = True

cache = Cache(
    app.server, config={"CACHE_TYPE": "filesystem", "CACHE_DIR": "cache"}
)
