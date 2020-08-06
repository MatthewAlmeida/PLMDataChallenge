import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output, State

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
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H4("ALS Data Analysis", className="card-title"),
                                        html.P(
                                            "This dashboard presents the results of our analysis"
                                            " of the users provided for the data challenge.",
                                            className="card-text"
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                ),
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
        )       
    ],
    style={"margin":"auto"}
)

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True)
