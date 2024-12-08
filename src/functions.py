import graph_tool.all as gt
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
import time
import pickle
import gzip
import datetime

def run_loop(g):
    while True:
        print('\n========= OPTIONS =========')
        print('[0]: Print graph')
        print('[1]: Print blockmodel graph')
        print('[q]: Quit')
        
        choice = input('\nEnter the number of what you\'d like to do: ')

        match choice:
            case '0':
                gt.graph_draw(g)
            case '1':
                state = gt.minimize_blockmodel_dl(g)
                state.draw()
            case 'q':
                print('\nQuitting...')
                break
            case _:
                print('\nInvalid entry, try again.')


def average_shortest_path_length(g):
    """
    Calculate the average shortest path length using graph-tool.

    Parameters:
        g (Graph): A graph-tool Graph object.

    Returns:
        float: Average shortest path length.
    """
    # Compute all-pairs shortest distances
    total_length = 0
    total_pairs = 0

    distances = gt.shortest_distance(g, weights=g.ep.syn_count).a

    

    for v in g.vertices():
        distances = gt.shortest_distance(g, source=v, weights=g.ep.syn_count).a  # Get as numpy array
        finite_distances = distances[distances < float("inf")]
        total_length += finite_distances.sum()
        total_pairs += len(finite_distances) - 1  # Exclude self-distances

    if total_pairs > 0:
        return total_length / total_pairs
    else:
        return float("inf")



def print_summmary_statistics(g):
    dist_unweighted, ends_unweighted = gt.pseudo_diameter(g)
    dist_weighted, ends_weighted =  gt.pseudo_diameter(g, weights=g.ep.syn_count)
    c, num_triangles, num_triples = gt.global_clustering(g, weight=g.ep.syn_count, ret_counts=True)
    
    print('Pseudo-diameter: (weighted):', dist_weighted)
    print('Average shortest path length:', average_shortest_path_length(g))
    print('Clustering coefficient:', c[0], 'with standard deviation', c[1])
    print('Number of triangles:', num_triangles)
    print('Number of triples:', num_triples)

def print_motif_statistics(g):
    num_v_in_motif = 3
    motifs, num_motifs = gt.motifs(g, num_v_in_motif)
    print('Number of motifs:', num_motifs)

def load_graph(file_name):
    g = gt.load_graph(file_name)

    print("\Loaded graph from", file_name, ".")
    print(f"Vertices: {g.num_vertices():,}")
    print(f"Edges: {g.num_edges():,}.")

    print("\n=== PROPERTY LIST ===")
    g.list_properties()

    return g

def load_state(filepath):
    """Load a nested state object from a gzipped pickle file."""
    with gzip.open(filepath, 'rb') as f:
        return pickle.load(f)
    
def plot_PDFhist(kis):
    # input : a list of degrees, e.g., from a networkx graph G
    # output: a plot of the PDF of the degree distribution Pr(k) as a simple histogram for k>=1
    
    kmax = max(kis)

    # histogram and plot
    counts, bins = np.histogram(kis, bins=[i for i in range(kmax+2)], density=True)
    plt.bar(bins[1:-1], counts[1:], facecolor='r', alpha=0.5)    
    plt.xlabel('Degree, k')
    plt.ylabel('Pr(k)')
    plt.show()
    return

def plot_PDFsemi(kis):
    # input : a list of degrees, e.g., from a networkx graph G
    # output: a plot of the PDF of the degree distribution Pr(k) on semi-log axes for k>=1
    
    kmax = max(kis)

    # histogram and plot
    counts, bins = np.histogram(kis, bins=[i for i in range(kmax+2)], density=True)
    plt.semilogx(bins[1:-1], counts[1:], 'rs-', alpha=0.5)
    plt.xlabel('Degree, k')
    plt.ylabel('Pr(k)')
    plt.show()
    return

def plot_PDFloglog(kis):
    # input : a list of degrees, e.g., from a networkx graph G
    # output: a plot of the PDF of the degree distribution Pr(k) on log-log axes for k>=1
    
    kmax = max(kis)

    # histogram and plot
    counts, bins = np.histogram(kis, bins=[i for i in range(kmax+2)], density=True)
    plt.loglog(bins[1:-1], counts[1:], 'rs', alpha=0.5)
    plt.xlabel('Degree, k')
    plt.ylabel('Pr(k)')
    plt.show()
    return

def plot_CCDF(kis):
    # input : a list of degrees, e.g., from a networkx graph G
    # output: a plot of the CCDF of the degree distribution Pr(K>=k) for k>=1
    
    kmax = max(kis)

    # histogram and plot
    counts, bins = np.histogram(kis, bins=[i for i in range(kmax+2)], density=True)
    cumcounts = np.cumsum(counts)
    cumcounts = np.insert(cumcounts,0,0)
    plt.loglog(bins[1:-1], 1-cumcounts[1:-1], 'rs', alpha=0.5)
    plt.xlabel('Degree, k')
    plt.ylabel('Pr(K>=k)')
    plt.show()
    return

def generate_timestamped_filename(base_name, extension):
    """Generate a unique filename with a timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{base_name}_{timestamp}.{extension}"

def print_graph_stats(graph):
    """Print basic statistics for a graph."""
    print("\nGRAPH STATISTICS")
    print("Vertices:", graph.num_vertices())
    print("Edges:", graph.num_edges())
    print("Vertex properties:", list(graph.vp.keys()))
    print("Edge properties:", list(graph.ep.keys()))

def plot_ccdf(graph):
    """Plot the CCDF of the degree distribution of a graph."""
    degrees = [v.out_degree() for v in graph.vertices()]  # Use in_degree() for in-degrees
    sorted_degrees = sorted(degrees, reverse=True)

    # Compute CCDF
    ccdf = np.arange(1, len(sorted_degrees) + 1) / len(sorted_degrees)

    # Plot
    plt.figure(figsize=(8, 6))
    plt.loglog(sorted_degrees, ccdf, marker='o', linestyle='', markersize=5, label="CCDF")
    plt.xlabel("Degree (log scale)")
    plt.ylabel("CCDF (log scale)")
    plt.title("Complementary Cumulative Distribution Function (CCDF)")
    plt.legend()
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)

    # Show the plot
    plt.show()

def visualize_graph(g, file_name="graph.png"):
    gt.graph_draw(g, output=file_name)
    print(f"Graph visualization saved to {file_name}")

def filter_graph(g, threshold):
  print(f"\nFiltering out vertices with less than {threshold} synapses ...")
  start = time.time()
  filtered_g = gt.GraphView(g, efilt=lambda e: g.ep["syn_count"][e] > threshold)
  print("Completed in ", time.time()-start, "seconds")

  print("\n=== GRAPH SUMMARY ===")
  print(f"Vertices: {filtered_g.num_vertices():,}", f"Edges: {filtered_g.num_edges():,}.")

  return filtered_g

def compute_metrics(g):
    # Compute and print degree distribution
    in_degrees = g.get_in_degrees(g.get_vertices())
    out_degrees = g.get_out_degrees(g.get_vertices())
    print("In-Degree Distribution:", in_degrees)
    print("Out-Degree Distribution:", out_degrees)

    # Compute clustering coefficient
    clustering_coeff = gt.global_clustering(g)[0]
    print(f"Average Clustering Coefficient: {clustering_coeff:.4f}")

def sbm():
    start = time.time()

    print("\nLoading connections.gt.gz ...")
    g = gt.load_graph("data/connections.gt.gz")
    print("Successfully loaded connections.gt.gz!")

    print("\nCreating a BlockState object for the graph ...")
    state = gt.minimize_blockmodel_dl(g)
    print("Successfully created BlockState!")

    print("\nBlockState Statistics:")
    blocks = state.get_blocks()

    num_nodes = state.get_N()
    print(f'Total number of nodes: {num_nodes}')

    num_edges = state.get_E()
    print(f'Total number of edges: {num_edges}')

    num_blocks = state.get_B()
    print(f'Total number of blocks: {num_blocks}')

    eff_num_blocks = state.get_Be()
    print(f'Effective number of blocks: {eff_num_blocks}')

    # Calculate entropy of the model
    entropy = state.entropy()
    print(f"Model entropy: {entropy}")

    # Calculate the description length (DL)
    dl = state.entropy(dl=True)
    print(f"Model description length: {dl}") 

    end = time.time()
    print(f"\nExecution time: {end - start} seconds")

def is_graph_connected(edges, num_nodes):
    """ 
    Check if a graph is connected.

    Parameters:
        edges (list of tuples): List of (source, target, weight) edges.
        num_nodes (int): Total number of nodes in the graph.

    Returns:
        bool: True if the graph is connected, False otherwise.
    """
    # Build adjacency list
    adjacency_list = defaultdict(list)
    for src, tgt, weight in edges:
        adjacency_list[src].append(tgt)
        adjacency_list[tgt].append(src)

    visited = set()

    def dfs(node):
        """Depth-First Search to visit nodes."""
        visited.add(node)
        for neighbor in adjacency_list[node]:
            if neighbor not in visited:
                dfs(neighbor)

    # Start DFS from the first node
    dfs(0)

    # Check if all nodes are visited
    return len(visited) == num_nodes