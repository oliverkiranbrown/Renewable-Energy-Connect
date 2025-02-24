# Import packages
from dash import Dash, html, dash_table
import pandas as pd

# Incorporate data
df = pd.read_csv('/Users/oliverbrown/Desktop/Oli/Renewable-Energy-Connect/cee-members.csv')

# create fake mock data from other file
from build_graph import create_graph

# Initialize the app
app = Dash()

# create the graph
graph_to_show = create_graph()

# App layout
app.layout = [
    html.Div(children='My First App with Data'),
    html.Div(children=html.Iframe(
        srcDoc=graph_to_show.generate_html(),
        width='800px',
        height='600px'
    ))
]

# Run the app
if __name__ == '__main__':
    app.run(debug=True)