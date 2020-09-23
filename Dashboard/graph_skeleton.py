import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
import twitch_data

color = ['#5c16c5'] * 5

# Build a single graph
def build_graph(data, streamer, layout):
    return (
        html.Div(
            dbc.Card(
            dcc.Graph(
                id=streamer,       
                animate=True,
                figure={
                    'data': [data],
                    'layout' : {
                        **layout,
                        'title' : streamer + layout['title'] # overwrite layout title 
                    }
                }
            ), style={"background-color": "LightGrey", "padding": '10px', "color": "black"}
        ))
    )

# Build a graph for each streamer currently selected in the dropdown.
# Graph dependent on the current tab
def build_graphs(streamers, tab_switch, chatDF, graph_format):
    columns = []
    graph_info = graph_format[tab_switch]
    if tab_switch == 'tab2':
        graph_type = 'bar'
        data = chatDF.top_emotes_per_channel(5)
        extra_args = {'marker': {'color' : color }}
    
    elif tab_switch == 'tab3':
        graph_type = 'pie'
        data = chatDF.emote_type_breakdown()
        extra_args = {'hole': 0.5, 'pull':[0, 0, 0, 0, 0.2, 0.2, 0.2], 
            'marker': {'colors' : px.colors.cyclical.Twilight}
        }

    elif tab_switch == 'tab4':
        graph_type = 'bar'
        data = chatDF.top_chatters_per_channel(5)
        extra_args = {'marker': {'color' : color }}

    elif tab_switch == 'tab5':
        graph_type = 'bar'
        data = chatDF.top_commands_per_channel(3)
        extra_args = {'marker': {'color' : color }}

    for streamer in streamers:
        streamer_data = generate_graph_data(graph_type, data[streamer].index.values, data[streamer].values, streamer, **extra_args)
        columns.append(dbc.Col(build_graph(streamer_data, streamer, graph_info['layout']), sm=12, md=6, lg=4, className = 'graph-cols'))
    
    return (html.Div([dbc.Row(columns)]))


# Function to structure graph data into dictionary to pass into dcc.Graph
def generate_graph_data(graph_type, labels, values, name, **kwargs):
    if graph_type == 'bar':
        data = {'x': labels, 'y': values, 'type': 'bar', 'name': name}
    
    if graph_type == 'pie':
        data = {'labels': labels, 'values': values, 'type': 'pie', 'name': name}
    
    for key, value in kwargs.items():
        data[key] = value

    return data