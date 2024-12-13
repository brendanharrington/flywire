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

def print_motif_statistics(g):
    num_v_in_motif = 3
    motifs, num_motifs = gt.motifs(g, num_v_in_motif)
    print('Number of motifs:', num_motifs)

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

def plot_degree_distribution(g, degree_type="in", weighted=False, flag=0):
    """
    Plot the degree distribution of a graph.

    Parameters:
    g: graph_tool.Graph
        The graph object.
    degree_type: str
        "in" for in-degrees, "out" for out-degrees.
    weighted: bool
        True for weighted degree distribution, False for unweighted.
    flag: bool
        Print if 1
    """
    # Determine degree calculation based on parameters
    if degree_type == "in":
        if weighted:
            degrees = g.get_in_degrees(list(g.vertices()), g.ep.syn_count)
            title = "In-degree distribution (weighted)"
        else:
            degrees = g.get_in_degrees(list(g.vertices()))
            title = "In-degree distribution (unweighted)"
    elif degree_type == "out":
        if weighted:
            degrees = g.get_out_degrees(list(g.vertices()), g.ep.syn_count)
            title = "Out-degree distribution (weighted)"
        else:
            degrees = g.get_out_degrees(list(g.vertices()))
            title = "Out-degree distribution (unweighted)"
    else:
        raise ValueError("degree_type must be either 'in' or 'out'.")

    # Create histogram
    if flag == 1:
        bin_range = int((max(degrees)) - min(degrees))+1
        counts, bins = np.histogram(degrees, bin_range)
        plt.figure(figsize=(10, 5))
        plt.stairs(counts, bins)
        plt.xlabel('Degree (k)')
        plt.ylabel('Frequency')
        plt.title(title)
        plt.show()

    return degrees

def print_basic_statistics(g, flag):
    n = g.num_vertices()
    m = g.num_edges()
    k_ins_unweighted = plot_degree_distribution(g, degree_type='in', weighted=False) # add 'flag=1' as a parameter to plot a histogram
    k_ins_weighted = plot_degree_distribution(g, degree_type='in', weighted=True) # add 'flag=1' as a parameter to plot a histogram
    k_outs_unweighted = plot_degree_distribution(g, degree_type='out', weighted=False) # add 'flag=1' as a parameter to plot a histogram
    k_outs_weighted = plot_degree_distribution(g, degree_type='out', weighted=True) # add 'flag=1' as a parameter to plot a histogram

    print('\nNumber of nodes:', n, '\n',
          'Number of edges:', m, '\n',
          'Mean degree (unweighted):', np.mean(k_ins_unweighted), '\n',
          'Mean degree (weighted)', np.mean(k_ins_weighted), '\n')

    print('=== IN DEGREE ===', '\n',
          '=== UNWEIGHTED ===', '\n',
          'Maximum:', max(k_ins_unweighted), '\n',
          'Minimum:', min(k_ins_unweighted), '\n',
          '=== WEIGHTED ===', '\n',
          'Maximum:', max(k_ins_weighted), '\n',
          'Minimum:', min(k_ins_weighted), '\n')
    
    print('=== OUT DEGREE ===', '\n',
          '=== UNWEIGHTED ===', '\n',
          'Maximum:', max(k_outs_unweighted), '\n',
          'Minimum:', min(k_outs_unweighted), '\n',
          '=== WEIGHTED ===', '\n',
          'Maximum:', max(k_outs_weighted), '\n',
          'Minimum:', min(k_outs_weighted), '\n')
    
    
    print('=== TOTAL DEGREE ===', '\n',
          'UNWEIGHTED', '\n',
          'Mean:', np.mean(k_ins_unweighted), '\n',
          'Maximum:', max(k_ins_unweighted), '\n',
          'Minimum:', min(k_ins_unweighted), '\n',
          '\n',
          'WEIGHTED', '\n',
          'Mean:', np.mean(k_ins_weighted), '\n',
          'Maximum:', max(k_ins_weighted), '\n',
          'Minimum:', min(k_ins_weighted), '\n')

def print_summmary_statistics(g, version):
    n = g.num_vertices()
    m = g.num_edges()
    k_mean = m/n
    connection_probability = m / (n*(n-1))
    reciprocity = gt.edge_reciprocity(g)

    dist_unweighted, ends_unweighted = gt.pseudo_diameter(g)
    dist_weighted, ends_weighted =  gt.pseudo_diameter(g, weights=g.ep.syn_count)
    c, num_triangles, num_triples = gt.global_clustering(g, ret_counts=True)

    in_degrees = g.get_in_degrees(g.get_vertices())
    out_degrees = g.get_out_degrees(g.get_vertices())
    total_degrees = in_degrees + out_degrees
    
    print(f'\n=== v{version} ===')
    print('\nNumber of Nodes:', n)
    print('Number of Edges:', m)

    print(f'\nAverage Node Degree: {k_mean:4f}')
    print(f'\nAverage Node Degree: {k_mean:4f}')
    print('Maximum Node Degree:', max(total_degrees))
    print('Minimum Node Degree:', min(total_degrees))

    print(f'\nConnection Probability: {connection_probability:4f}')
    print(f'Reciprocity: {reciprocity:4f}\n')

    print('Pseudo-diameter:', dist_unweighted)
    print(f'Clustering coefficient: {c[0]:4f} with standard deviation {c[1]:4f}')
    print(f'Number of triangles: {num_triangles}')
    print(f'Number of triples: {num_triples}', '\n')

