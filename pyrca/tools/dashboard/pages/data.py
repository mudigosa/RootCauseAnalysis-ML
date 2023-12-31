#
# Copyright (c) 2023 salesforce.com, inc.
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# For full license text, see the LICENSE file in the repo root or https://opensource.org/licenses/BSD-3-Clause#
from dash import dcc
from dash import html, dash_table
from .utils import create_modal, create_emtpy_figure
from ..settings import *


def create_stats_table(data_stats=None):
    if data_stats is None or len(data_stats) == 0:
        data = [{"Stats": "", "Value": ""}]
    else:
        data = [{"Stats": key, "Value": value} for key, value in data_stats["@global"].items()]

    table = dash_table.DataTable(
        id="data-stats",
        data=data,
        columns=[{"id": "Stats", "name": "Stats"}, {"id": "Value", "name": "Value"}],
        editable=False,
        style_header_conditional=[{"textAlign": "center"}],
        style_cell_conditional=[{"textAlign": "center"}],
        style_header=dict(backgroundColor=TABLE_HEADER_COLOR),
        style_data=dict(backgroundColor=TABLE_DATA_COLOR),
    )
    return table


def create_metric_stats_table(metric_stats=None, column=None):
    if metric_stats is None or len(metric_stats) == 0 or column not in metric_stats:
        data = [{"Stats": "", "Value": ""}]
    else:
        data = [{"Stats": key, "Value": value} for key, value in metric_stats[column].items()]

    table = dash_table.DataTable(
        id="metric-stats",
        data=data,
        columns=[{"id": "Stats", "name": "Stats"}, {"id": "Value", "name": "Value"}],
        editable=False,
        style_header_conditional=[{"textAlign": "center"}],
        style_cell_conditional=[{"textAlign": "center"}],
        style_header=dict(backgroundColor=TABLE_HEADER_COLOR),
        style_data=dict(backgroundColor=TABLE_DATA_COLOR),
    )
    return table


def create_control_panel() -> html.Div:
    return html.Div(
        id="control-card",
        children=[
            html.Br(),
            html.P(id="label", children="Upload Time Series Data File"),
            dcc.Upload(
                id="upload-data",
                children=html.Div(
                    children=[
                        html.Img(src="../assets/upload.svg"),
                        html.Div(id="select-a-file"),
                    ]
                ),
                style={
                    "height": "50px",
                    "lineHeight": "50px",
                    "borderWidth": "1px",
                    "borderStyle": "dashed",
                    "borderRadius": "5px",
                    "textAlign": "center",
                    "margin": "5px",
                },
                multiple=True,
            ),
            html.Br(),
            html.P("Select Data File"),
            html.Div(
                id="select-file-parent", children=[dcc.Dropdown(id="select-file", options=[], style={"width": "100%"})]
            ),
            html.Br(),
            html.P("Overall Stats"),
            html.Div(
                id="data-stats-table",
                children=[create_metric_stats_table()],
            ),
            html.Br(),
            html.P("Metric/Variable Stats"),
            html.Div(
                id="select-column-parent",
                children=[dcc.Dropdown(id="select-column", options=[], style={"width": "100%"})],
            ),
            html.Div(
                id="metric-stats-table",
                children=[create_stats_table()],
            ),
            html.Br(),
            html.Div(children=[html.Button(id="data-btn", children="Load", n_clicks=0)], style={"textAlign": "center"}),
            html.Br(),
            html.P("Estimate Threshold"),
            html.Label("Metric"),
            html.Div(
                id="select-thres-column-parent",
                children=[dcc.Dropdown(id="select-thres-column", options=[], style={"width": "100%"})],
            ),
            html.Label("Sigma"),
            html.Div(
                id="sigma_input",
                children=[
                    dcc.Input(id="sigma", type="number", placeholder="Sigma value", value=4, style={"width": "100%"})
                ],
            ),
            html.Br(),
            html.Div(
                children=[html.Button(id="thres-btn", children="Estimate", n_clicks=0)], style={"textAlign": "center"}
            ),
            html.Br(),
            html.P("Manual Threshold"),
            html.Label("Metric"),
            html.Div(
                id="select-manual-column-parent",
                children=[dcc.Dropdown(id="select-manual-column", options=[], style={"width": "100%"})],
            ),
            html.Label("Lower"),
            html.Div(
                id="lower_input",
                children=[
                    dcc.Input(id="lower_bound", type="number", placeholder="Lower bound", style={"width": "100%"})
                ],
            ),
            html.Label("Upper"),
            html.Div(
                id="upper_input",
                children=[
                    dcc.Input(id="upper_bound", type="number", placeholder="Upper bound", style={"width": "100%"})
                ],
            ),
            html.Br(),
            html.Div(
                children=[html.Button(id="manual-btn", children="Test", n_clicks=0)], style={"textAlign": "center"}
            ),
            create_modal(
                modal_id="data-exception-modal",
                header="An Exception Occurred",
                content="An exception occurred. Please click OK to continue.",
                content_id="data-exception-modal-content",
                button_id="data-exception-modal-close",
            ),
            create_modal(
                modal_id="data-download-exception-modal",
                header="An Exception Occurred",
                content="An exception occurred. Please click OK to continue.",
                content_id="data-download-exception-modal-content",
                button_id="data-download-exception-modal-close",
            ),
        ],
    )


def create_right_column() -> html.Div:
    return html.Div(
        id="right-column-data",
        children=[
            html.Div(
                id="result_table_card",
                children=[
                    html.B("Time Series Plots"),
                    html.Hr(),
                    html.Div(id="data-plots", children=[create_emtpy_figure()]),
                ],
            ),
            html.Div(
                id="result_table_card", children=[html.B("Time Series Samples"), html.Hr(), html.Div(id="data-table")]
            ),
        ],
    )


def create_data_layout() -> html.Div:
    return html.Div(
        id="data_views",
        children=[
            # Left column
            html.Div(
                id="left-column-data",
                className="three columns",
                children=[create_control_panel()],
            ),
            # Right column
            html.Div(className="nine columns", children=create_right_column()),
        ],
    )
