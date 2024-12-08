import graph_tool.all as gt
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
import time
import pickle
import gzip

import functions as fnc


def main():
    g = gt.load_graph(file_name=f"data/connections.gt.gz")
    fnc.print_summmary_statistics(g)
    print(fnc.average_shortest_path_length(g))

    # filtered_g = fg.filter_graph(g, threshold=100)
    # gt.draw(filtered_g)
    
    
    # edges = g.get_all_edges()
    # num_nodes = g.num_vertices()

    # connected = is_graph_connected(edges, num_nodes)
    # print("Is the graph connected?", connected)

    # d_map, d_hist = gt.label_components(g, directed=True)

    # print(d_hist)

    # fnc.print_summmary_statistics(g)
    # fnc.run_loop(g)
    
    
if __name__ == "__main__":
    main()