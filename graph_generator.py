import networkx as nx
import random

def generate_random_graph(num_nodes, num_edges, directed=False):
    graph_type = random.choice(['cycle', 'dense', 'sparse'])
    if graph_type == 'cycle':
        return create_cycle_graph(num_nodes, directed=directed)
    elif graph_type == 'dense':
        return create_dense_graph(num_nodes, directed=directed)
    elif graph_type == 'sparse':
        return create_sparse_graph(num_nodes, directed=directed)

def create_random_graph(num_nodes, num_edges, directed=False):
    graph = nx.DiGraph() if directed else nx.Graph()
    graph.add_nodes_from(range(num_nodes))
    while graph.number_of_edges() < num_edges:
        u = random.randint(0, num_nodes - 1)
        v = random.randint(0, num_nodes - 1)
        if u != v:
            weight = random.randint(1, 10)
            graph.add_edge(u, v, weight=weight)
    return graph

def create_cycle_graph(num_nodes, directed=False):
    weights = range(1, 10)
    cycle = nx.DiGraph() if directed else nx.Graph()
    edges = [(i, (i + 1) % num_nodes, random.choice(weights)) for i in range(num_nodes)]
    cycle.add_weighted_edges_from(edges)
    return cycle

def create_dense_graph(num_nodes, directed=False):
    graph = nx.DiGraph() if directed else nx.Graph()
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            weight = random.randint(1, 10)
            graph.add_edge(i, j, weight=weight)
            if directed:
                graph.add_edge(j, i, weight=weight)
    return graph

def create_sparse_graph(num_nodes, directed=False):
    return create_random_graph(num_nodes, num_nodes - 1, directed)
