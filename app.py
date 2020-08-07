"""
This is the main entrypoint for the dashboard. This
file is pretty lean; most of the important building 
of the dashboards' components happens in the
PLMDashComponents class. 
"""

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

# Layout of the dashboard happens here. This simply lays out the
# cards defined in the PLMDashComponents class into rows and 
# columns in the bootstrap method.
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
                dbc.Col(
                    [
                        plmdc.intro_card,
                        plmdc.condition_card

                    ]
                ),
                dbc.Col(
                    [
                        plmdc.trend_card
                    ]
                )
            ]
        ),
    ],
    style={"margin":"auto"}
)

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True)
