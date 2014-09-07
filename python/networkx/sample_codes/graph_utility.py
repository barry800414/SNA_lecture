
import networkx as nx

def print_graph_info(g, show_data=False):
    print('--------------start---------------')
    print("Number of nodes: ", g.number_of_nodes(), "Nodes: ", g.nodes(data = show_data))
    print("Number of edges: ", g.number_of_edges(), "Edges: ", g.edges(data = show_data))
    print('---------------end----------------')
