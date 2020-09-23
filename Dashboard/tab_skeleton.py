import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


# Construct layout for the tab
def build_tab_skeleton(header_title):
    return [
        html.Div(
            id="graph-header",
            children=html.P(
                header_title
            ),
        ),
        html.Div(
            id="graph-main-content",
            children=[
                # Create div for graphs, populated later on
                html.Div(
                    id="value-setter-menu",
                    children=[
                        html.Div(children=html.Div(id='graphs'))
                    ],
                ),
            ],
        ),
    ]