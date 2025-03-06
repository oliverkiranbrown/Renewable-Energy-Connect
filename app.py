# install needed libraries
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback
import pandas as pd

# create fake mock data from other file
from build_graph import create_graph
from create_toy_data import *
from insert_click import *

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Initialize the app
app = Dash()

# create the graph and insert the js snippet inside the html
graph_to_show = insert_click_event_js(create_graph())

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1(children = 'Renewable Energy Connect', style={"textAlign": "center"}),
    dcc.Tabs(id="tabs-example-graph", value='tab-1-example-graph', children=[
        dcc.Tab(label='Graph View', value='tab-1-example-graph'),
        dcc.Tab(label='Table View', value='tab-2-example-graph'),
    ]),
    html.Div(id='tabs-content-example-graph')
])

# backend
@callback(Output('tabs-content-example-graph', 'children'),
              Input('tabs-example-graph', 'value'))
def render_content(tab):
    if tab == 'tab-1-example-graph':
        return html.Div([
            html.Div(children=html.Iframe(
                id='graph_frame',
                srcDoc=graph_to_show,
                width='80%',
                height='600px')   
            ), 
            # store clicked node data (to avoid writing to a file)
            dcc.Store(id='clicked-node-store'),
            html.Div([
                html.H2("Details Section", style={"textAlign": "center"}),
                html.P("This section can be used to display additional details."),
                dcc.Textarea(
                    placeholder="Enter comments here...",
                    style={"width": "20%", "height": "100px"}
                ),
                html.Div(id='node-output', value='')
            ])
        ])
    elif tab == 'tab-2-example-graph':
        return html.Div([
            dash_table.DataTable(
                data = df.to_dict('records'), 
                columns = [{"name": i, "id": i} for i in df.columns],
                filter_action = "native",
                sort_action = "native" 
            )
        ]
    )

# Dash Callback to Update Clicked Node Display
@app.callback(
    Output("node-output", "children"),
    Input("clicked-node-store", "data")
)
def update_clicked_node(node):
    if node:
        return f"Node {node} clicked!"
    return "Click a node to see details."


if __name__ == '__main__':
    app.run(debug=True)