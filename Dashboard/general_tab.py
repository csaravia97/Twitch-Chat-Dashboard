import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
import graph_skeleton

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
import twitch_data


# construct tab layout for general tab
def tab_layout(streamers, chatDF, graph_format):

    # Embed graph within card
    def gen_graph_skeleton(graph_function, header):
        card = dbc.Card(
            [
                dbc.CardHeader(header),
                dbc.CardBody(graph_function(streamers, chatDF, graph_format), style={"padding": "0.5rem"}),
            ],
            style={"background-color": "LightGrey", "color": "black"}
        )
        return card

    return (
        html.Div(
            id = "general-tab-graphs",
            children = [
                dbc.Row(
                    [
                        dbc.Col(gen_graph_skeleton(question_mark_messages, 'Messages beginning with "?".'), lg=6, md=12),
                        dbc.Col(gen_graph_skeleton(streamer_mentions, "Number of times @'d."), lg=6, md=12)
                    ]
                ),
                dbc.Row(dbc.Col(gen_graph_skeleton(emote_ratio, "Emote Ratio = (Number of emotes / Message length)"), 
                                lg=8, md=12, className='graph-cols'), 
                        justify='center'),
            ]
        )
    )

# create graph for question mark data (get all messages that begin with '?')
def question_mark_messages(streamers, chatDF, graph_format):
    layout = graph_format['question-mark']['layout']
    data = chatDF.question_mark_count()[streamers] # only get data for currently selected streamers
    color = ['#5c16c5'] * len(streamers)
    extra_args = {'marker': {'color' : color }}
    graph_data = graph_skeleton.generate_graph_data('bar', data.index, data.values, 'question-mark', **extra_args)
    
    return(dcc.Graph(
        id='question-mark-graph',       
        animate=True,
        figure={
            'data': [graph_data],
            'layout' : layout
        }
    ))


# create graph for @streamer data (all chat messages directed towards the streamer)
def streamer_mentions(streamers, chatDF, graph_format):
    layout = graph_format['streamer-mentions']['layout']
    data = chatDF.streamer_mention_count()[streamers]
    color = ['#5c16c5'] * len(streamers)
    extra_args = {'marker': {'color' : color }}
    graph_data = graph_skeleton.generate_graph_data('bar', data.index, data.values, 'mentions', **extra_args)

    return(dcc.Graph(
        id='question-mark-graph',       
        animate=True,
        figure={
            'data': [graph_data],
            'layout' : layout
        }
    ))

# create graph for word-emote ratio (On average how much of a message is composed of emotes)
def emote_ratio(streamers, chatDF, graph_format):
    layout = graph_format['emote-ratio']['layout']
    data = chatDF.average_emote_ratio()[streamers]
    color = ['#5c16c5'] * len(streamers)
    extra_args = {'marker': {'color' : color }}
    graph_data = graph_skeleton.generate_graph_data('bar', data.index, data.values, 'emote-ratio', **extra_args)

    return(dcc.Graph(
        id='question-mark-graph',       
        animate=True,
        figure={
            'data': [graph_data],
            'layout' : layout
        }
    ))