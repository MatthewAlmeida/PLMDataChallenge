import argparse

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output, State

from plm_dash_components import PLMDashComponents 

# --------------------
# Handle a single command line argument to point the
# app code to the proper database host

parser = argparse.ArgumentParser(description="Launch PLM data challenge app.")
parser.add_argument(
    "-d",
    "--docker",
    action="store_true",
    help="If launching in a docker container, pass this flag to route to database."
)
args =parser.parse_args()
use_docker_host = args.docker

plmdc = PLMDashComponents(use_docker_host)

# --------------------

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    fluid=True,
    children=[
        html.H2(children='PatientsLikeMe Data Challenge'),
        html.Div(children='''
            Built with Python-Dash and Postgres, deployed via Docker-compose on AWS EC2.
        '''),
        html.Hr(),

        dbc.Row(
            [
                dbc.Col([plmdc.intro_card]),
                dbc.Col(
                    [
                        dcc.Graph(
                            id='example-graph',
                            figure={
                                'data': [
                                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                                ],
                                'layout': {'title': 'Dash Data Visualization'}
                            }
                        )
                    ]
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col([plmdc.condition_card]),
            ]
        )
    ],
    style={"margin":"auto"}
)

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True)
