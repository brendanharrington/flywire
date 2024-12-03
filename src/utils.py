from datetime import datetime

def generate_timestamped_filename(base_name, extension):
    """Generate a unique filename with a timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{base_name}_{timestamp}.{extension}"

def print_graph_stats(graph):
    """Print basic statistics for a graph."""
    print("GRAPH STATISTICS")
    print("Vertices:", graph.num_vertices())
    print("Edges:", graph.num_edges())
    print("Vertex properties:", list(graph.vp.keys()))
    print("Edge properties:", list(graph.ep.keys()))

def print_greeting():
    print('Hello from utils.h!')