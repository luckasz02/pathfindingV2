import heapq
import networkx as nx
import time

def find_path(graph, start_node, end_node, algorithm):
    if algorithm == "astar":
        return a_star_algorithm(graph, start_node, end_node)
    elif algorithm == "bidijkstra":
        return bidirectional_dijkstra(graph, start_node, end_node)
    elif algorithm == "bellmanford":
        return bellman_ford_algorithm(graph, start_node, end_node)

def a_star_algorithm(graph, start, goal):
    start_time = time.time()
    open_set = set([start])
    came_from = {}
    g_score = {node: float('inf') for node in graph.nodes()}
    g_score[start] = 0
    f_score = {node: float('inf') for node in graph.nodes()}
    f_score[start] = heuristic(start, goal)
    steps = []

    while open_set:
        current = min(open_set, key=lambda node: f_score[node])
        if current == goal:
            path = reconstruct_path(came_from, current)
            total_distance = g_score[goal]
            computation_time = time.time() - start_time
            return {
                "ComputationTime": computation_time,
                "NodesVisited": len(steps),
                "Route": path,
                "TotalDistance": total_distance
            }

        open_set.remove(current)
        steps.append(current)
        for neighbor in graph.neighbors(current):
            tentative_g_score = g_score[current] + graph[current][neighbor].get('weight', 1)
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                if neighbor not in open_set:
                    open_set.add(neighbor)

    return {
        "ComputationTime": time.time() - start_time,
        "NodesVisited": len(steps),
        "Route": [],
        "TotalDistance": float('inf')
    }

def heuristic(node1, node2):
    return 0  # Simplistic heuristic for demo purposes

def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    total_path.reverse()
    return total_path

def bidirectional_dijkstra(graph, start, goal):
    start_time = time.time()
    def dijkstra_partial(source, target, graph, steps, label):
        q, seen, mins = [(0, source, ())], set(), {source: 0}
        while q:
            (cost, v1, path) = heapq.heappop(q)
            if v1 not in seen:
                seen.add(v1)
                path = (v1, path)
                steps.append(v1)
                if v1 == target:
                    return cost, path
                
                for v2 in graph.neighbors(v1):
                    if v2 in seen:
                        continue
                    prev = mins.get(v2, None)
                    next_cost = cost + graph[v1][v2].get('weight', 1)
                    if prev is None or next_cost < prev:
                        mins[v2] = next_cost
                        heapq.heappush(q, (next_cost, v2, path))
        return float('inf'), []
    
    steps = []
    forward_cost, forward_path = dijkstra_partial(start, goal, graph, steps, 'forward')
    backward_cost, backward_path = dijkstra_partial(goal, start, graph, steps, 'backward')

    if forward_cost < backward_cost:
        path = reconstruct_path_bidirectional(forward_path)
        total_distance = forward_cost
    else:
        path = reconstruct_path_bidirectional(backward_path)
        total_distance = backward_cost
    computation_time = time.time() - start_time
    return {
        "ComputationTime": computation_time,
        "NodesVisited": len(steps),
        "Route": path,
        "TotalDistance": total_distance
    }

def reconstruct_path_bidirectional(path):
    result_path = []
    while path:
        node, path = path
        result_path.append(node)
    return result_path[::-1]

def bellman_ford_algorithm(graph, start, goal):
    start_time = time.time()
    distance = {node: float('inf') for node in graph.nodes()}
    predecessor = {node: None for node in graph.nodes()}
    distance[start] = 0
    steps = []

    for _ in range(len(graph) - 1):
        for node in graph.nodes():
            for neighbor in graph.neighbors(node):
                weight = graph[node][neighbor].get('weight', 1)
                if distance[node] + weight < distance[neighbor]:
                    distance[neighbor] = distance[node] + weight
                    predecessor[neighbor] = node
                    steps.append(neighbor)

    for node in graph.nodes():
        for neighbor in graph.neighbors(node):
            weight = graph[node][neighbor].get('weight', 1)
            if distance[node] + weight < distance[neighbor]:
                return {
                    "ComputationTime": time.time() - start_time,
                    "NodesVisited": "Not applicable for Bellman-Ford",
                    "Route": "Path not provided by Bellman-Ford",
                    "TotalDistance": float('inf'),
                    "Error": "Graph contains a negative weight cycle"
                }
    
    path = reconstruct_path_bellman_ford(predecessor, goal)
    total_distance = distance[goal]
    computation_time = time.time() - start_time
    return {
        "ComputationTime": computation_time,
        "NodesVisited": "Not applicable for Bellman-Ford",
        "Route": path,
        "TotalDistance": total_distance
    }

def reconstruct_path_bellman_ford(predecessor, goal):
    path = []
    while goal is not None:
        path.append(goal)
        goal = predecessor[goal]
    path.reverse()
    return path
