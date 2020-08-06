import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table

from dataclasses import (
    dataclass, InitVar
)

import plotly.graph_objects as go

from plmdata import Backend

@dataclass
class PLMDashComponents:
    use_docker_host: InitVar[bool]

    intro_card_title: str = "ALS Exploratory Data Analysis"

    # I know these numbers should come from the DB.

    intro_card_text_1: str = (
        "Four .csv files were provided: user_ALSFRS_score.csv, user_condition.csv, "
        "user_onset_date.csv, and user_symptom.csv. They each had a user_id field to "
        "join on, and the following row counts: alsfrs: 4409; condition: 626,914; "
        "onset: 229; symptom: 261,716." 
    )
    intro_card_text_2: str = (
        "They had the following unique user counts: alsfrs: 200; condition: 435,861; "
        "onset: 229; symptom: 35,912. However, these ids do not join perfectly; we see the "
        "following join results: alsfrs users in onset: 179; alsfrs users in condition: 197; "
        "alsfrs users in symptom: 16; onset users in condition: 225; onset users in symptom: 18"
    )

    condition_card_title: str = (
        "Distribution of Conditions of Users"
    )

    condition_card_text: str = (
        "Of the 200 users with time series data in alsfrs, 197 of them have conditions "
        "listed in the conditions table. These are overwhelmingly not ALS; for the "
        "purposes of the data challenge, we are assuming that the alsfrs table and "
        "onset table supersede the conditions table. Any user with records in alsfrs "
        "or onset is assumed to have ALS."
    )

    intro_card: dbc.Card = dbc.Card(
        [
            html.H4(intro_card_title, className="card-title"),
            html.P(intro_card_text_1, className="card-text"),
            html.P(intro_card_text_2, className="card-text")
        ], 
        body=True,
    )

    def __post_init__(self, use_docker_host):
        B = Backend(use_docker_host)

        condition_df = B.get_condition_card_data()

        self.condition_card = dbc.Card(
            [
                html.H4(self.condition_card_title, className="card-title"),
                html.P(self.condition_card_text),
                dash_table.DataTable(
                    id='condition_table',
                    columns=[{"name": i, "id": i} for i in condition_df.columns],
                    data=condition_df.to_dict('records'),
                    style_cell={'textAlign': 'left'},
                    style_as_list_view=True,
                )
            ], 
            body=True,
        )

        self.density_card = dbc.Card(
            [
                dcc.Graph(
                    
                )
            ]
        )