from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

# def generate_timestamped_filename(base_name, extension):
#     """Generate a unique filename with a timestamp."""
#     timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
#     return f"{base_name}_{timestamp}.{extension}"

# def print_graph_stats(graph):
#     """Print basic statistics for a graph."""
#     print("\nGRAPH STATISTICS")
#     print("Vertices:", graph.num_vertices())
#     print("Edges:", graph.num_edges())
#     print("Vertex properties:", list(graph.vp.keys()))
#     print("Edge properties:", list(graph.ep.keys()))

# def plot_ccdf(graph):
#     """Plot the CCDF of the degree distribution of a graph."""
#     degrees = [v.out_degree() for v in graph.vertices()]  # Use in_degree() for in-degrees
#     sorted_degrees = sorted(degrees, reverse=True)

#     # Compute CCDF
#     ccdf = np.arange(1, len(sorted_degrees) + 1) / len(sorted_degrees)

#     # Plot
#     plt.figure(figsize=(8, 6))
#     plt.loglog(sorted_degrees, ccdf, marker='o', linestyle='', markersize=5, label="CCDF")
#     plt.xlabel("Degree (log scale)")
#     plt.ylabel("CCDF (log scale)")
#     plt.title("Complementary Cumulative Distribution Function (CCDF)")
#     plt.legend()
#     plt.grid(True, which="both", linestyle="--", linewidth=0.5)

#     # Show the plot
#     plt.show()

def compute_metrics(g):
    # Compute and print degree distribution
    in_degrees = g.get_in_degrees(g.get_vertices())
    out_degrees = g.get_out_degrees(g.get_vertices())
    print("In-Degree Distribution:", in_degrees)
    print("Out-Degree Distribution:", out_degrees)

    # Compute clustering coefficient
    clustering_coeff = gt.global_clustering(g)[0]
    print(f"Average Clustering Coefficient: {clustering_coeff:.4f}")

def visualize_graph(g, file_name="graph.png"):
    gt.graph_draw(g, output=file_name)
    print(f"Graph visualization saved to {file_name}")
