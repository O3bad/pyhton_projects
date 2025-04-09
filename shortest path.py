import heapq as priority_queue

def shortest_path_with_skips(num_nodes, edges, start_node, destination_node, max_skips):
    graph = {node: [] for node in range(num_nodes)}
    for source, target, weight in edges:
        graph[source].append((target, weight))

    queue = [(0, start_node, max_skips + 1)]
    processed_nodes = {}

    while queue:
        current_path_cost, current_node, remaining_skips = priority_queue.heappop(queue)

        if current_node == destination_node:
            return current_path_cost

        if current_node in processed_nodes and processed_nodes[current_node] >= remaining_skips:
            continue

        processed_nodes[current_node] = remaining_skips

        if remaining_skips:
            for neighbor, edge_weight in graph.get(current_node, []):
                priority_queue.heappush(queue, (current_path_cost + edge_weight, neighbor, remaining_skips - 1))

    return -1

num_nodes_example = 4
edge_list_example = [[0, 1, 100], [1, 2, 100], [2, 3, 100], [0, 2, 500]]
start_node_example, destination_node_example, max_skips_example = 0, 3, 1
print(shortest_path_with_skips(num_nodes_example, edge_list_example, start_node_example, destination_node_example, max_skips_example))