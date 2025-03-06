import numpy as np
import networkx as nx

from pyvis import network as net

# run the script to create the df objects required
from create_toy_data import *

def create_graph():
    G = nx.DiGraph()

    # add the project stages to the graph
    G.add_nodes_from(project_stages_nodes)

    # add the directed edges that link the project stages together
    for i in range(len(project_stages)-1):
        G.add_edge(project_stages[i], 
                project_stages[i+1], 
                color = 'black')#,
                #width = 100)

    # add the different actors to the graph
    G.add_nodes_from(actor_nodes)

    # add the edges from the stages to the actors
    for i in range(len(df)):
        G.add_edge(df['name'][i], df['primary_project_stage'][i])
        if df['secondary_project_stage'][i] != 'NA':
            G.add_edge(df['name'][i], df['secondary_project_stage'][i])

    # create PyVis object and convert NetworkX object to PyVis Format
    graph_to_show = net.Network(height='800px',
                                directed = True,
                                cdn_resources='in_line',
                                select_menu=True,
                                filter_menu=True)

    graph_to_show.from_nx(G)

    # make the key nodes bigger
    for n in graph_to_show.nodes:
        if n['color'] == 'DarkSalmon':
            n['font'] = {'size': 50}

    for e in graph_to_show.edges:
        # hacky fix to avoid accessing a dictionary item that doesn't exist
        if len(e) > 4:
            if (e['color'] == 'black'):
                e['width'] = 10
                e['arrowStrikethrough'] = False                

    return graph_to_show