import graph_tool.all as gt
import matplotlib.pyplot as plt
import numpy as np

import functions as fnc



def plot_both_versions(g, g2):
    # Process graph g
    edge_order_w_size_g = sorted([[e[0], e[1], e[2]] for e in g.get_edges([g.ep["syn_count"]])], 
                                  key=lambda e: e[2])
    edge_order_g = np.array(edge_order_w_size_g)[:, :2]
    edge_size_g = np.array(edge_order_w_size_g)[:, 2]
    sizes_g, _ = gt.edge_percolation(g, edge_order_g)

    # Process graph g2
    edge_order_w_size_g2 = sorted([[e[0], e[1], e[2]] for e in g2.get_edges([g2.ep["syn_count"]])], 
                                   key=lambda e: e[2])
    edge_order_g2 = np.array(edge_order_w_size_g2)[:, :2]
    edge_size_g2 = np.array(edge_order_w_size_g2)[:, 2]
    sizes_g2, _ = gt.edge_percolation(g2, edge_order_g2)

    # Create the plot
    fig, ax = plt.subplots(1, 1, figsize=(8, 5))
    ax2 = ax.twinx()

    # Plot sizes for g and g2
    ax.plot(sizes_g, 'red', label="g: Largest WCC")
    ax.plot(sizes_g2, 'blue', label="g2: Largest WCC")

    # Plot edge weights for g and g2
    ax2.plot(np.insert(edge_size_g, 0, 0)[:len(sizes_g)], 'gray', linestyle='dotted', label="g: Connection Weight")
    ax2.plot(np.insert(edge_size_g2, 0, 0)[:len(sizes_g2)], 'black', linestyle='dashed', label="g2: Connection Weight")

    # Add labels and legends
    ax.set_ylabel("Size of the largest WCC")
    ax2.set_ylabel("Largest connection weight", color='gray')
    ax2.set_yscale('log')
    ax.set_xlabel("# of remaining edges")

    ax.legend(loc="upper left")
    ax2.legend(loc="upper right")

    plt.title("Comparison of Edge Percolation for g and g2")
    plt.show()


def main():
    version = '783'
    file_name = 'data/connections-v' + version + '.gt.gz'

    g = gt.load_graph(file_name=file_name)
    g2 = gt.load_graph(file_name='data/connections-v630.gt.gz')
    
    # fnc.print_summmary_statistics(g, version)

    plot_both_versions(g, g2)

if __name__ == "__main__":
    main()
