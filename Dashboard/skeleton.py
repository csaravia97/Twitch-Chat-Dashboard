import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html


def build_banner():
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.Div(
                id="banner-text",
                children=[
                    html.H3("Twitch Chat Statistics Dashboard"),
                    html.H5("Created By: Carlos Saravia"),
                ],
            ),
        ],
    )


def build_tabs(tab_names):
    tabs = []
    tabs.append(
        dbc.Tab(
            id="general-tab",
            label="GENERAL STATISTICS",
            tab_id="tab1",
            className="custom-tab",
        )
    )
    # Create a tab for each tab_name
    for tab_number, graph in enumerate(tab_names, 2):
        tabs.append(
            dbc.Tab(
                id=f"{graph}-tab",
                label=f"{graph}",
                tab_id=f"tab{tab_number}",
                className="custom-tab",
            )
        )
    # Append tabs array to tabs component and return 
    return html.Div(
        id="tabs",
        className="tabs",
        children=[
            dbc.Card([
                dbc.CardHeader(
                    dbc.Tabs(
                        id="app-tabs",
                        className="custom-tabs",
                        children=tabs,
                        active_tab='tab1',
                        card=True
                    ),
                    className="tab-card-header"
                )
            ])
        ],
    )
