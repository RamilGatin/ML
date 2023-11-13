import sys

import networkx as nx
import matplotlib.pyplot as plt
import random

def print_graph(graph, edges_with_value):
    print(graph)
    pos = nx.circular_layout(graph)
    nx.draw(graph, pos, with_labels=True)
    nx.draw_networkx_edge_labels(
        graph,
        pos,
        edge_labels=edges_with_value)
    plt.show()

def return_min_edge(edges_with_value, added_nodes):
    d_min = sys.maxsize
    edge_to_return = None
    for edge in edges_with_value:
        if edges_with_value[edge] <= d_min:
            if edge[0] in added_nodes and edge[1] in added_nodes:
                continue
            if len(added_nodes) == 0:
                d_min = edges_with_value[edge]
                edge_to_return = edge
            elif edge[0] in added_nodes or edge[1] in added_nodes:
                d_min = edges_with_value[edge]
                edge_to_return = edge
    return edge_to_return


def get_shortest_path(edges_with_value):
    edges_copy = edges_with_value.copy()
    shortest_path_with_value = {}
    nodes = []
    for edge in edges_copy:
        if edge[0] not in nodes:
            nodes.append(edge[0])
        if edge[1] not in nodes:
            nodes.append(edge[1])

    added_nodes = []
    while len(nodes) != len(added_nodes):
        edge_to_add = return_min_edge(edges_copy, added_nodes)
        val = edges_copy[edge_to_add]
        del edges_copy[edge_to_add]
        if edge_to_add[0] not in added_nodes:
            added_nodes.append(edge_to_add[0])
        if edge_to_add[1] not in added_nodes:
            added_nodes.append(edge_to_add[1])
        shortest_path_with_value[(edge_to_add[0], edge_to_add[1])] = val
    return shortest_path_with_value

def return_max_edge(edges_with_value):
    d_max = -1
    edge_to_return = None
    for edge in edges_with_value:
        if edges_with_value[edge] >= d_max:
            d_max = edges_with_value[edge]
            edge_to_return = edge
    return edge_to_return

def divide_on_clusters(short_path_edges_with_value, nodes, amount_of_clusters):
    already_existed_clusters = len(nodes) - len(short_path_edges_with_value)
    if already_existed_clusters >= amount_of_clusters:
        return
    edges_copy = short_path_edges_with_value.copy()
    for i in range(amount_of_clusters - already_existed_clusters):
        edge_to_remove = return_max_edge(edges_copy)
        if edge_to_remove == None:
            break
        del edges_copy[edge_to_remove]
    return edges_copy


if __name__ == '__main__':
    G = nx.Graph()
    nodes = range(7)
    G.add_nodes_from(nodes)
    edges = []
    for i in range(len(G.nodes)):
        for j in range(i + 1, len(G.nodes)):
            if random.randint(0, 1) == 1:
                edges.append((i, j, random.randint(1, 10)))

    G.add_weighted_edges_from(edges)
    edges_with_value = {}
    for edge in edges:
        edges_with_value[(edge[0], edge[1])] = edge[2]
    print_graph(G, edges_with_value)

    short_path_edges_with_value = get_shortest_path(edges_with_value)
    short_path_edges = []
    for edge in short_path_edges_with_value:
        short_path_edges.append((edge[0], edge[1], short_path_edges_with_value[edge]))
    NEW_G = nx.Graph()
    NEW_G.add_nodes_from(G.nodes)
    NEW_G.add_weighted_edges_from(short_path_edges)
    print_graph(NEW_G, short_path_edges_with_value)

    clustered_edges_with_value = divide_on_clusters(short_path_edges_with_value, G.nodes, 3)
    clustered_path_edges = []
    for edge in clustered_edges_with_value:
        clustered_path_edges.append((edge[0], edge[1], clustered_edges_with_value[edge]))
    CLUSTERED_G = nx.Graph()
    CLUSTERED_G.add_nodes_from(G.nodes)
    CLUSTERED_G.add_weighted_edges_from(clustered_path_edges)
    print_graph(CLUSTERED_G, clustered_edges_with_value)
