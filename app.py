# -*- coding: utf-8 -*-
from wiki_contribution.run import app, server

if __name__ == "__main__":
    app.run_server(debug=False, port=5000)