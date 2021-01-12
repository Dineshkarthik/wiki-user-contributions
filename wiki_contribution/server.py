# -*- coding: utf-8 -*-
import os
import hashlib

import dash_bootstrap_components as dbc
from dash import Dash
from flask import Flask, redirect, escape, request
from flask_caching import Cache


external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    "//fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i",
    {
        "href": "https://use.fontawesome.com/releases/v5.8.1/css/all.css",
        "rel": "stylesheet",
        "integrity": "sha384-50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf",
        "crossorigin": "anonymous",
    },
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
