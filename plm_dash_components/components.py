"""
This file contains a dataclass that holds all the
dashboard components, which helps to keep app.py
from being a complete mess. This is where we 
instantiate the Backend object that we use to reach 
the database and call the wrapper functions for the
dataframes provided by that Backend.
"""

import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table

from dataclasses import (
    dataclass, InitVar
)

import plotly.graph_objects as go
import plotly.express as px

from plmdata import Backend

@dataclass
class PLMDashComponents:
    use_docker_host: InitVar[bool]

    intro_card_title: str = "ALS Exploratory Data Analysis"

    # I know these numbers should come from the DB...

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
        "alsfrs users in symptom: 16; onset users in condition: 225; onset users in symptom: 18. "
        "See below for a breakdown of the condition entries of those users in alsfrs."
    )

    intro_card_text_3: str = (
        "After looking at the data series in the alsfrs table by user and in groups of users, "
        "it appears that apart from a few exceptions, sadly, the score progressions for each user conform "
        "very closely to their trend line in a steady negative decline. The rates of decline, however, "
        "vary dramatically - in terms of predicting future outcomes, it seems to be more effective "
        "to use the trend line established by the first few reports of a given user to predict that user's "
        "experience than a model made up of a sample of many users."
    )

    # The intro card doesn't need to hit the DB, so it doesn't need to 
    # be in __post_init__.

    intro_card: dbc.Card = dbc.Card(
        [
            html.H4(intro_card_title, className="card-title"),
            html.P(intro_card_text_1, className="card-text"),
            html.P(intro_card_text_2, className="card-text"),
            html.P(intro_card_text_3, className="card-text"),
        ], 
        body=True,
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

    trend_card_title: str = "Selected Single-user Score Progressions with Trend Lines"

    trend_card_text: str = (
        "Here we present four selected examples of single-user alsfrs score progressions "
        "with trend lines. Three of them exhibit very good fit; the fourth trend line is "
        "inaccurate, but it appears this is an unusual case, where the user reported three "
        "instances of high function almost twenty years before his or her disease began "
        "progressing rapidly."
    )

    def _build_trend_card_figures(self, user_ids):
        figures = []

        for uid in user_ids:
            user_df = self.B.get_alsfrs_series_by_user_id(uid)
            figures.append(
                px.scatter(
                    user_df, x="report_date", y="score", trendline="ols",
                    labels={"report_date":"Report Date", "score": "ALS FRS score"},
                    title=f"User {uid}"
                )
            )
        
        return figures

    def __post_init__(self, use_docker_host):
        
        # Initialize backend
        self.B = Backend(use_docker_host)

        # --------------------
        # Condition card
        #
        # Get source data from database
        condition_df = self.B.get_condition_card_data()

        # Build the condition card
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

        # --------------------
        # Single-User trendline cards
        # 
        # Selected user IDs
        # 2768 2514 1841 7326

        # Ask the Backend for the data
        trend_figures = self._build_trend_card_figures(
            [2768, 2514, 1841, 7326]
        )
        # Assemble card layout
        self.trend_card = dbc.Card(
            [
                html.H4(self.trend_card_title),
                html.P(self.trend_card_text),
                dbc.Row(
                    [
                        dbc.Col([dcc.Graph(figure=trend_figures[0])]),
                        dbc.Col([dcc.Graph(figure=trend_figures[1])]),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col([dcc.Graph(figure=trend_figures[2])]),
                        dbc.Col([dcc.Graph(figure=trend_figures[3])]),
                    ]
                ),
            ],
            body=True
        )