
import networkx as nx

def print_graph_info(g, show_data=False):
    print("Number of nodes: " + g.number_of_nodes())
    print("Nodes: " + g.nodes(data = show_data))
    print("Number of edges: " + g.number_of_edges())
    print("Edges: " + g.edges(data = show_data))

