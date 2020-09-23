import skeleton
import tab_skeleton
import graph_skeleton
import general_tab
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from twitch_data import TwitchData

import numpy as np
import pandas as pd
import json

data = TwitchData('../Data/')
df = data.chat_df
channels = df.channel.unique()

with open('./graph_formatting.json') as f:
  graph_format = json.load(f)

app = dash.Dash('streamer-dashboard', external_stylesheets=[dbc.themes.SUPERHERO])
app.config["suppress_callback_exceptions"] = True

def render_content_load():
    return (html.Div(children=html.P('tab1')))


app.layout = html.Div(
    id="big-app-container",
    children=[
        # build banner
        skeleton.build_banner(),
        html.Div(
            id="app-container",
            # Provided the tab names, build the tabs using skeleton provided in tab_skeleton (all except general)
            children=[
                html.Div(
                    id="streamer-select-menu",
                    children=[
                        html.Label(id="streamer-select-title", children="Select Streamers:"),
                        html.Br(),
                        # add each streamer to dropdown
                        dcc.Dropdown(
                            id="streamer-select-dropdown",
                            options=list(
                                {"label": s, "value": s} for s in channels
                            ),
                            value=[channels[1]],
                            multi=True
                        ),
                    ],
                ),
                dbc.Jumbotron([                
                skeleton.build_tabs(['MOST USED EMOTES', 'EMOTE TYPE BREAKDOWN','MOST ACTIVE PARTICIPANTS', 'MOST USED COMMANDS']),
                # Main app
                html.Div(id="app-content"),], className='content-jumbotron')
            ],
        ),
    ],
    
)

# Callback to render tab content using active_tab property of app-tabs 
@app.callback(
    Output(component_id='app-content', component_property='children'),
    [Input(component_id='app-tabs', component_property='active_tab')]
)

def render_tab_content(tab_switch):
    if tab_switch == 'tab1':
        return (html.Div(
             children=tab_skeleton.build_tab_skeleton(
                'General statistics calculated over all of the data.')
            )
        )

    elif tab_switch == 'tab2': 
        return (html.Div(
            children=tab_skeleton.build_tab_skeleton(
                'Most used emote per channel.')
            )
        )
    
    elif tab_switch == 'tab3':
        return (html.Div(
            children=tab_skeleton.build_tab_skeleton(
                'Breakdown of emote type usage. Note that Other Channel Emotes includes only emotes from channels that are available\
                    in the dropdown menu.')
            )
        )
        
    elif tab_switch == 'tab4': 
        return (html.Div(
            children=tab_skeleton.build_tab_skeleton(
                'Chat participation statistics per channel. With each bar graph signifying top 5 participants in chat.')
            )
        )
    elif tab_switch == 'tab5': 
        return (html.Div(
            children=tab_skeleton.build_tab_skeleton(
                'Top 3 most used chat commands per channel. ')
            )
        )

# Given currently selected dropdown option, current tab, and chatDF, generate graph for each selected option
@app.callback(
    Output(component_id='graphs', component_property='children'),
    [Input(component_id='streamer-select-dropdown', component_property='value'), 
     Input(component_id='app-tabs', component_property='active_tab')],
)

def update_graph(streamers, tab_switch):
    if tab_switch == 'tab1':
        return general_tab.tab_layout(streamers, data, graph_format['tab1'])
    return graph_skeleton.build_graphs(streamers, tab_switch, data, graph_format)


# Update graphs in general tab when dropdown updated (chains with callback above)
@app.callback(
    Output(component_id='general-tab-graphs', component_property='children'),
    [Input(component_id='graphs', component_property='children')],
    [State(component_id='streamer-select-dropdown', component_property='value'), 
    State(component_id='app-tabs', component_property='active_tab')]
)

def update_gen_tab_graphs(graphs, streamers, tab_switch):
    if tab_switch == 'tab1':
        return general_tab.tab_layout(streamers, data, graph_format['tab1'])
    return dash.no_update

if __name__ == '__main__':
    app.run_server(debug=True)