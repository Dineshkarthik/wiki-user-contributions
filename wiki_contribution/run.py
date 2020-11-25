"""Index page of the application."""
from datetime import date, datetime, timedelta

import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import requests
from dash.dependencies import Input, Output, State

from .server import app, server, cache


app.layout = html.Div(
    children=[
        html.Nav(
            className="navbar navbar-expand-lg py-md-3 navbar-light bg-light",
            children=[
                html.Div(
                    [
                        html.Strong(
                            "Wiki User Contribution", className="navbar-header"
                        )
                    ]
                ),
            ],
        ),
        html.Div(
            className="bordered-inner-div",
            children=[
                html.Div(
                    className="form-group",
                    children=[
                        html.Div(
                            className="form-group",
                            children=[
                                html.Label("Language:"),
                                html.Div(
                                    className="form-group",
                                    children=[
                                        dcc.Input(
                                            id="language",
                                            type="text",
                                            placeholder="Ex: en, ta",
                                            style={
                                                "width": "51.5%",
                                                "marginBottom": "3%",
                                            },
                                            required="REQUIRED",
                                        )
                                    ],
                                ),
                            ],
                        ),
                        html.Div(
                            className="form-group",
                            children=[
                                html.Label("Wikisite:"),
                                html.Div(
                                    className="form-group",
                                    children=[
                                        dcc.Input(
                                            id="wikisite",
                                            type="text",
                                            placeholder="Ex: wikisource",
                                            style={
                                                "width": "51.5%",
                                                "marginBottom": "3%",
                                            },
                                            required="REQUIRED",
                                        )
                                    ],
                                ),
                            ],
                        ),
                        html.Div(
                            className="form-group",
                            children=[
                                html.Label("Username:"),
                                html.Div(
                                    className="form-group",
                                    children=[
                                        dcc.Input(
                                            id="username",
                                            type="text",
                                            placeholder="your wikimedia username",
                                            style={
                                                "width": "51.5%",
                                                "marginBottom": "3%",
                                            },
                                            required="REQUIRED",
                                        )
                                    ],
                                ),
                            ],
                        ),
                    ],
                    style={
                        "float": "left",
                        "width": "40%",
                        "marginBottom": "3%",
                    },
                ),
                html.Div(
                    className="form-group",
                    id="date-range-div",
                    children=[
                        html.Div([html.Label("Date range: YYYY-MM-DD")]),
                        html.Div(
                            [
                                dcc.DatePickerRange(
                                    id="date-picker-range",
                                    min_date_allowed=date(2001, 1, 15),
                                    max_date_allowed=date.today(),
                                    display_format="YYYY-MM-DD",
                                    start_date=date.today()
                                    - timedelta(days=7),
                                    end_date=date.today(),
                                )
                            ],
                            style={"width": "100%"},
                        ),
                    ],
                    style={"padding": "1%"},
                ),
                html.Button(
                    "Generate Report",
                    id="generate-report",
                    className="submit-button",
                    type="submit",
                    value="form",
                    style={
                        "marginTop": "5%",
                        "marginBottom": "5%",
                    },
                ),
            ],
            style={
                "padding": "1%",
                "overflow": "hidden",
            },
        ),
        html.Div(id="out-all-types"),
        html.Div(
            id="report-table-div",
            children=[
                dt.DataTable(
                    id="report-table",
                    data=[{}],
                    columns=[],
                    style_cell={
                        "textAlign": "center",
                        "fontSize": "14px",
                        "padding": "5px",
                    },
                    style_data_conditional=[
                        {
                            "if": {"row_index": "odd"},
                            "backgroundColor": "rgb(248, 248, 248)",
                        }
                    ],
                    style_header={
                        "backgroundColor": "rgb(230, 230, 230)",
                        "fontWeight": "bold",
                        "textAlign": "center",
                    },
                    sort_action="native",
                    sort_mode="multi",
                    page_action="native",
                    page_current=0,
                    page_size=20,
                    export_columns="all",
                    export_format="csv",
                    export_headers="names",
                )
            ],
            style={"display": "none", "margin": "3%"},
        ),
    ]
)


S = requests.Session()


@cache.memoize(timeout=1200)
def get_usercontrib_details(
    language, wikisite, username, start_date, end_date
):
    URL = "https://" + language + "." + wikisite + ".org/w/api.php"

    PARAMS = {
        "uclimit": 500,
        "action": "query",
        "format": "json",
        "list": "usercontribs",
        "ucuser": username,
        "ucstart": start_date + " 00:00:00",
        "ucend": end_date + " 23:59:59",
        "ucdir": "newer",
        "ucprop": "title|sizediff|size|timestamp",
    }

    csv_content = []

    while True:

        R = S.get(url=URL, params=PARAMS)
        DATA = R.json()
        USERCONTRIBS = DATA["query"]["usercontribs"]
        for uc in USERCONTRIBS:
            csv_content.append(
                {key: uc[key] for key in PARAMS["ucprop"].split("|")}
            )

        if "continue" in DATA:
            PARAMS["uccontinue"] = DATA["continue"]["uccontinue"]
            PARAMS["continue"] = DATA["continue"]["continue"]
            USERCONTRIBS = DATA["query"]["usercontribs"]
            for uc in USERCONTRIBS:
                csv_content.append(
                    {key: uc[key] for key in PARAMS["ucprop"].split("|")}
                )
        else:
            break
    return csv_content


@cache.memoize(timeout=1200)
@app.callback(
    [
        Output("report-table", "data"),
        Output("report-table", "columns"),
        Output("report-table-div", "style"),
    ],
    [Input("generate-report", "n_clicks")],
    [
        State("date-picker-range", "start_date"),
        State("date-picker-range", "end_date"),
        State("username", "value"),
        State("language", "value"),
        State("wikisite", "value"),
    ],
)
def generate_report(
    gen_report,
    start_date,
    end_date,
    username,
    language,
    wikisite,
):
    if gen_report:
        results = get_usercontrib_details(
            language, wikisite, username, start_date, end_date
        )
        columns = []
        if results:
            columns = [{"name": i, "id": i} for i in results[0].keys()]
        return [
            results,
            columns,
            {"display": "block", "margin": "3%"},
        ]
    return [[], [], {"display": "none"}]


if __name__ == "__main__":
    app.run_server(debug=False, threaded=True, port=5000)