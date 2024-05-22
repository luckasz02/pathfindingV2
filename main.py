from flask import Flask, render_template, jsonify, request
import pathfinding
import graph_generator
import networkx as nx
import json

app = Flask(__name__)
current_graph = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/find_path', methods=['POST'])
def find_path():
    global current_graph
    data = request.json
    start_node = int(data['start_node'])
    end_node = int(data['end_node'])
    algorithm = data['algorithm']
    result = pathfinding.find_path(current_graph, start_node, end_node, algorithm)
    return jsonify(result)

@app.route('/generate_graph', methods=['POST'])
def generate_graph():
    global current_graph
    data = request.json
    num_nodes = data['num_nodes']
    num_edges = data['num_edges']
    graph_type = data['graph_type']
    directed = data['directed']

    if graph_type == 'random':
        graph = graph_generator.generate_random_graph(num_nodes, num_edges, directed)
    elif graph_type == 'cycle':
        graph = graph_generator.create_cycle_graph(num_nodes, directed=directed)
    elif graph_type == 'dense':
        graph = graph_generator.create_dense_graph(num_nodes, directed)
    elif graph_type == 'sparse':
        graph = graph_generator.create_sparse_graph(num_nodes, directed)

    current_graph = graph

    graph_data = nx.readwrite.json_graph.cytoscape_data(graph)
    return jsonify(graph_data)

if __name__ == '__main__':
    app.run(debug=True)
