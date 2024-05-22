# Graph Algorithm Visualizer

Graph Algorithm Visualizer is a web application that allows users to generate various types of graphs and visualize different pathfinding algorithms like A\*, Bidirectional Dijkstra, and Bellman-Ford on them.

## Features

- **Generate Graphs:** Create random, cycle, dense, or sparse graphs with customizable number of nodes and edges.
- **Visualize Pathfinding Algorithms:** Visualize paths found using A\*, Bidirectional Dijkstra, and Bellman-Ford algorithms.
- **Interactive Interface:** Select nodes and find paths interactively on the graph.

## Installation

To run this project locally, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/graph-algorithm-visualizer.git
   cd graph-algorithm-visualizer
   ```

2. **Set up a virtual environment and activate it:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

   Ensure `requirements.txt` includes:

   ```text
   Flask
   networkx
   ```

## Usage

1. **Run the Flask application:**

   ```bash
   python main.py
   ```

2. **Open your browser and go to:**

   ```
   http://127.0.0.1:5000
   ```

3. **Generate a graph:**

   - Select the graph type (Random, Cycle, Dense, Sparse).
   - Specify the number of nodes and edges.
   - Choose whether the graph should be directed or not.
   - Click "Generate Graph".

4. **Select nodes and find paths:**

   - Click on the nodes to select them.
   - Choose the pathfinding algorithm (A\*, Bidirectional Dijkstra, Bellman-Ford).
   - Click "Find Path".

## Project Structure

- `app.js`: Handles the client-side logic for generating and visualizing graphs.
- `index.html`: Main HTML page with the user interface.
- `style.css`: Styles for the application.
- `main.py`: Flask server for handling requests.
- `pathfinding.py`: Implements the pathfinding algorithms.
- `graph_generator.py`: Generates different types of graphs.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
