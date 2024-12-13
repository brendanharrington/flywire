import graph_tool.all as gt
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
import time
import pickle
import gzip
import datetime

""" 
LOOP
"""
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


def print_motif_statistics(g):
    num_v_in_motif = 3
    motifs, num_motifs = gt.motifs(g, num_v_in_motif)
    print('Number of motifs:', num_motifs)

""" 
PLOT
"""
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


""" 
PRINT 
"""

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

""" 
MISC
"""
def count_FFBL_motifs(g,flag=0):
    # input : a networkx digraph G and a binary-valued variabe flag
    # output: if flag=1, a print statement of the type {FFL,FBL} and its member edges for each found motif
    #         a list (FFL,FBL) of the counts of feed-forward and feed-back loops in G
    
    # YOUR CODE HERE
    FFL_count = 0
    FBL_count = 0

    for i in g.get_vertices():
        for j in g.get_out_neighbors(i):
            for k in g.get_out_neighbors(j):
                if k == i:
                    continue  
                
                if g.edge(i, k):
                    FFL_count += 1
                    if flag == 1:
                        print(f"FFL: ({i},{j}),({j},{k}),({i},{k})")
                
                if g.edge(k, i):
                    FBL_count += 1
                    if flag == 1:
                        print(f"FBL: ({i},{j}),({j},{k}),({k},{i})")
                        
    return FFL_count,FBL_count