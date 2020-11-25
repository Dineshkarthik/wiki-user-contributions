"""Index page of the application."""
from datetime import date, datetime, timedelta

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import requests
from dash.dependencies import Input, Output, State

from .server import app, server, cache

LOGO = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Wikimedia-logo_black.svg/45px-Wikimedia-logo_black.svg.png"
S = requests.Session()

app.layout = html.Div(
    children=[
        dbc.Navbar(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Img(src=LOGO, height="30px"),
                                dbc.NavbarBrand(
                                    "Wiki User Contributions", className="ml-2"
                                ),
                            ]
                        ),
                    ],
                    align="left",
                    no_gutters=True,
                ),
            ],
            color="#119dff",
            dark=True,
        ),
        html.Div(
            className="bordered-inner-div",
            children=[
                dbc.Alert(
                    "Please fill out all the required fields (*)",
                    id="missing-params-alert",
                    dismissable=True,
                    is_open=False,
                ),
                html.Div(
                    className="form-group",
                    children=[
                        html.Div(
                            className="form-group",
                            children=[
                                dbc.Label("Language*:"),
                                html.Div(
                                    className="form-group",
                                    children=[
                                        dbc.Input(
                                            id="language",
                                            type="text",
                                            placeholder="Ex: en, ta",
                                            style={
                                                "width": "51.5%",
                                                "marginBottom": "3%",
                                            },
                                        )
                                    ],
                                ),
                            ],
                        ),
                        html.Div(
                            className="form-group",
                            children=[
                                dbc.Label("Wikisite*:"),
                                html.Div(
                                    className="form-group",
                                    children=[
                                        dbc.Input(
                                            id="wikisite",
                                            type="text",
                                            placeholder="Ex: wikisource",
                                            style={
                                                "width": "51.5%",
                                                "marginBottom": "3%",
                                            },
                                        )
                                    ],
                                ),
                            ],
                        ),
                        html.Div(
                            className="form-group",
                            children=[
                                dbc.Label("Username*:"),
                                html.Div(
                                    className="form-group",
                                    children=[
                                        dbc.Input(
                                            id="username",
                                            type="text",
                                            placeholder="your wikimedia username",
                                            style={
                                                "width": "51.5%",
                                                "marginBottom": "3%",
                                            },
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
                        "marginTop": "10%",
                        "marginBottom": "2%",
                    },
                ),
                dbc.Alert(
                    [
                        html.H4("No Data!", className="alert-heading"),
                        html.Hr(),
                        html.P(
                            "There is no user contribution data available for the given time-period.",
                            className="mb-0",
                        ),
                    ],
                    id="no-data-alert",
                    dismissable=True,
                    is_open=False,
                    color="info",
                ),
            ],
            style={
                "padding": "1%",
                "overflow": "hidden",
            },
        ),
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


@cache.memoize(timeout=120)
def get_usercontrib_details(
    language, wikisite, username, start_date, end_date
):
    URL = f"https://{language}.{wikisite}.org/w/api.php"

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


@cache.memoize(timeout=120)
@app.callback(
    [
        Output("report-table", "data"),
        Output("report-table", "columns"),
        Output("report-table-div", "style"),
        Output("missing-params-alert", "is_open"),
        Output("no-data-alert", "is_open"),
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
    results: list = []
    columns: list = []
    style: dict = {"display": "none"}
    alert: bool = False
    no_data_alert: bool = False
    if gen_report:
        if all([language, wikisite, username, start_date, end_date]):
            results = get_usercontrib_details(
                language, wikisite, username, start_date, end_date
            )
            if results:
                columns = [{"name": i, "id": i} for i in results[0].keys()]
                style = {"display": "block", "margin": "3%"}
            else:
                no_data_alert = True
        else:
            alert = True
    return [results, columns, style, alert, no_data_alert]


@app.callback(
    [
        Output("username", "invalid"),
        Output("language", "invalid"),
        Output("wikisite", "invalid"),
    ],
    [Input("generate-report", "n_clicks")],
    [
        State("username", "value"),
        State("language", "value"),
        State("wikisite", "value"),
    ],
)
def validate_inputs(
    gen_report,
    username,
    language,
    wikisite,
):
    if gen_report:
        return [not bool(username), not bool(language), not bool(wikisite)]
    return [False, False, False]


if __name__ == "__main__":
    app.run_server(debug=False, threaded=True, port=5000)
